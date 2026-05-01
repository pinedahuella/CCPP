using UnityEngine;

/// <summary>
/// Datos de la transición de zona.
/// Sin lógica, solo referencias y configuración.
/// </summary>
public class TransicionZonaData : MonoBehaviour
{
    [Header("Cuadro negro")]
    [Tooltip("Transform del cuadro negro hijo de la cámara")]
    public Transform cuadroNegro;

    [Tooltip("Velocidad a la que sube y baja el cuadro negro")]
    public float velocidadTransicion = 2f;

    [Header("Zonas")]
    [Tooltip("GameObject de la nueva zona a activar")]
    public GameObject zonaEntrada;

    [Tooltip("GameObject de la zona anterior a desactivar")]
    public GameObject zonaSalida;

    [Header("Puntos de destino")]
    [Tooltip("Punto donde se teletransporta el jugador")]
    public Transform puntoJugador;

    [Tooltip("Punto donde se teletransporta la cámara")]
    public Transform puntoCamara;

    [Header("Referencias")]
    [Tooltip("Transform de la cámara principal")]
    public Transform camara;
}