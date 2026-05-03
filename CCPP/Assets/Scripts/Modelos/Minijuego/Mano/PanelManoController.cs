using UnityEngine;

/// <summary>
/// Controlador del panel intermedio de la mano.
/// Muestra dos opciones al jugador: Saludo o Senal.
/// </summary>
[RequireComponent(typeof(PanelManoData))]
public class PanelManoController : MonoBehaviour
{
    private PanelManoData _data;

    /// <summary>Se dispara cuando el jugador elige la opcion Saludo en el panel de mano.</summary>
    public static event System.Action OnSaludoSeleccionado;
    /// <summary>Se dispara cuando el jugador elige la opcion Senal en el panel de mano.</summary>
    public static event System.Action OnSenalSeleccionada;

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

    #region API Pública

    /// <summary>
    /// Abre el panel de mano y configura los botones de Saludo y Senal.
    /// Llamado por MinijuegoManager cuando el jugador selecciona la parte ManoDerecha.
    /// </summary>
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

    /// <summary>
    /// Cierra el panel de mano y limpia los listeners de los botones.
    /// </summary>
    public void CerrarPanel()
    {
        if (_data.panelMano == null) return;
        _data.panelMano.SetActive(false);
        LimpiarBotones();
    }

    #endregion

    #region Botones

    /// <summary>Asigna los listeners a los botones de Saludo y Senal.</summary>
    private void ConfigurarBotones()
    {
        LimpiarBotones();

        if (_data.botonSaludo != null)
            _data.botonSaludo.onClick.AddListener(AlSeleccionarSaludo);

        if (_data.botonSenal != null)
            _data.botonSenal.onClick.AddListener(AlSeleccionarSenal);
    }

    /// <summary>Elimina todos los listeners de los botones de Saludo y Senal.</summary>
    private void LimpiarBotones()
    {
        if (_data.botonSaludo != null)
            _data.botonSaludo.onClick.RemoveAllListeners();

        if (_data.botonSenal != null)
            _data.botonSenal.onClick.RemoveAllListeners();
    }

    /// <summary>Cierra el panel y dispara el evento OnSaludoSeleccionado.</summary>
    private void AlSeleccionarSaludo()
    {
        CerrarPanel();
        OnSaludoSeleccionado?.Invoke();
    }

    /// <summary>Cierra el panel y dispara el evento OnSenalSeleccionada.</summary>
    private void AlSeleccionarSenal()
    {
        CerrarPanel();
        OnSenalSeleccionada?.Invoke();
    }

    #endregion
}