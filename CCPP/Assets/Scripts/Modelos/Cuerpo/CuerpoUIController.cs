using UnityEngine;

/// <summary>
/// Controlador de la UI del cuerpo.
/// Abre el panel al llamarse desde el trigger del jugador,
/// activa o desactiva botones según las habilidades desbloqueadas,
/// y notifica qué parte fue seleccionada.
/// </summary>
[RequireComponent(typeof(CuerpoUIData))]
public class CuerpoUIController : MonoBehaviour
{
    // ── Referencias ────────────────────────────────────────────────
    private CuerpoUIData _data;
    private JugadorHabilidadesData _habilidades;

    // ── Evento ────────────────────────────────────────────────────
    /// <summary>
    /// Se dispara cuando el jugador selecciona una parte del cuerpo.
    /// El minijuego correspondiente se suscribe a este evento.
    /// </summary>
    public static event System.Action<ParteCuerpo> OnParteSeleccionada;

    // ──────────────────────────────────────────────────────────────
    #region Unity Callbacks

    private void Awake()
    {
        ObtenerReferencias();
    }

    private void Start()
    {
        ValidarReferencias();
        CerrarPanel();
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Inicialización

    private void ObtenerReferencias()
    {
        _data = GetComponent<CuerpoUIData>();
        _habilidades = FindFirstObjectByType<JugadorHabilidadesData>();
    }

    private void ValidarReferencias()
    {
        if (_data.panelCuerpo == null)
            Debug.LogError("[CuerpoUIController] panelCuerpo no asignado en CuerpoUIData.");

        if (_habilidades == null)
            Debug.LogError("[CuerpoUIController] No se encontró JugadorHabilidadesData en escena.");

        if (_data.partes == null || _data.partes.Length == 0)
            Debug.LogError("[CuerpoUIController] El array de partes está vacío en CuerpoUIData.");
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region API Pública

    /// <summary>
    /// Abre el panel y configura los botones según las habilidades del jugador.
    /// Llamado por el trigger del jugador al recibir click.
    /// </summary>
    public void AbrirPanel()
    {
        if (_data.panelCuerpo == null || _habilidades == null)
        {
            Debug.LogWarning("[CuerpoUIController] No se puede abrir el panel: referencias faltantes.");
            return;
        }

        ConfigurarBotones();
        _data.panelCuerpo.SetActive(true);
    }

    /// <summary>
    /// Cierra el panel y limpia los listeners de los botones.
    /// </summary>
    public void CerrarPanel()
    {
        if (_data.panelCuerpo == null)
            return;

        _data.panelCuerpo.SetActive(false);
        LimpiarBotones();
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Botones

    /// <summary>
    /// Recorre el array de partes, activa o desactiva cada botón
    /// según el estado de habilidades del jugador, y asigna listeners.
    /// </summary>
    private void ConfigurarBotones()
    {
        if (_data.partes == null)
            return;

        foreach (ParteCuerpoData entrada in _data.partes)
        {
            if (entrada == null || entrada.boton == null)
            {
                Debug.LogWarning("[CuerpoUIController] Entrada de parte o botón nulo. Revisar Inspector.");
                continue;
            }

            bool desbloqueada = _habilidades.EstaDesbloqueada(entrada.parte);

            entrada.boton.interactable = desbloqueada;

            if (entrada.imagenBoton != null)
                entrada.imagenBoton.color = desbloqueada ? _data.colorDesbloqueado : _data.colorBloqueado;

            entrada.boton.onClick.RemoveAllListeners();

            if (desbloqueada)
            {
                ParteCuerpo parteCapturada = entrada.parte;
                entrada.boton.onClick.AddListener(() => AlSeleccionarParte(parteCapturada));
            }
        }
    }

    private void LimpiarBotones()
    {
        if (_data.partes == null)
            return;

        foreach (ParteCuerpoData entrada in _data.partes)
        {
            if (entrada != null && entrada.boton != null)
                entrada.boton.onClick.RemoveAllListeners();
        }
    }

    private void AlSeleccionarParte(ParteCuerpo parte)
    {
        CerrarPanel();
        OnParteSeleccionada?.Invoke(parte);
    }

    #endregion
}