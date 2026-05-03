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

    private int _escenaActual = 0;
    private bool _jugadorDentro = false;
    private bool _enFlujo = false;
    private DialogoController _dialogoController;

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

    #region Flujo Principal

    /// <summary>
    /// Arranca el flujo completo de la misa: bloquea movimiento, oculta al jugador
    /// y ejecuta la primera escena.
    /// </summary>
    private IEnumerator IniciarFlujo()
    {
        _enFlujo = true;
        if (indicadorSpace != null) indicadorSpace.SetActive(false);
        if (visualJugadorReal != null) visualJugadorReal.SetActive(false);
        if (jugadorData != null) jugadorData.puedeMoverse = false;

        yield return StartCoroutine(EjecutarEscena(_escenaActual));
    }

    /// <summary>
    /// Ejecuta la escena de la misa en el indice dado: configura objetos, musica,
    /// animacion del sacerdote, titulo y dialogo inicial antes de esperar la mision.
    /// </summary>
    /// <param name="indice">Indice de la escena dentro del array de escenas.</param>
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

    /// <summary>
    /// Muestra los visuales del jugador, crea y asigna la mision de postura
    /// y espera hasta recibir el resultado antes de continuar al acierto o fallo.
    /// </summary>
    /// <param name="escena">Escena actual cuya mision se va a ejecutar.</param>
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

    /// <summary>
    /// Muestra el dialogo de exito y avanza a la siguiente escena de la misa.
    /// </summary>
    /// <param name="escena">Escena que el jugador acabo de completar correctamente.</param>
    private IEnumerator AlAcertar(EscenaMisa escena)
    {
        yield return StartCoroutine(EsperarDialogo(escena.dialogoExito));
        _escenaActual++;
        yield return StartCoroutine(EjecutarEscena(_escenaActual));
    }

    /// <summary>
    /// Muestra el dialogo de fallo, baja la cortina negra, reposiciona al jugador
    /// y reintenta la escena actual.
    /// </summary>
    /// <param name="escena">Escena en la que el jugador fallo.</param>
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

    #region Ganar / Reiniciar

    /// <summary>
    /// Activa el objeto de comunion, oculta la barra de vidas,
    /// devuelve el control al jugador y termina el flujo de la misa.
    /// </summary>
    private IEnumerator Ganar()
    {
        if (objetoGanar != null) objetoGanar.SetActive(true);
        if (vidaUI != null) vidaUI.gameObject.SetActive(false);

        if (jugadorData != null) jugadorData.puedeMoverse = true;
        if (visualJugadorReal != null) visualJugadorReal.SetActive(true);

        _enFlujo = false;
        yield break;
    }

    /// <summary>
    /// Reinicia el flujo completo de la misa: resetea vidas y escenas,
    /// reposiciona al jugador y vuelve a ejecutar desde la escena 0.
    /// </summary>
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

    #region Helpers

    /// <summary>
    /// Inicia un dialogo y espera hasta que el DialogoController dispare OnDialogoTerminado.
    /// No hace nada si el dialogo es null.
    /// </summary>
    /// <param name="dialogo">Datos del dialogo a reproducir.</param>
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

    /// <summary>
    /// Muestra el panel de titulo con el texto indicado durante 2.5 segundos y luego lo oculta.
    /// </summary>
    /// <param name="texto">Texto del titulo de la escena a mostrar.</param>
    private IEnumerator MostrarTitulo(string texto)
    {
        if (panelTitulo == null) yield break;
        if (textoTitulo != null) textoTitulo.text = texto;
        panelTitulo.SetActive(true);
        yield return new WaitForSeconds(2.5f);
        panelTitulo.SetActive(false);
    }

    /// <summary>
    /// Activa e inactiva los GameObjects configurados en la escena de la misa.
    /// </summary>
    /// <param name="escena">Escena cuya lista de objetos se va a procesar.</param>
    private void ConfigurarObjetos(EscenaMisa escena)
    {
        if (escena.activar != null)
            foreach (GameObject obj in escena.activar)
                if (obj != null) obj.SetActive(true);

        if (escena.desactivar != null)
            foreach (GameObject obj in escena.desactivar)
                if (obj != null) obj.SetActive(false);
    }

    /// <summary>
    /// Mueve al sacerdote hacia el punto de destino de la escena a velocidad constante.
    /// </summary>
    /// <param name="escena">Escena que contiene el punto destino y la velocidad del sacerdote.</param>
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

    /// <summary>
    /// Mueve el cuadro negro suavemente hasta la posicion Y indicada para crear transiciones cinematicas.
    /// Y = 0 lo baja (pantalla negra), Y = 2 lo sube (revela la escena).
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