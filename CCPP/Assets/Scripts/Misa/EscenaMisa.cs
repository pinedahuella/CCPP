using UnityEngine;

/// <summary>
/// Datos de una escena individual de la misa.
/// Serializable para configurar inline en el Inspector del GestorMisa.
/// </summary>
[System.Serializable]
public class EscenaMisa
{
    [Header("Identificación")]
    public string nombreEscena;

    [Tooltip("Si es true muestra el título grande antes del diálogo inicial")]
    public bool mostrarTitulo;
    public string textoTitulo;

    [Header("Diálogos")]
    public DialogoData dialogoInicial;
    public DialogoData dialogoExito;
    public DialogoData dialogoFallo;

    [Header("Misión")]
    public TipoAccion tipoAccion;
    public int valorEsperado;

    [Header("Música")]
    [Tooltip("Si no es null cambia la música al iniciar esta escena")]
    public AudioClip musicaOpcional;

    [Header("Sacerdote")]
    public string animacionSacerdote;
    [Tooltip("Si no es null mueve al sacerdote a este punto")]
    public Transform puntoDestino;
    public float velocidadSacerdote = 2f;

    [Header("Objetos")]
    [Tooltip("Se activan al iniciar la escena")]
    public GameObject[] activar;
    [Tooltip("Se desactivan al iniciar la escena")]
    public GameObject[] desactivar;

    [Header("Sprites del jugador en escena")]
    public GameObject[] visualesJugador;
}