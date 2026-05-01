using UnityEngine;

/// <summary>
/// Datos de una línea de diálogo.
/// Struct puro, sin lógica.
/// </summary>
[System.Serializable]
public struct DialogoLinea
{
    [Tooltip("Texto de esta línea de diálogo")]
    [TextArea]
    public string texto;

    [Tooltip("Imagen del personaje que habla")]
    public Sprite imagen;

    [Tooltip("Si es true la imagen aparece a la izquierda, si es false a la derecha")]
    public bool esIzquierda;
}