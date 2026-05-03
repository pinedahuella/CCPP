using UnityEngine;

/// <summary>
/// Al activarse aplica configuración específica al minijuego de pecho.
/// Coloca este script en el mismo GameObject que activas para la misión.
/// </summary>
public class ConfigPecho : MonoBehaviour
{
    [Header("Referencia")]
    public MinijuegoPechoData data;

    [Header("Configuración")]
    public int rondasTotales = 4;
    public float velocidadMin = 80f;
    public float velocidadMax = 180f;
    public float margenAcierto = 30f;
    public float tamanoInicial = 400f;
    public float tamanoCorazon = 100f;

    private void OnEnable()
    {
        if (data == null) { Debug.LogWarning("[ConfigPecho] data no asignado."); return; }

        data.rondasTotales = rondasTotales;
        data.velocidadMin = velocidadMin;
        data.velocidadMax = velocidadMax;
        data.margenAcierto = margenAcierto;
        data.tamanoInicial = tamanoInicial;
        data.tamanoCorazon = tamanoCorazon;
    }
}