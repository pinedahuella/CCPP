using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// Datos del minijuego de señal.
/// 4 botones que deben presionarse en orden en tiempo limitado.
/// Solo datos, sin lógica.
/// </summary>
public class MinijuegoSenalData : MonoBehaviour
{
    [Header("Panel")]
    public GameObject panelSenal;

    [Header("Botones en orden de aparición en escena")]
    [Tooltip("Los 4 botones de señal")]
    public Button[] botones;

    [Header("Configuración")]
    [Tooltip("Segundos para completar la secuencia")]
    public float tiempoLimite = 5f;

    // ── Estado ────────────────────────────────────────────────────
    [HideInInspector]
    public int indiceActual = 0;

    [HideInInspector]
    public int[] ordenAleatorio = new int[4];
}