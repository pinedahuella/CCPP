using UnityEngine;

/// <summary>
/// Contenedor de una conversación completa.
/// MonoBehaviour para poder asignarse en el Inspector.
/// Solo datos, sin lógica.
/// </summary>
public class DialogoData : MonoBehaviour
{
    [Tooltip("Lista de líneas de esta conversación en orden")]
    public DialogoLinea[] lineas;
}