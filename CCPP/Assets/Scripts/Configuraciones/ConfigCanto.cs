using UnityEngine;

/// <summary>
/// Al activarse aplica configuracion especifica al minijuego de canto.
/// </summary>
public class ConfigCanto : MonoBehaviour
{
    [Header("Referencia")]
    public MinijuegoCantoData data;

    [Header("Configuracion")]
    public float velocidadMin = 150f;
    public float velocidadMax = 280f;
    public float posYInicial = 400f;
    public float intervaloNotas = 1.2f;
    public float margenAcierto = 60f;
    public int notasParaGanar = 8;
    public int fallosPermitidos = 3;

    /// <summary>
    /// Copia los valores serializados de este Config al MinijuegoCantoData de referencia.
    /// Se ejecuta cada vez que este GameObject se activa en escena.
    /// </summary>
    private void OnEnable()
    {
        if (data == null) { Debug.LogWarning("[ConfigCanto] data no asignado."); return; }

        data.velocidadMin = velocidadMin;
        data.velocidadMax = velocidadMax;
        data.posYInicial = posYInicial;
        data.intervaloNotas = intervaloNotas;
        data.margenAcierto = margenAcierto;
        data.notasParaGanar = notasParaGanar;
        data.fallosPermitidos = fallosPermitidos;
    }
}