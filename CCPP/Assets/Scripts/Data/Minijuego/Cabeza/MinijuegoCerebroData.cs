using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// Datos del minijuego de cerebro.
/// Solo datos, sin lógica.
/// </summary>
public class MinijuegoCerebroData : MonoBehaviour
{
    [Header("Panel")]
    public GameObject panelCerebro;

    [Header("Cerebro")]
    [Tooltip("Image del cerebro central")]
    public Image imagenCerebro;

    [Tooltip("RectTransform del cerebro para detectar colisión")]
    public RectTransform rectCerebro;

    [Header("Distractores")]
    [Tooltip("Los 4 distractores, cada uno con su Image y RectTransform")]
    public DistractorCerebro[] distractores;

    [Header("Configuración cerebro")]
    [Tooltip("Cuánto alpha pierde por segundo")]
    public float perdidaAlpha = 0.08f;

    [Tooltip("Cuánto alpha gana al presionar espacio")]
    public float gananciaAlpha = 0.3f;

    [Header("Configuración distractores")]
    public float velocidadMin = 60f;
    public float velocidadMax = 160f;

    [Tooltip("Radio de colisión con el cerebro en píxeles")]
    public float radioColision = 50f;

    [Header("Configuración de victoria")]
    [Tooltip("Segundos que debe sobrevivir para ganar")]
    public float tiempoSobrevivir = 15f;

    // ── Estado ────────────────────────────────────────────────────
    [HideInInspector] public float tiempoTranscurrido = 0f;
    [HideInInspector] public bool minijuegoActivo = false;
}