using UnityEngine;
using System.Collections;
using System.Collections.Generic;

/// <summary>
/// Mision de postura parado.
/// Trigger detecta al jugador, muestra indicador de space,
/// lanza dialogos, suscribe mision y maneja cinematica de exito/fallo.
/// </summary>
public class MisionPosturaParado : MonoBehaviour
{
    [Header("Referencias")]
    [Tooltip("Sprite hijo que indica al jugador que presione space")]
    public GameObject indicadorSpace;

    [Tooltip("PENSAMIENTOJUGADOR — se activa al terminar el diálogo inicial")]
    public GameObject pensamientoJugador;

    [Tooltip("Cuadro negro de la cámara para la cinemática")]
    public Transform cuadroNegro;

    [Tooltip("Pared u obstáculo que se desactiva al completar la misión")]
    public GameObject pared;

    [Header("Diálogos")]
    public DialogoData dialogoInicial;
    public DialogoData dialogoExito;
    public DialogoData dialogoFallo;

    [Header("Cinemática — Sprites")]
    [Tooltip("Sprites que se DESACTIVAN en el primer swap")]
    public List<SpriteRenderer> spritesDesactivar;

    [Tooltip("Sprites que se ACTIVAN en el primer swap")]
    public List<SpriteRenderer> spritesActivar;

    [Header("Cinemática — Tiempos")]
    public float velocidadCuadro = 2f;
    public float tiempoAntesDeSwap = 0.3f;
    public float tiempoEntreSwapYSubida = 0.5f;
    public float tiempoAntesSegundoBajada = 0.8f;
    public float tiempoEntreSwapFinalYSubida = 0.5f;

    private bool _jugadorDentro = false;
    private bool _misionActiva = false;
    private JugadorData _jugadorData;
    private DialogoController _dialogoController;

    #region Unity Callbacks

    private void Awake()
    {
        _dialogoController = FindFirstObjectByType<DialogoController>();

        if (indicadorSpace != null)
            indicadorSpace.SetActive(false);
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

        if (indicadorSpace != null)
            indicadorSpace.SetActive(true);
    }

    private void OnTriggerExit(Collider other)
    {
        if (!other.CompareTag("Player")) return;

        _jugadorDentro = false;

        if (indicadorSpace != null)
            indicadorSpace.SetActive(false);
    }

    #endregion

    #region Flujo de Misión

    /// <summary>
    /// Espera un frame antes de abrir el dialogo para evitar que el mismo
    /// Space que inicia la mision lo consuma el DialogoController.
    /// </summary>
    private IEnumerator IniciarMisionSiguienteFrame()
    {
        _misionActiva = true;

        if (indicadorSpace != null)
            indicadorSpace.SetActive(false);

        if (_jugadorData != null)
            _jugadorData.puedeMoverse = false;

        yield return null; // ← espera el siguiente frame

        DialogoController.OnDialogoTerminado += AlTerminarDialogoInicial;
        _dialogoController.Iniciar(dialogoInicial);
    }

    /// <summary>Se llama al terminar el dialogo inicial; registra la mision de postura parado.</summary>
    private void AlTerminarDialogoInicial()
    {
        DialogoController.OnDialogoTerminado -= AlTerminarDialogoInicial;
        SuscribirMision();
    }

    /// <summary>
    /// Crea y asigna en MisionesGlobal una MisionPosicion que espera Postura=1 (parado).
    /// Activa el pensamiento del jugador una vez registrada la mision.
    /// </summary>
    private void SuscribirMision()
    {
        MisionPosicion mision = new MisionPosicion(
            TipoAccion.Postura,
            1, // parado
            AlAcertar,
            AlFallar
        );

        if (MisionesGlobal.Instancia != null)
            MisionesGlobal.Instancia.AsignarMision(mision);
        else
            Debug.LogError("[MisionPosturaParado] MisionesGlobal no encontrado.");

        // Se activa DESPUES de que termina el dialogo inicial
        if (pensamientoJugador != null)
            pensamientoJugador.SetActive(true);
    }


    /// <summary>Se llama cuando la postura elegida no es la correcta; muestra el dialogo de fallo.</summary>
    private void AlFallar()
    {
        if (pensamientoJugador != null)
            pensamientoJugador.SetActive(false);

        DialogoController.OnDialogoTerminado += AlTerminarDialogoFallo;
        _dialogoController.Iniciar(dialogoFallo);
    }

    /// <summary>Se llama al terminar el dialogo de fallo; reactiva el movimiento para reintentar.</summary>
    private void AlTerminarDialogoFallo()
    {
        DialogoController.OnDialogoTerminado -= AlTerminarDialogoFallo;

        if (_jugadorData != null)
            _jugadorData.puedeMoverse = true;

        _misionActiva = false;
    }


    /// <summary>Se llama cuando la postura elegida es correcta; muestra el dialogo de exito.</summary>
    private void AlAcertar()
    {
        if (pensamientoJugador != null)
            pensamientoJugador.SetActive(false);

        DialogoController.OnDialogoTerminado += AlTerminarDialogoExito;
        _dialogoController.Iniciar(dialogoExito);
    }

    /// <summary>Se llama al terminar el dialogo de exito; lanza la cinematica de cambio de sprites.</summary>
    private void AlTerminarDialogoExito()
    {
        DialogoController.OnDialogoTerminado -= AlTerminarDialogoExito;
        StartCoroutine(Cinematica());
    }

    #endregion

    #region Cinemática

    private IEnumerator Cinematica()
    {
        // 1 — Bajar cuadro negro
        yield return StartCoroutine(MoverCuadro(0f));
        yield return new WaitForSeconds(tiempoAntesDeSwap);

        // 2 — Primer swap de sprites
        SwapSprites(true);
        yield return new WaitForSeconds(tiempoEntreSwapYSubida);

        // 3 — Subir cuadro negro
        yield return StartCoroutine(MoverCuadro(2f));
        yield return new WaitForSeconds(tiempoAntesSegundoBajada);

        // 4 — Bajar cuadro negro de nuevo
        yield return StartCoroutine(MoverCuadro(0f));
        yield return new WaitForSeconds(tiempoAntesDeSwap);

        // 5 — Segundo swap (invertido)
        SwapSprites(false);
        yield return new WaitForSeconds(tiempoEntreSwapFinalYSubida);

        // 6 — Subir cuadro negro
        yield return StartCoroutine(MoverCuadro(2f));

        // 7 — Desactivar pared
        if (pared != null)
            pared.SetActive(false);

        // 8 — Devolver movimiento
        if (_jugadorData != null)
            _jugadorData.puedeMoverse = true;

        // 9 — Desactivar este script
        this.enabled = false;
    }

    /// <summary>
    /// primer swap: desactiva A y activa B.
    /// segundo swap: activa A y desactiva B.
    /// </summary>
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