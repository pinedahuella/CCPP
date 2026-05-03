using UnityEngine;

/// <summary>
/// Al activarse aplica configuración específica al minijuego de responder.
/// </summary>
public class ConfigResponder : MonoBehaviour
{
    [Header("Referencia")]
    public MinijuegoResponderData data;

    [Header("Configuración")]
    public float tiempoLimite = 10f;
    public float anchoBarraInicial = 600f;
    public float alphaAyudaPorEspacio = 0.15f;
    public float aceleracionBarraPorEspacio = 1.5f;
    public int indiceRespuestaCorrecta = 0;

    [Header("Contenido")]
    public string textoBoton0 = "Opción A";
    public string textoBoton1 = "Opción B";
    public string textoBoton2 = "Opción C";
    public string textoAyudaContenido = "La respuesta es...";

    private void OnEnable()
    {
        if (data == null) { Debug.LogWarning("[ConfigResponder] data no asignado."); return; }

        data.tiempoLimite = tiempoLimite;
        data.anchoBarraInicial = anchoBarraInicial;
        data.alphaAyudaPorEspacio = alphaAyudaPorEspacio;
        data.aceleracionBarraPorEspacio = aceleracionBarraPorEspacio;
        data.indiceRespuestaCorrecta = indiceRespuestaCorrecta;
        data.textoAyudaContenido = textoAyudaContenido;

        data.textoBotones = new string[3]
        {
            textoBoton0,
            textoBoton1,
            textoBoton2
        };
    }
}