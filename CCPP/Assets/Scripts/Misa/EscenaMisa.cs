using UnityEngine;

/// <summary>
/// Datos de una escena individual de la misa.
/// Serializable para configurar inline en el Inspector del GestorMisa.
/// </summary>
[System.Serializable]
public class EscenaMisa
{
    [Header("Identificacion")]
    public string nombreEscena;

    [Tooltip("Si es true muestra el ttulo grande antes del dialogo inicial")]
    public bool mostrarTitulo;
    public string textoTitulo;

    [Header("Dialogos")]
    public DialogoData dialogoInicial;
    public DialogoData dialogoExito;
    public DialogoData dialogoFallo;

    [Header("Mision")]
    public TipoAccion tipoAccion;
    public int valorEsperado;

    [Header("Msica")]
    [Tooltip("Si no es null cambia la msica al iniciar esta escena")]
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