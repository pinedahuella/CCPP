using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// Datos del panel intermedio de la mano.
/// El jugador elige entre Saludo o Senal.
/// Solo datos, sin logica.
/// </summary>
public class PanelManoData : MonoBehaviour
{
    [Header("Panel")]
    [Tooltip("Panel raíz, se activa al seleccionar ManoDerecha")]
    public GameObject panelMano;

    [Header("Botones")]
    [Tooltip("Botón para lanzar el minijuego de saludo")]
    public Button botonSaludo;

    [Tooltip("Botón para lanzar el minijuego de señal")]
    public Button botonSenal;
}