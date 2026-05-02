using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// Datos del panel intermedio de la boca.
/// El jugador elige entre Responder o Cantar.
/// Solo datos, sin lógica.
/// </summary>
public class PanelBocaData : MonoBehaviour
{
    [Header("Panel")]
    public GameObject panelBoca;

    [Header("Botones")]
    public Button botonResponder;
    public Button botonCantar;
}