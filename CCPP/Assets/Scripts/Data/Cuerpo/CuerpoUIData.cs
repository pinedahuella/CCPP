using UnityEngine;

/// <summary>
/// Datos de la UI del cuerpo.
/// Expone el panel y el array de partes con sus botones.
/// Sin lógica, solo referencias.
/// </summary>
public class CuerpoUIData : MonoBehaviour
{
    [Header("Panel principal")]
    [Tooltip("Panel que contiene todos los botones de partes del cuerpo")]
    public GameObject panelCuerpo;

    [Header("Partes del cuerpo")]
    [Tooltip("Arrastrar aquí los GameObjects que tengan el componente ParteCuerpoData")]
    public ParteCuerpoData[] partes;

    [Header("Colores de estado")]
    [Tooltip("Color del botón cuando la parte está desbloqueada")]
    public Color colorDesbloqueado = Color.white;

    [Tooltip("Color del botón cuando la parte está bloqueada")]
    public Color colorBloqueado = Color.gray;
}