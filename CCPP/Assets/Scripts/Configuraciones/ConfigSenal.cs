using UnityEngine;

/// <summary>
/// Al activarse aplica configuracion especifica al minijuego de senal.
/// </summary>
public class ConfigSenal : MonoBehaviour
{
    [Header("Referencia")]
    public MinijuegoSenalData data;

    [Header("Configuracion")]
    public float tiempoLimite = 5f;
    public float anchoBarraInicial = 400f;
    public bool esCompleja = false;

    /// <summary>
    /// Copia los valores serializados de este Config al MinijuegoSenalData de referencia,
    /// incluyendo el modo simple o complejo.
    /// Se ejecuta cada vez que este GameObject se activa en escena.
    /// </summary>
    private void OnEnable()
    {
        if (data == null) { Debug.LogWarning("[ConfigSenal] data no asignado."); return; }

        data.tiempoLimite = tiempoLimite;
        data.anchoBarraInicial = anchoBarraInicial;
        data.esCompleja = esCompleja;
    }
}