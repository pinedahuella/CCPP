using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// Datos y estado de un distractor individual del minijuego de cerebro.
/// MonoBehaviour, vive en cada GameObject distractor.
/// </summary>
public class DistractorCerebro : MonoBehaviour
{
    [Tooltip("Image del distractor")]
    public Image imagen;

    [Tooltip("Botón para que el jugador pueda hacer click")]
    public Button boton;

    // ── Estado ────────────────────────────────────────────────────
    [HideInInspector] public Vector2 posicionOriginal;
    [HideInInspector] public float velocidadActual;
    [HideInInspector] public bool activo = false;

    private void Awake()
    {
        // Forzamos a que el RectTransform se asiente si está dentro de un LayoutGroup
        Canvas.ForceUpdateCanvases();
        posicionOriginal = GetComponent<RectTransform>().anchoredPosition;
    }

    /// <summary>
    /// Resetea el distractor a su posición original con nueva velocidad.
    /// </summary>
    public void Resetear(float nuevaVelocidad)
    {
        GetComponent<RectTransform>().anchoredPosition = posicionOriginal;
        velocidadActual = nuevaVelocidad;
        activo = true;

        if (imagen != null)
            imagen.gameObject.SetActive(true);
    }

    /// <summary>
    /// Vuelve a posición original al ser clickeado.
    /// </summary>
    public void AlClickear(float velocidadMin, float velocidadMax)
    {
        Resetear(Random.Range(velocidadMin, velocidadMax));
    }
}