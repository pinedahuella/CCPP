using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// Datos de una celda de la cuadricula del minijuego de pierna.
/// MonoBehaviour, vive en cada uno de los 9 GameObjects de celda.
/// Sin logica, solo estado y referencias.
/// </summary>
public class CeldaCuadriculaData : MonoBehaviour
{
    [Header("Posición en la grilla (0-2)")]
    [Tooltip("Columna de esta celda en la cuadrícula")]
    public int columna;

    [Tooltip("Fila de esta celda en la cuadrícula")]
    public int fila;

    [Header("Estado")]
    [Tooltip("Parte de la pierna colocada en esta celda. Null si está vacía.")]
    public PartePierna? parteOcupante = null;

    [Header("Referencias UI")]
    [Tooltip("Botón de esta celda para recibir clicks")]
    public Button boton;

    [Tooltip("Imagen que muestra la parte colocada en esta celda")]
    public Image imagenParte;

    [Tooltip("Sprite por defecto de la celda cuando está vacía")]
    public Sprite spriteDefault;

    #region API Pública

    /// <summary>Devuelve true si hay alguna parte de pierna colocada en esta celda.</summary>
    public bool EstaOcupada => parteOcupante.HasValue;

    /// <summary>
    /// Vacia la celda: elimina la parte ocupante y restaura el sprite por defecto.
    /// </summary>
    public void Limpiar()
    {
        parteOcupante = null;
        if (imagenParte != null)
        {
            imagenParte.sprite = spriteDefault;
            imagenParte.gameObject.SetActive(false);
        }
    }

    #endregion
}