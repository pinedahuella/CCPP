using UnityEngine;

public class CamaraData : MonoBehaviour
{
    [Header("Objetivo")]
    public Transform jugador;

    [Header("Configuración")]
    public float velocidadSmooth = 5f;

    [Header("Estado")]
    public bool seguirJugador = true;
}