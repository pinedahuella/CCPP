using UnityEngine;
/// <summary>
/// Contenedor de datos del jugador.
/// No contiene lógica, solo expone las variables
/// que JugadorController necesita para operar.
/// </summary>
public class JugadorData : MonoBehaviour
{
    [Header("Movimiento")]
    [Tooltip("Velocidad máxima en unidades/segundo")]
    public float velocidadMaxima = 5f;

    [Tooltip("Qué tan rápido alcanza la velocidad máxima (unidades/s²)")]
    public float aceleracion = 20f;

    [Tooltip("Qué tan rápido frena al soltar el input (unidades/s²)")]
    public float desaceleracion = 30f;

    [Header("Estado (solo lectura)")]
    [Tooltip("Dirección de input detectada este frame")]
    public Vector3 direccionInput = Vector3.zero;

    [Header("Condicion para moverse")]
    [Tooltip("Impide movimiento en ciertas acciones o cuando se desee")]
    public bool puedeMoverse = true;
}