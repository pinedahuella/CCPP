using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// Datos del minijuego de pierna.
/// Sin lógica, solo referencias y estado.
/// </summary>
public class MinijuegoPiernaData : MonoBehaviour
{
    [Header("Panel raíz")]
    [Tooltip("Panel completo del minijuego, se activa al iniciar")]
    public GameObject panelMinijuego;

    [Header("Cuadrícula")]
    [Tooltip("Las 9 celdas de la cuadrícula, asignar en orden de izquierda a derecha, arriba a abajo")]
    public CeldaCuadriculaData[] celdas;

    [Header("Imágenes de orden (panel lateral)")]
    [Tooltip("Imagen del slot 1 del panel de orden")]
    public Image imagenOrden1;
    [Tooltip("Imagen del slot 2 del panel de orden")]
    public Image imagenOrden2;
    [Tooltip("Imagen del slot 3 del panel de orden")]
    public Image imagenOrden3;

    [Header("Sprites de cada parte")]
    [Tooltip("Sprite visual de la cadera")]
    public Sprite spriteCadera;
    [Tooltip("Sprite visual de la rodilla")]
    public Sprite spriteRodilla;
    [Tooltip("Sprite visual del pie")]
    public Sprite spritePie;

    [Header("Conexiones")]
    [Tooltip("Imagen de línea entre cadera y rodilla")]
    public Image lineaCaderaRodilla;
    [Tooltip("Imagen de línea entre rodilla y pie")]
    public Image lineaRodillaPie;

    [Header("Configuración")]
    [Tooltip("Segundos de espera antes de reportar el resultado")]
    public float tiempoEspera = 1.2f;

    // ── Estado interno (solo lectura desde el Inspector) ───────────
    [Header("Estado (solo lectura)")]
    [Tooltip("Índice de la parte que toca colocar ahora (0=primera del orden)")]
    public int turnoActual = 0;

    [Tooltip("Orden aleatorio generado al iniciar")]
    public PartePierna[] ordenAleatorio = new PartePierna[3];

    // ──────────────────────────────────────────────────────────────
    #region Helpers

    /// <summary>
    /// Devuelve el sprite correspondiente a una parte.
    /// </summary>
    public Sprite ObtenerSprite(PartePierna parte)
    {
        switch (parte)
        {
            case PartePierna.Cadera: return spriteCadera;
            case PartePierna.Rodilla: return spriteRodilla;
            case PartePierna.Pie: return spritePie;
            default:
                Debug.LogWarning($"[MinijuegoPiernaData] Parte no reconocida: {parte}");
                return null;
        }
    }

    /// <summary>
    /// Devuelve la imagen del slot de orden según índice (0,1,2).
    /// </summary>
    public Image ObtenerImagenOrden(int indice)
    {
        switch (indice)
        {
            case 0: return imagenOrden1;
            case 1: return imagenOrden2;
            case 2: return imagenOrden3;
            default:
                Debug.LogWarning($"[MinijuegoPiernaData] Índice de orden fuera de rango: {indice}");
                return null;
        }
    }

    #endregion
}