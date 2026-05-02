using UnityEngine;

/// <summary>
/// Primera misión del juego.
/// Flujo: diálogo inicial → suscribe misión + activa PENSAMIENTOJUGADOR
/// → si falla: diálogo fallo → vuelve a suscribir + activar
/// → si acierta: diálogo éxito → resto de lógica a cargo del diseñador
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

    // ──────────────────────────────────────────────────────────────
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

    // ──────────────────────────────────────────────────────────────
    #region Flujo de Misión

    private void IniciarDialogoInicial()
    {
        DialogoController.OnDialogoTerminado += AlTerminarDialogoInicial;
        _dialogoController.Iniciar(dialogoInicial);
    }

    private void AlTerminarDialogoInicial()
    {
        DialogoController.OnDialogoTerminado -= AlTerminarDialogoInicial;
        SuscribirMision();
    }

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

    private void AlFallar()
    {
        DesactivarPensamiento();
        DialogoController.OnDialogoTerminado += AlTerminarDialogoFallo;
        _dialogoController.Iniciar(dialogoFallo);
    }

    private void AlTerminarDialogoFallo()
    {
        DialogoController.OnDialogoTerminado -= AlTerminarDialogoFallo;
        SuscribirMision();
    }

    private void AlAcertar()
    {
        DesactivarPensamiento();
        DialogoController.OnDialogoTerminado += AlTerminarDialogoExito;
        _dialogoController.Iniciar(dialogoExito);
    }

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

    // ──────────────────────────────────────────────────────────────
    #region Helpers

    private void ActivarPensamiento()
    {
        if (pensamientoJugador != null)
            pensamientoJugador.SetActive(true);
    }

    private void DesactivarPensamiento()
    {
        if (pensamientoJugador != null)
            pensamientoJugador.SetActive(false);
    }

    #endregion
}