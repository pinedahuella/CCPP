using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// Datos del minijuego de saludo de mano.
/// Solo datos, sin logica.
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
    public GameObject imagenExito;

    [Header("Barra de tiempo")]
    [Tooltip("RectTransform de la barra que se acorta con el tiempo")]
    public RectTransform barraTiempo;
    [Tooltip("Ancho inicial de la barra en píxeles")]
    public float anchoBarraInicial = 400f;

    [Header("Configuración")]
    public float tiempoLimite = 3f;
    public float tiempoExito = 1.2f;

    [HideInInspector] public bool botonCorrectoEsArriba;
}