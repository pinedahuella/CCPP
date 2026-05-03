using UnityEngine;

/// <summary>
/// Muestra los 3 corazones de vida del jugador.
/// Se desactiva uno por cada fallo.
/// </summary>
public class VidaUI : MonoBehaviour
{
    [Tooltip("Los 3 corazones en orden, el ultimo es el primero en perderse")]
    public GameObject[] corazones;

    private int _vidasActuales;

    private void Start()
    {
        Resetear();
    }

    /// <summary>
    /// Restaura todos los corazones a su estado visible y reinicia el contador de vidas.
    /// </summary>
    public void Resetear()
    {
        _vidasActuales = corazones.Length;
        foreach (GameObject c in corazones)
            if (c != null) c.SetActive(true);
    }

    /// <summary>
    /// Descuenta una vida y desactiva el corazon correspondiente.
    /// No hace nada si ya no quedan vidas.
    /// </summary>
    public void PerderVida()
    {
        if (_vidasActuales <= 0) return;
        _vidasActuales--;
        corazones[_vidasActuales].SetActive(false);
    }

    /// <summary>True cuando el jugador ha perdido todas sus vidas.</summary>
    public bool SinVidas => _vidasActuales <= 0;
}