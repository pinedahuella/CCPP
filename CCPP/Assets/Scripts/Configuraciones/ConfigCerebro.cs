using UnityEngine;

/// <summary>
/// Al activarse aplica configuración específica al minijuego de cerebro.
/// </summary>
public class ConfigCerebro : MonoBehaviour
{
    [Header("Referencia")]
    public MinijuegoCerebroData data;

    [Header("Configuración")]
    public float perdidaAlpha = 0.08f;
    public float gananciaAlpha = 0.3f;
    public float velocidadMin = 60f;
    public float velocidadMax = 160f;
    public float radioColision = 50f;
    public float tiempoSobrevivir = 15f;

    private void OnEnable()
    {
        if (data == null) { Debug.LogWarning("[ConfigCerebro] data no asignado."); return; }

        data.perdidaAlpha = perdidaAlpha;
        data.gananciaAlpha = gananciaAlpha;
        data.velocidadMin = velocidadMin;
        data.velocidadMax = velocidadMax;
        data.radioColision = radioColision;
        data.tiempoSobrevivir = tiempoSobrevivir;
    }
}