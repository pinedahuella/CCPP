using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// Datos del minijuego de saludo de mano.
/// Solo datos, sin lógica.
/// </summary>
public class MinijuegoSaludoData : MonoBehaviour
{
    [Header("Panel")]
    public GameObject panelSaludo;

    [Header("Botones")]
    public Button botonArriba;
    public Button botonAbajo;

    [Tooltip("Imagen de la mano del otro personaje (va en el botón correcto aleatorio)")]
    public Image imagenManoOtro;

    [Tooltip("Imagen de tu mano (va en el botón incorrecto)")]
    public Image imagenManoJugador;

    [Header("Imagen de éxito")]
    [Tooltip("Imagen de dos manos dándose, aparece al acertar")]
    public GameObject imagenExito;

    [Header("Configuración")]
    [Tooltip("Segundos para completar el saludo")]
    public float tiempoLimite = 3f;

    [Tooltip("Segundos que se muestra la imagen de éxito antes de cerrar")]
    public float tiempoExito = 1.2f;

    // ── Estado ────────────────────────────────────────────────────
    [HideInInspector]
    public bool botonCorrectoEsArriba;
}