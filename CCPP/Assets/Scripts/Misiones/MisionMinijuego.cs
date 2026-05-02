using UnityEngine;
using System.Collections;
using System.Collections.Generic;

/// <summary>
/// Misión genérica reutilizable.
/// Configura TipoAccion y respuestaEsperada desde el Inspector.
/// </summary>
public class MisionMinijuego : MonoBehaviour
{
    [Header("Referencias")]
    public GameObject indicadorSpace;
    public GameObject pensamientoJugador;
    public Transform cuadroNegro;

    [Header("Habilidad Nueva (opcional)")]
    public JugadorHabilidadesData habilidadesJugador;
    public ParteCuerpo habilidadADesbloquear;
    public GameObject uiNuevaHabilidad;

    [Header("Misión")]
    public TipoAccion tipoAccion;
    public int respuestaEsperada;

    [Header("Diálogos")]
    public DialogoData dialogoInicial;
    public DialogoData dialogoExito;
    public DialogoData dialogoFallo;

    [Header("Cinemática — Sprites")]
    public List<SpriteRenderer> spritesDesactivar;
    public List<SpriteRenderer> spritesActivar;

    [Header("Cinemática — Tiempos")]
    public float velocidadCuadro = 2f;
    public float tiempoAntesDeSwap = 0.3f;
    public float tiempoEntreSwapYSubida = 0.5f;
    public float tiempoAntesSegundoBajada = 0.8f;
    public float tiempoEntreSwapFinalYSubida = 0.5f;

    [Header("Objetos Finales")]
    public List<GameObject> objetosADesactivar;
    public List<GameObject> objetosAActivar;

    // ── Estado ────────────────────────────────────────────────────
    private bool _jugadorDentro = false;
    private bool _misionActiva = false;
    private JugadorData _jugadorData;
    private DialogoController _dialogoController;

    // ──────────────────────────────────────────────────────────────
    #region Unity Callbacks

    private void Awake()
    {
        _dialogoController = FindFirstObjectByType<DialogoController>();
        if (indicadorSpace != null) indicadorSpace.SetActive(false);
    }

    private void Update()
    {
        if (!_jugadorDentro || _misionActiva) return;
        if (Input.GetKeyDown(KeyCode.Space))
            StartCoroutine(IniciarMisionSiguienteFrame());
    }

    private void OnTriggerEnter(Collider other)
    {
        if (!other.CompareTag("Player")) return;
        _jugadorData = other.GetComponent<JugadorData>();
        _jugadorDentro = true;
        if (indicadorSpace != null) indicadorSpace.SetActive(true);
    }

    private void OnTriggerExit(Collider other)
    {
        if (!other.CompareTag("Player")) return;
        _jugadorDentro = false;
        if (indicadorSpace != null) indicadorSpace.SetActive(false);
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Flujo

    private IEnumerator IniciarMisionSiguienteFrame()
    {
        _misionActiva = true;
        if (indicadorSpace != null) indicadorSpace.SetActive(false);
        if (_jugadorData != null) _jugadorData.puedeMoverse = false;

        yield return null;

        DialogoController.OnDialogoTerminado += AlTerminarDialogoInicial;
        _dialogoController.Iniciar(dialogoInicial);
    }

    private void AlTerminarDialogoInicial()
    {
        DialogoController.OnDialogoTerminado -= AlTerminarDialogoInicial;

        if (habilidadesJugador != null)
        {
            DesbloquearHabilidad();
            if (uiNuevaHabilidad != null) uiNuevaHabilidad.SetActive(true);
        }

        SuscribirMision();
    }

    private void DesbloquearHabilidad()
    {
        switch (habilidadADesbloquear)
        {
            case ParteCuerpo.Piernas: habilidadesJugador.tienePiernas = true; break;
            case ParteCuerpo.Pecho: habilidadesJugador.tienePecho = true; break;
            case ParteCuerpo.Cabeza: habilidadesJugador.tieneCabeza = true; break;
            case ParteCuerpo.Boca: habilidadesJugador.tieneBoca = true; break;
            case ParteCuerpo.ManoDerecha: habilidadesJugador.tieneManoDerecha = true; break;
        }
    }

    private void SuscribirMision()
    {
        MisionPosicion mision = new MisionPosicion(
            tipoAccion, respuestaEsperada,
            AlAcertar, AlFallar
        );

        if (MisionesGlobal.Instancia != null)
            MisionesGlobal.Instancia.AsignarMision(mision);
        else
            Debug.LogError("[MisionMinijuego] MisionesGlobal no encontrado.");

        if (pensamientoJugador != null)
            pensamientoJugador.SetActive(true);
    }

    private void AlFallar()
    {
        if (pensamientoJugador != null) pensamientoJugador.SetActive(false);
        DialogoController.OnDialogoTerminado += AlTerminarDialogoFallo;
        _dialogoController.Iniciar(dialogoFallo);
    }

    private void AlTerminarDialogoFallo()
    {
        DialogoController.OnDialogoTerminado -= AlTerminarDialogoFallo;
        if (_jugadorData != null) _jugadorData.puedeMoverse = true;
        StartCoroutine(ReactivarSiguienteFrame());
    }

    private IEnumerator ReactivarSiguienteFrame()
    {
        yield return null;
        yield return null;
        _misionActiva = false;
    }

    private void AlAcertar()
    {
        if (pensamientoJugador != null) pensamientoJugador.SetActive(false);
        DialogoController.OnDialogoTerminado += AlTerminarDialogoExito;
        _dialogoController.Iniciar(dialogoExito);
    }

    private void AlTerminarDialogoExito()
    {
        DialogoController.OnDialogoTerminado -= AlTerminarDialogoExito;
        StartCoroutine(Cinematica());
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Cinemática

    private IEnumerator Cinematica()
    {
        yield return StartCoroutine(MoverCuadro(0f));
        yield return new WaitForSeconds(tiempoAntesDeSwap);
        SwapSprites(true);
        yield return new WaitForSeconds(tiempoEntreSwapYSubida);
        yield return StartCoroutine(MoverCuadro(2f));
        yield return new WaitForSeconds(tiempoAntesSegundoBajada);
        yield return StartCoroutine(MoverCuadro(0f));
        yield return new WaitForSeconds(tiempoAntesDeSwap);
        SwapSprites(false);
        yield return new WaitForSeconds(tiempoEntreSwapFinalYSubida);
        yield return StartCoroutine(MoverCuadro(2f));

        if (objetosADesactivar != null)
            foreach (GameObject obj in objetosADesactivar)
                if (obj != null) obj.SetActive(false);

        if (objetosAActivar != null)
            foreach (GameObject obj in objetosAActivar)
                if (obj != null) obj.SetActive(true);

        if (_jugadorData != null) _jugadorData.puedeMoverse = true;
        this.enabled = false;
    }

    private void SwapSprites(bool primerSwap)
    {
        foreach (SpriteRenderer sr in spritesDesactivar)
            if (sr != null) sr.enabled = !primerSwap;

        foreach (SpriteRenderer sr in spritesActivar)
            if (sr != null) sr.enabled = primerSwap;
    }

    private IEnumerator MoverCuadro(float yDestino)
    {
        if (cuadroNegro == null) yield break;

        Vector3 posInicial = cuadroNegro.localPosition;
        Vector3 posDestino = new Vector3(posInicial.x, yDestino, posInicial.z);
        float distancia = Mathf.Abs(posInicial.y - yDestino);
        if (distancia < 0.001f) yield break;

        float tiempoTotal = distancia / velocidadCuadro;
        float tiempoTranscurrido = 0f;

        while (tiempoTranscurrido < tiempoTotal)
        {
            tiempoTranscurrido += Time.deltaTime;
            float t = Mathf.Clamp01(tiempoTranscurrido / tiempoTotal);
            cuadroNegro.localPosition = Vector3.Lerp(posInicial, posDestino, t);
            yield return null;
        }

        cuadroNegro.localPosition = posDestino;
    }

    #endregion
}