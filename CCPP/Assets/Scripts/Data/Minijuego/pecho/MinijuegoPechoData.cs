using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// Datos del minijuego de ritmo del pecho.
/// Solo datos, sin lógica.
/// </summary>
public class MinijuegoPechoData : MonoBehaviour
{
    [Header("Panel")]
    public GameObject panelPecho;

    [Header("Visual")]
    [Tooltip("RectTransform del círculo externo que se achica")]
    public RectTransform circuloExterno;

    [Tooltip("RectTransform del corazón fijo en el centro")]
    public RectTransform corazon;

    [Tooltip("Botón del corazón que el jugador presiona")]
    public Button botonCorazon;

    [Header("Configuración de rondas")]
    [Tooltip("Cuántas veces debe acertar para ganar")]
    public int rondasTotales = 4;

    [Tooltip("Tamaño inicial del círculo externo")]
    public float tamanoInicial = 400f;

    [Tooltip("Tamaño del corazón fijo (referencia para comparar)")]
    public float tamanoCorazon = 100f;

    [Tooltip("Margen de tolerancia para considerar acierto")]
    public float margenAcierto = 30f;

    [Tooltip("Velocidad mínima de achicamiento")]
    public float velocidadMin = 80f;

    [Tooltip("Velocidad máxima de achicamiento")]
    public float velocidadMax = 180f;

    // ── Estado ────────────────────────────────────────────────────
    [HideInInspector] public int rondaActual = 0;
    [HideInInspector] public float tamanoActual = 0f;
    [HideInInspector] public float velocidadActual = 0f;
    [HideInInspector] public bool esperandoClick = false;
}