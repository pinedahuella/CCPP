using UnityEngine;
using System.Collections;
using System.Collections.Generic;

/// <summary>
/// Mision generica reutilizable.
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

    private bool _jugadorDentro = false;
    private bool _misionActiva = false;
    private JugadorData _jugadorData;
    private DialogoController _dialogoController;

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

    #region Flujo

    /// <summary>
    /// Espera un frame para evitar que el Space que activa la mision sea consumido
    /// por el DialogoController, luego bloquea al jugador e inicia el dialogo.
    /// </summary>
    private IEnumerator IniciarMisionSiguienteFrame()
    {
        _misionActiva = true;
        if (indicadorSpace != null) indicadorSpace.SetActive(false);
        if (_jugadorData != null) _jugadorData.puedeMoverse = false;

        yield return null;

        DialogoController.OnDialogoTerminado += AlTerminarDialogoInicial;
        _dialogoController.Iniciar(dialogoInicial);
    }

    /// <summary>
    /// Se llama al terminar el dialogo inicial; desbloquea la habilidad si corresponde
    /// y registra la mision en MisionesGlobal.
    /// </summary>
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

    /// <summary>
    /// Activa el flag de habilidad correspondiente en JugadorHabilidadesData
    /// segun la parte del cuerpo configurada en el Inspector.
    /// </summary>
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

    /// <summary>
    /// Crea y asigna en MisionesGlobal una MisionPosicion con el tipo y valor esperados,
    /// luego activa el pensamiento del jugador.
    /// </summary>
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

    /// <summary>Se llama cuando el minijuego devuelve un resultado incorrecto; muestra el dialogo de fallo.</summary>
    private void AlFallar()
    {
        if (pensamientoJugador != null) pensamientoJugador.SetActive(false);
        DialogoController.OnDialogoTerminado += AlTerminarDialogoFallo;
        _dialogoController.Iniciar(dialogoFallo);
    }

    /// <summary>Se llama al terminar el dialogo de fallo; reactiva el movimiento y permite reintentar.</summary>
    private void AlTerminarDialogoFallo()
    {
        DialogoController.OnDialogoTerminado -= AlTerminarDialogoFallo;
        if (_jugadorData != null) _jugadorData.puedeMoverse = true;
        StartCoroutine(ReactivarSiguienteFrame());
    }

    /// <summary>
    /// Espera dos frames antes de desmarcar la mision como activa
    /// para evitar que el jugador la reactive el mismo frame que termino el dialogo.
    /// </summary>
    private IEnumerator ReactivarSiguienteFrame()
    {
        yield return null;
        yield return null;
        _misionActiva = false;
    }

    /// <summary>Se llama cuando el minijuego devuelve el resultado correcto; muestra el dialogo de exito.</summary>
    private void AlAcertar()
    {
        if (pensamientoJugador != null) pensamientoJugador.SetActive(false);
        DialogoController.OnDialogoTerminado += AlTerminarDialogoExito;
        _dialogoController.Iniciar(dialogoExito);
    }

    /// <summary>Se llama al terminar el dialogo de exito; lanza la cinematica de transicion.</summary>
    private void AlTerminarDialogoExito()
    {
        DialogoController.OnDialogoTerminado -= AlTerminarDialogoExito;
        StartCoroutine(Cinematica());
    }

    #endregion

    #region Cinemática

    /// <summary>
    /// Ejecuta la cinematica de transicion: baja cortina, hace swap de sprites,
    /// sube cortina, activa/desactiva objetos finales y reactiva al jugador.
    /// </summary>
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

    /// <summary>
    /// Intercambia la visibilidad de los grupos de sprites para simular el cambio de atuendo del jugador.
    /// </summary>
    /// <param name="primerSwap">Si es true aplica el primer intercambio; si es false lo invierte.</param>
    private void SwapSprites(bool primerSwap)
    {
        foreach (SpriteRenderer sr in spritesDesactivar)
            if (sr != null) sr.enabled = !primerSwap;

        foreach (SpriteRenderer sr in spritesActivar)
            if (sr != null) sr.enabled = primerSwap;
    }

    /// <summary>
    /// Mueve el cuadro negro suavemente hasta la posicion Y indicada.
    /// Y = 0 cubre la pantalla, Y = 2 la descubre.
    /// </summary>
    /// <param name="yDestino">Posicion Y local de destino del cuadro negro.</param>
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