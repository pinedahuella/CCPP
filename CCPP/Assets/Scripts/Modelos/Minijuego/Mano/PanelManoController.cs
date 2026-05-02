using UnityEngine;

/// <summary>
/// Controlador del panel intermedio de la mano.
/// Muestra dos opciones al jugador: Saludo o Señal.
/// </summary>
[RequireComponent(typeof(PanelManoData))]
public class PanelManoController : MonoBehaviour
{
    // ── Referencias ────────────────────────────────────────────────
    private PanelManoData _data;

    // ── Eventos ───────────────────────────────────────────────────
    public static event System.Action OnSaludoSeleccionado;
    public static event System.Action OnSenalSeleccionada;

    // ──────────────────────────────────────────────────────────────
    #region Unity Callbacks

    private void Awake()
    {
        _data = GetComponent<PanelManoData>();
    }

    private void Start()
    {
        CerrarPanel();
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region API Pública

    public void AbrirPanel()
    {
        if (_data.panelMano == null)
        {
            Debug.LogError("[PanelManoController] panelMano no asignado.");
            return;
        }

        ConfigurarBotones();
        _data.panelMano.SetActive(true);
    }

    public void CerrarPanel()
    {
        if (_data.panelMano == null) return;
        _data.panelMano.SetActive(false);
        LimpiarBotones();
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Botones

    private void ConfigurarBotones()
    {
        LimpiarBotones();

        if (_data.botonSaludo != null)
            _data.botonSaludo.onClick.AddListener(AlSeleccionarSaludo);

        if (_data.botonSenal != null)
            _data.botonSenal.onClick.AddListener(AlSeleccionarSenal);
    }

    private void LimpiarBotones()
    {
        if (_data.botonSaludo != null)
            _data.botonSaludo.onClick.RemoveAllListeners();

        if (_data.botonSenal != null)
            _data.botonSenal.onClick.RemoveAllListeners();
    }

    private void AlSeleccionarSaludo()
    {
        CerrarPanel();
        OnSaludoSeleccionado?.Invoke();
    }

    private void AlSeleccionarSenal()
    {
        CerrarPanel();
        OnSenalSeleccionada?.Invoke();
    }

    #endregion
}