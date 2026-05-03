using UnityEngine;

/// <summary>
/// Al activarse aplica configuracion especifica al minijuego de saludo.
/// </summary>
public class ConfigSaludo : MonoBehaviour
{
    [Header("Referencia")]
    public MinijuegoSaludoData data;

    [Header("Configuracion")]
    public float tiempoLimite = 3f;
    public float tiempoExito = 1.2f;
    public float anchoBarraInicial = 400f;

    /// <summary>
    /// Copia los valores serializados de este Config al MinijuegoSaludoData de referencia.
    /// Se ejecuta cada vez que este GameObject se activa en escena.
    /// </summary>
    private void OnEnable()
    {
        if (data == null) { Debug.LogWarning("[ConfigSaludo] data no asignado."); return; }

        data.tiempoLimite = tiempoLimite;
        data.tiempoExito = tiempoExito;
        data.anchoBarraInicial = anchoBarraInicial;
    }
}