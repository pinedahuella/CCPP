using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Collections;

/// <summary>
/// Gestiona el flujo completo de la misa.
/// Trigger → space → secuencia de escenas → vidas → ganar/perder.
/// </summary>
public class GestorMisa : MonoBehaviour
{
    // ── Referencias globales ───────────────────────────────────────
    [Header("Referencias")]
    public Transform cuadroNegro;
    public float velocidadCuadro = 3f;
    public AudioSource audioSource;
    public Animator animadorSacerdote;
    public Transform sacerdote;

    [Header("Jugador")]
    public JugadorData jugadorData;
    public GameObject visualJugadorReal;
    public Transform puntoResetJugador;
    public Transform transformJugador;

    [Header("UI")]
    public VidaUI vidaUI;
    public GameObject panelTitulo;
    public TextMeshProUGUI textoTitulo;
    public GameObject pensamientoJugador;

    [Header("Indicador space")]
    public GameObject indicadorSpace;

    [Header("Al ganar")]
    [Tooltip("GameObject del padre con la comunión, se activa al ganar")]
    public GameObject objetoGanar;

    [Header("Escenas")]
    public EscenaMisa[] escenas;

    // ── Estado ────────────────────────────────────────────────────
    private int _escenaActual = 0;
    private bool _jugadorDentro = false;
    private bool _enFlujo = false;
    private DialogoController _dialogoController;

    // ──────────────────────────────────────────────────────────────
    #region Unity Callbacks

    private void Awake()
    {
        _dialogoController = FindFirstObjectByType<DialogoController>();
    }

    private void Start()
    {
        if (indicadorSpace != null) indicadorSpace.SetActive(false);
        if (panelTitulo != null) panelTitulo.SetActive(false);
        if (objetoGanar != null) objetoGanar.SetActive(false);
        if (vidaUI != null) vidaUI.gameObject.SetActive(false);
    }

    private void Update()
    {
        if (!_jugadorDentro || _enFlujo) return;
        if (Input.GetKeyDown(KeyCode.Space))
            StartCoroutine(IniciarFlujo());
    }

    private void OnTriggerEnter(Collider other)
    {
        if (!other.CompareTag("Player")) return;
        _jugadorDentro = true;
        if (indicadorSpace != null) indicadorSpace.SetActive(true);
        if (vidaUI != null) vidaUI.gameObject.SetActive(true);
    }

    private void OnTriggerExit(Collider other)
    {
        if (!other.CompareTag("Player")) return;
        _jugadorDentro = false;
        if (indicadorSpace != null) indicadorSpace.SetActive(false);
        if (vidaUI != null) vidaUI.gameObject.SetActive(false);
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Flujo Principal

    private IEnumerator IniciarFlujo()
    {
        _enFlujo = true;
        if (indicadorSpace != null) indicadorSpace.SetActive(false);
        if (visualJugadorReal != null) visualJugadorReal.SetActive(false);
        if (jugadorData != null) jugadorData.puedeMoverse = false;

        yield return StartCoroutine(EjecutarEscena(_escenaActual));
    }

    private IEnumerator EjecutarEscena(int indice)
    {
        if (indice >= escenas.Length)
        {
            yield return StartCoroutine(Ganar());
            yield break;
        }

        EscenaMisa escena = escenas[indice];

        ConfigurarObjetos(escena);

        if (escena.musicaOpcional != null && audioSource != null)
        {
            audioSource.clip = escena.musicaOpcional;
            audioSource.Play();
        }

        if (!string.IsNullOrEmpty(escena.animacionSacerdote) && animadorSacerdote != null)
            animadorSacerdote.Play(escena.animacionSacerdote);

        if (escena.puntoDestino != null && sacerdote != null)
            yield return StartCoroutine(MoverSacerdote(escena));

        if (escena.mostrarTitulo)
            yield return StartCoroutine(MostrarTitulo(escena.textoTitulo));

        yield return StartCoroutine(EsperarDialogo(escena.dialogoInicial));
        yield return StartCoroutine(EsperarMision(escena));
    }

    private IEnumerator EsperarMision(EscenaMisa escena)
    {
        if (escena.visualesJugador != null)
            foreach (GameObject v in escena.visualesJugador)
                if (v != null) v.SetActive(true);

        if (pensamientoJugador != null)
            pensamientoJugador.SetActive(true);

        bool resultado = false;
        bool recibido = false;

        MisionPosicion mision = new MisionPosicion(
            escena.tipoAccion,
            escena.valorEsperado,
            () => { resultado = true; recibido = true; },
            () => { resultado = false; recibido = true; }
        );

        if (MisionesGlobal.Instancia != null)
            MisionesGlobal.Instancia.AsignarMision(mision);

        yield return new WaitUntil(() => recibido);

        if (pensamientoJugador != null)
            pensamientoJugador.SetActive(false);

        if (escena.visualesJugador != null)
            foreach (GameObject v in escena.visualesJugador)
                if (v != null) v.SetActive(false);

        if (resultado)
            yield return StartCoroutine(AlAcertar(escena));
        else
            yield return StartCoroutine(AlFallar(escena));
    }

    private IEnumerator AlAcertar(EscenaMisa escena)
    {
        yield return StartCoroutine(EsperarDialogo(escena.dialogoExito));
        _escenaActual++;
        yield return StartCoroutine(EjecutarEscena(_escenaActual));
    }

    private IEnumerator AlFallar(EscenaMisa escena)
    {
        yield return StartCoroutine(EsperarDialogo(escena.dialogoFallo));

        // Bajar cortina, resetear jugador, subir cortina y reintentar
        yield return StartCoroutine(MoverCuadro(0f));

        if (transformJugador != null && puntoResetJugador != null)
            transformJugador.position = puntoResetJugador.position;

        yield return new WaitForSeconds(0.3f);
        yield return StartCoroutine(MoverCuadro(2f));

        yield return StartCoroutine(EjecutarEscena(_escenaActual));
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Ganar / Reiniciar

    private IEnumerator Ganar()
    {
        if (objetoGanar != null) objetoGanar.SetActive(true);
        if (vidaUI != null) vidaUI.gameObject.SetActive(false);

        if (jugadorData != null) jugadorData.puedeMoverse = true;
        if (visualJugadorReal != null) visualJugadorReal.SetActive(true);

        _enFlujo = false;
        yield break;
    }

    private IEnumerator Reiniciar()
    {
        yield return StartCoroutine(MoverCuadro(0f));

        _escenaActual = 0;
        vidaUI?.Resetear();

        if (transformJugador != null && puntoResetJugador != null)
            transformJugador.position = puntoResetJugador.position;

        yield return new WaitForSeconds(0.5f);
        yield return StartCoroutine(MoverCuadro(2f));

        // Volver a ejecutar desde la escena 0 directamente
        yield return StartCoroutine(EjecutarEscena(_escenaActual));
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Helpers

    private IEnumerator EsperarDialogo(DialogoData dialogo)
    {
        if (dialogo == null) yield break;

        bool terminado = false;
        System.Action handler = () => terminado = true;
        DialogoController.OnDialogoTerminado += handler;
        _dialogoController.Iniciar(dialogo);
        yield return new WaitUntil(() => terminado);
        DialogoController.OnDialogoTerminado -= handler;
    }

    private IEnumerator MostrarTitulo(string texto)
    {
        if (panelTitulo == null) yield break;
        if (textoTitulo != null) textoTitulo.text = texto;
        panelTitulo.SetActive(true);
        yield return new WaitForSeconds(2.5f);
        panelTitulo.SetActive(false);
    }

    private void ConfigurarObjetos(EscenaMisa escena)
    {
        if (escena.activar != null)
            foreach (GameObject obj in escena.activar)
                if (obj != null) obj.SetActive(true);

        if (escena.desactivar != null)
            foreach (GameObject obj in escena.desactivar)
                if (obj != null) obj.SetActive(false);
    }

    private IEnumerator MoverSacerdote(EscenaMisa escena)
    {
        while (Vector3.Distance(sacerdote.position, escena.puntoDestino.position) > 0.05f)
        {
            sacerdote.position = Vector3.MoveTowards(
                sacerdote.position,
                escena.puntoDestino.position,
                escena.velocidadSacerdote * Time.deltaTime
            );
            yield return null;
        }
        sacerdote.position = escena.puntoDestino.position;
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