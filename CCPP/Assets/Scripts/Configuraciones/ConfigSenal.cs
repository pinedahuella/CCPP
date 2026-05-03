using UnityEngine;

/// <summary>
/// Al activarse aplica configuración específica al minijuego de señal.
/// </summary>
public class ConfigSenal : MonoBehaviour
{
    [Header("Referencia")]
    public MinijuegoSenalData data;

    [Header("Configuración")]
    public float tiempoLimite = 5f;
    public float anchoBarraInicial = 400f;
    public bool esCompleja = false;

    private void OnEnable()
    {
        if (data == null) { Debug.LogWarning("[ConfigSenal] data no asignado."); return; }

        data.tiempoLimite = tiempoLimite;
        data.anchoBarraInicial = anchoBarraInicial;
        data.esCompleja = esCompleja;
    }
}