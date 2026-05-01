using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// Datos de una parte del cuerpo vinculada a un botón de la UI.
/// MonoBehaviour para poder asignarse como componente en el Inspector.
/// Solo datos, sin lógica.
/// </summary>
public class ParteCuerpoData : MonoBehaviour
{
    [Tooltip("Qué parte del cuerpo representa este componente")]
    public ParteCuerpo parte;

    [Tooltip("Botón de la UI asociado a esta parte")]
    public Button boton;

    [Tooltip("Imagen del botón para feedback visual de bloqueado/desbloqueado")]
    public Image imagenBoton;
}