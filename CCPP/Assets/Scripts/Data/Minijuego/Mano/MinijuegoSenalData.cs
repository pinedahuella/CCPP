using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// Datos del minijuego de señal.
/// Soporta modo simple (4 botones) y modo complejo (más botones).
/// Solo datos, sin lógica.
/// </summary>
public class MinijuegoSenalData : MonoBehaviour
{
    [Header("Panel")]
    public GameObject panelSenal;

    [Header("Barra de tiempo")]
    public RectTransform barraTiempo;
    public float anchoBarraInicial = 400f;

    [Header("Modo Simple")]
    [Tooltip("Los 4 botones del modo simple")]
    public Button[] botones;
    [Tooltip("GameObjects del modo simple, se desactivan en modo complejo")]
    public GameObject[] objetosSimple;

    [Header("Modo Complejo")]
    [Tooltip("Si true usa los botones complejos en lugar de los simples")]
    public bool esCompleja = false;
    [Tooltip("Los botones del modo complejo (pueden ser más de 4)")]
    public Button[] botonesComplejos;
    [Tooltip("GameObjects del modo complejo, se activan solo en modo complejo")]
    public GameObject[] objetosComplejos;

    [Header("Configuración")]
    public float tiempoLimite = 5f;

    // ── Estado ────────────────────────────────────────────────────
    [HideInInspector] public int indiceActual = 0;
    [HideInInspector] public int[] ordenAleatorio = new int[4];
}