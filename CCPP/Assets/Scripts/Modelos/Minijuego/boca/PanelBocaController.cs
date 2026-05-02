using UnityEngine;

/// <summary>
/// Controlador del panel intermedio de la boca.
/// </summary>
[RequireComponent(typeof(PanelBocaData))]
public class PanelBocaController : MonoBehaviour
{
    private PanelBocaData _data;

    public static event System.Action OnResponderSeleccionado;
    public static event System.Action OnCantarSeleccionado;

    private void Awake()
    {
        _data = GetComponent<PanelBocaData>();
    }

    private void Start()
    {
        CerrarPanel();
    }

    public void AbrirPanel()
    {
        if (_data.panelBoca == null) { Debug.LogError("[PanelBocaController] panelBoca no asignado."); return; }
        LimpiarBotones();
        if (_data.botonResponder != null) _data.botonResponder.onClick.AddListener(AlSeleccionarResponder);
        if (_data.botonCantar != null) _data.botonCantar.onClick.AddListener(AlSeleccionarCantar);
        _data.panelBoca.SetActive(true);
    }

    public void CerrarPanel()
    {
        if (_data.panelBoca == null) return;
        _data.panelBoca.SetActive(false);
        LimpiarBotones();
    }

    private void LimpiarBotones()
    {
        if (_data.botonResponder != null) _data.botonResponder.onClick.RemoveAllListeners();
        if (_data.botonCantar != null) _data.botonCantar.onClick.RemoveAllListeners();
    }

    private void AlSeleccionarResponder() { CerrarPanel(); OnResponderSeleccionado?.Invoke(); }
    private void AlSeleccionarCantar() { CerrarPanel(); OnCantarSeleccionado?.Invoke(); }
}