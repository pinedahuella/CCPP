using UnityEngine;

/// <summary>
/// Al activarse aplica configuración específica al minijuego de saludo.
/// </summary>
public class ConfigSaludo : MonoBehaviour
{
    [Header("Referencia")]
    public MinijuegoSaludoData data;

    [Header("Configuración")]
    public float tiempoLimite = 3f;
    public float tiempoExito = 1.2f;
    public float anchoBarraInicial = 400f;

    private void OnEnable()
    {
        if (data == null) { Debug.LogWarning("[ConfigSaludo] data no asignado."); return; }

        data.tiempoLimite = tiempoLimite;
        data.tiempoExito = tiempoExito;
        data.anchoBarraInicial = anchoBarraInicial;
    }
}