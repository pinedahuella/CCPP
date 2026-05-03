using UnityEngine;

/// <summary>
/// Al activarse aplica configuracion especifica al minijuego de cerebro.
/// </summary>
public class ConfigCerebro : MonoBehaviour
{
    [Header("Referencia")]
    public MinijuegoCerebroData data;

    [Header("Configuracion")]
    public float perdidaAlpha = 0.08f;
    public float gananciaAlpha = 0.3f;
    public float velocidadMin = 60f;
    public float velocidadMax = 160f;
    public float radioColision = 50f;
    public float tiempoSobrevivir = 15f;

    /// <summary>
    /// Copia los valores serializados de este Config al MinijuegoCerebroData de referencia.
    /// Se ejecuta cada vez que este GameObject se activa en escena.
    /// </summary>
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