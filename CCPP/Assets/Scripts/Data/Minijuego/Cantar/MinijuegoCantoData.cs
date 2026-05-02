using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// Datos del minijuego de canto.
/// Solo datos, sin lógica.
/// </summary>
public class MinijuegoCantoData : MonoBehaviour
{
    [Header("Panel")]
    public GameObject panelCanto;

    [Header("Pools de notas por carril")]
    public NotaCanto[] notasCarril0;
    public NotaCanto[] notasCarril1;
    public NotaCanto[] notasCarril2;
    public NotaCanto[] notasCarril3;

    [Header("Botones de carril (en orden 0-3)")]
    public Button[] botones;

    [Tooltip("Margen Y en píxeles mundiales para considerar acierto")]
    public float margenAcierto = 60f;

    [Header("Configuración de notas")]
    public float velocidadMin = 150f;
    public float velocidadMax = 280f;

    [Tooltip("Píxeles sobre el botón donde aparece la nota")]
    public float posYInicial = 400f;

    [Tooltip("Intervalo en segundos entre aparición de notas")]
    public float intervaloNotas = 1.2f;

    [Header("Configuración de victoria")]
    public int notasParaGanar = 8;
    public int fallosPermitidos = 3;

    // ── Estado ────────────────────────────────────────────────────
    [HideInInspector] public int notasAcertadas = 0;
    [HideInInspector] public int fallosActuales = 0;
    [HideInInspector] public float timerNota = 0f;
    [HideInInspector] public bool minijuegoActivo = false;
}