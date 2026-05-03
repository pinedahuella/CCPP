using UnityEngine;

/// <summary>
/// Controlador del panel intermedio de la boca.
/// </summary>
[RequireComponent(typeof(PanelBocaData))]
public class PanelBocaController : MonoBehaviour
{
    private PanelBocaData _data;

    /// <summary>Se dispara cuando el jugador elige la opcion Responder en el panel de boca.</summary>
    public static event System.Action OnResponderSeleccionado;
    /// <summary>Se dispara cuando el jugador elige la opcion Cantar en el panel de boca.</summary>
    public static event System.Action OnCantarSeleccionado;

    private void Awake()
    {
        _data = GetComponent<PanelBocaData>();
    }

    private void Start()
    {
        CerrarPanel();
    }

    /// <summary>
    /// Abre el panel de boca y configura los botones de Responder y Cantar.
    /// Llamado por MinijuegoManager cuando el jugador selecciona la parte Boca.
    /// </summary>
    public void AbrirPanel()
    {
        if (_data.panelBoca == null) { Debug.LogError("[PanelBocaController] panelBoca no asignado."); return; }
        LimpiarBotones();
        if (_data.botonResponder != null) _data.botonResponder.onClick.AddListener(AlSeleccionarResponder);
        if (_data.botonCantar != null) _data.botonCantar.onClick.AddListener(AlSeleccionarCantar);
        _data.panelBoca.SetActive(true);
    }

    /// <summary>
    /// Cierra el panel de boca y limpia los listeners de los botones.
    /// </summary>
    public void CerrarPanel()
    {
        if (_data.panelBoca == null) return;
        _data.panelBoca.SetActive(false);
        LimpiarBotones();
    }

    /// <summary>Elimina todos los listeners de los botones Responder y Cantar.</summary>
    private void LimpiarBotones()
    {
        if (_data.botonResponder != null) _data.botonResponder.onClick.RemoveAllListeners();
        if (_data.botonCantar != null) _data.botonCantar.onClick.RemoveAllListeners();
    }

    /// <summary>Cierra el panel y dispara el evento OnResponderSeleccionado.</summary>
    private void AlSeleccionarResponder() { CerrarPanel(); OnResponderSeleccionado?.Invoke(); }
    /// <summary>Cierra el panel y dispara el evento OnCantarSeleccionado.</summary>
    private void AlSeleccionarCantar() { CerrarPanel(); OnCantarSeleccionado?.Invoke(); }
}