using UnityEngine;

/// <summary>
/// Muestra los 3 corazones de vida del jugador.
/// Se desactiva uno por cada fallo.
/// </summary>
public class VidaUI : MonoBehaviour
{
    [Tooltip("Los 3 corazones en orden, el último es el primero en perderse")]
    public GameObject[] corazones;

    private int _vidasActuales;

    private void Start()
    {
        Resetear();
    }

    public void Resetear()
    {
        _vidasActuales = corazones.Length;
        foreach (GameObject c in corazones)
            if (c != null) c.SetActive(true);
    }

    public void PerderVida()
    {
        if (_vidasActuales <= 0) return;
        _vidasActuales--;
        corazones[_vidasActuales].SetActive(false);
    }

    public bool SinVidas => _vidasActuales <= 0;
}