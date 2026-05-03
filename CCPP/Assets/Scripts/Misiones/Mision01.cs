using UnityEngine;

/// <summary>
/// Primera mision del juego.
/// Flujo: dialogo inicial → suscribe mision + activa PENSAMIENTOJUGADOR
/// → si falla: dialogo fallo → vuelve a suscribir + activar
/// → si acierta: dialogo exito → resto de logica a cargo del disenador
/// </summary>
public class Mision01 : MonoBehaviour
{
    [Header("Diálogos")]
    public DialogoData dialogoInicial;
    public DialogoData dialogoFallo;
    public DialogoData dialogoExito;

    [Header("Referencias")]
    public GameObject pensamientoJugador;

    [Header("Lógicas de activación")]
    public JugadorController controladorJugador;
    public AudioSource jugadorAudioSource;
    public GameObject[] VisualesJugador;
    public GameObject[] VisualesJugadorDesactivadas;
    public GameObject BurbujaEspaciadora;

    private DialogoController _dialogoController;

    #region Unity Callbacks

    private void Start()
    {
        _dialogoController = FindFirstObjectByType<DialogoController>();

        if (_dialogoController == null)
        {
            Debug.LogError("[Mision01] No se encontró DialogoController en escena.");
            return;
        }

        DesactivarPensamiento();
        IniciarDialogoInicial();
    }

    #endregion

    #region Flujo de Misión

    /// <summary>Suscribe el handler de fin de dialogo e inicia el dialogo de introduccion.</summary>
    private void IniciarDialogoInicial()
    {
        DialogoController.OnDialogoTerminado += AlTerminarDialogoInicial;
        _dialogoController.Iniciar(dialogoInicial);
    }

    /// <summary>Se llama al terminar el dialogo inicial; desuscribe el handler y activa la mision.</summary>
    private void AlTerminarDialogoInicial()
    {
        DialogoController.OnDialogoTerminado -= AlTerminarDialogoInicial;
        SuscribirMision();
    }

    /// <summary>
    /// Crea y asigna una MisionPosicion de tipo Postura=1 (parado),
    /// activa el pensamiento del jugador y muestra la burbuja de espacio.
    /// </summary>
    private void SuscribirMision()
    {
        MisionPosicion mision = new MisionPosicion(
            TipoAccion.Postura, 1,
            AlAcertar, AlFallar
        );

        if (MisionesGlobal.Instancia == null)
        {
            Debug.LogError("[Mision01] MisionesGlobal no encontrado.");
            return;
        }

        MisionesGlobal.Instancia.AsignarMision(mision);
        ActivarPensamiento();

        if (BurbujaEspaciadora != null)
            BurbujaEspaciadora.SetActive(true);
    }

    /// <summary>Se llama cuando el minijuego reporta un resultado incorrecto; inicia el dialogo de fallo.</summary>
    private void AlFallar()
    {
        DesactivarPensamiento();
        DialogoController.OnDialogoTerminado += AlTerminarDialogoFallo;
        _dialogoController.Iniciar(dialogoFallo);
    }

    /// <summary>Se llama al terminar el dialogo de fallo; vuelve a suscribir la mision para reintentar.</summary>
    private void AlTerminarDialogoFallo()
    {
        DialogoController.OnDialogoTerminado -= AlTerminarDialogoFallo;
        SuscribirMision();
    }

    /// <summary>Se llama cuando el minijuego reporta el resultado correcto; inicia el dialogo de exito.</summary>
    private void AlAcertar()
    {
        DesactivarPensamiento();
        DialogoController.OnDialogoTerminado += AlTerminarDialogoExito;
        _dialogoController.Iniciar(dialogoExito);
    }

    /// <summary>
    /// Se llama al terminar el dialogo de exito; reactiva al jugador,
    /// muestra sus visuales finales y habilita el AudioSource de caminata.
    /// </summary>
    private void AlTerminarDialogoExito()
    {
        DialogoController.OnDialogoTerminado -= AlTerminarDialogoExito;

        if (controladorJugador != null)
            controladorJugador.enabled = true;

        foreach (var item in VisualesJugador)
            if (item != null) item.SetActive(true);

        foreach (var item in VisualesJugadorDesactivadas)
            if (item != null) item.SetActive(false);

        if (jugadorAudioSource != null)
            jugadorAudioSource.enabled = true;
    }

    #endregion

    #region Helpers

    /// <summary>Activa el panel de pensamiento del jugador para indicarle que debe elegir una postura.</summary>
    private void ActivarPensamiento()
    {
        if (pensamientoJugador != null)
            pensamientoJugador.SetActive(true);
    }

    /// <summary>Desactiva el panel de pensamiento del jugador.</summary>
    private void DesactivarPensamiento()
    {
        if (pensamientoJugador != null)
            pensamientoJugador.SetActive(false);
    }

    #endregion
}