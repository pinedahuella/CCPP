using UnityEngine;

/// <summary>
/// Al activarse aplica configuracion especifica al minijuego de pecho.
/// Coloca este script en el mismo GameObject que activas para la mision.
/// </summary>
public class ConfigPecho : MonoBehaviour
{
    [Header("Referencia")]
    public MinijuegoPechoData data;

    [Header("Configuracion")]
    public int rondasTotales = 4;
    public float velocidadMin = 80f;
    public float velocidadMax = 180f;
    public float margenAcierto = 30f;
    public float tamanoInicial = 400f;
    public float tamanoCorazon = 100f;

    /// <summary>
    /// Copia los valores serializados de este Config al MinijuegoPechoData de referencia.
    /// Se ejecuta cada vez que este GameObject se activa en escena.
    /// </summary>
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