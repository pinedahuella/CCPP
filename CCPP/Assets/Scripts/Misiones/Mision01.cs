using UnityEngine;

/// <summary>
/// Primera misión del juego.
/// Flujo: diálogo inicial → suscribe misión + activa PENSAMIENTOJUGADOR
/// → si falla: diálogo fallo → vuelve a suscribir + activar
/// → si acierta: diálogo éxito → resto de lógica a cargo del diseñador
/// </summary>
public class Mision01 : MonoBehaviour
{
    // ── Referencias ────────────────────────────────────────────────
    [Header("Diálogos")]
    [Tooltip("Diálogo que se muestra al iniciar la misión")]
    public DialogoData dialogoInicial;

    [Tooltip("Diálogo que se muestra si el jugador falla")]
    public DialogoData dialogoFallo;

    [Tooltip("Diálogo que se muestra si el jugador acierta")]
    public DialogoData dialogoExito;

    [Header("Referencias")]
    [Tooltip("GameObject PENSAMIENTOJUGADOR con el TriggerCuerpoUI")]
    public GameObject pensamientoJugador;

    [Header("Logicas DE activacion")]
    [Tooltip("al finalizar de forma correcta")]
    public JugadorController controladorJugador;
    public GameObject[] VisualesJugador;

    // ── Controlador de diálogo ─────────────────────────────────────
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
        if (!ValidarDialogo(dialogoInicial, "dialogoInicial")) return;

        DialogoController.OnDialogoTerminado += AlTerminarDialogoInicial;
        _dialogoController.Iniciar(dialogoInicial);
    }

    private void AlTerminarDialogoInicial()
    {
        DialogoController.OnDialogoTerminado -= AlTerminarDialogoInicial;
        SuscribirMision();
    }

    // ──────────────────────────────────────────────────────────────

    private void SuscribirMision()
    {
        MisionPosicion mision = new MisionPosicion(
            TipoAccion.Postura,
            1, // parado
            AlAcertar,
            AlFallar
        );

        if (MisionesGlobal.Instancia == null)
        {
            Debug.LogError("[Mision01] MisionesGlobal no encontrado.");
            return;
        }

        MisionesGlobal.Instancia.AsignarMision(mision);
        ActivarPensamiento();
    }

    // ──────────────────────────────────────────────────────────────

    private void AlFallar()
    {
        DesactivarPensamiento();

        if (!ValidarDialogo(dialogoFallo, "dialogoFallo")) return;

        DialogoController.OnDialogoTerminado += AlTerminarDialogoFallo;
        _dialogoController.Iniciar(dialogoFallo);
    }

    private void AlTerminarDialogoFallo()
    {
        DialogoController.OnDialogoTerminado -= AlTerminarDialogoFallo;
        SuscribirMision();
    }

    // ──────────────────────────────────────────────────────────────

    private void AlAcertar()
    {
        DesactivarPensamiento();

        if (!ValidarDialogo(dialogoExito, "dialogoExito")) return;

        DialogoController.OnDialogoTerminado += AlTerminarDialogoExito;
        _dialogoController.Iniciar(dialogoExito);
    }

    private void AlTerminarDialogoExito()
    {
        DialogoController.OnDialogoTerminado -= AlTerminarDialogoExito;
        // Resto de lógica a cargo del diseñador

        controladorJugador.enabled = true;
        foreach (var item in VisualesJugador)
        {
            item.SetActive(true);
        }
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Helpers

    private void ActivarPensamiento()
    {
        if (pensamientoJugador == null)
        {
            Debug.LogWarning("[Mision01] pensamientoJugador no asignado.");
            return;
        }
        pensamientoJugador.SetActive(true);
    }

    private void DesactivarPensamiento()
    {
        if (pensamientoJugador == null) return;
        pensamientoJugador.SetActive(false);
    }

    private bool ValidarDialogo(DialogoData dialogo, string nombre)
    {
        if (dialogo == null)
        {
            Debug.LogWarning($"[Mision01] {nombre} no asignado.");
            return false;
        }
        return true;
    }

    #endregion
}