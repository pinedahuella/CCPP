using UnityEngine;

/// <summary>
/// Vive en la Sphere hija del jugador.
/// Al presionar Espacio, avisa a CuerpoUIController que abra el panel.
/// </summary>
public class TriggerCuerpoUI : MonoBehaviour
{
    // ── Referencias ────────────────────────────────────────────────
    private CuerpoUIController _uiController;

    // ──────────────────────────────────────────────────────────────
    #region Unity Callbacks

    private void Awake()
    {
        ObtenerReferencias();
    }

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
            AbrirUI();
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Inicialización

    private void ObtenerReferencias()
    {
        _uiController = FindFirstObjectByType<CuerpoUIController>();

        if (_uiController == null)
            Debug.LogError("[TriggerCuerpoUI] No se encontró CuerpoUIController en escena.");
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Lógica

    private void AbrirUI()
    {
        if (_uiController == null)
        {
            Debug.LogWarning("[TriggerCuerpoUI] No hay CuerpoUIController. No se puede abrir el panel.");
            return;
        }

        _uiController.AbrirPanel();
        gameObject.SetActive(false);   
    }

    #endregion
}