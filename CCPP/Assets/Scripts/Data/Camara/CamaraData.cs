using UnityEngine;

/// <summary>
/// Contenedor de datos de la camara principal del juego.
/// Expone el objetivo a seguir y la velocidad de suavizado.
/// Sin logica, solo referencias que CamaraController consume.
/// </summary>
public class CamaraData : MonoBehaviour
{
    /// <summary>Transform del jugador que la camara sigue horizontalmente.</summary>
    [Header("Objetivo")]
    public Transform jugador;

    /// <summary>Factor de suavizado Lerp aplicado cada frame en LateUpdate.</summary>
    [Header("Configuracion")]
    public float velocidadSmooth = 5f;

    /// <summary>Si es false la camara deja de seguir al jugador (util en cinematicas).</summary>
    [Header("Estado")]
    public bool seguirJugador = true;
}