using UnityEngine;

/// <summary>
/// Datos de una linea de dialogo.
/// Struct puro, sin logica.
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