using UnityEngine;

/// <summary>
/// Al activarse aplica configuracion especifica al minijuego de responder.
/// </summary>
public class ConfigResponder : MonoBehaviour
{
    [Header("Referencia")]
    public MinijuegoResponderData data;

    [Header("Configuracion")]
    public float tiempoLimite = 10f;
    public float anchoBarraInicial = 600f;
    public float alphaAyudaPorEspacio = 0.15f;
    public float aceleracionBarraPorEspacio = 1.5f;
    public int indiceRespuestaCorrecta = 0;

    [Header("Contenido")]
    public string textoBoton0 = "Opcion A";
    public string textoBoton1 = "Opcion B";
    public string textoBoton2 = "Opcion C";
    public string textoAyudaContenido = "La respuesta es...";

    /// <summary>
    /// Copia los valores serializados de este Config al MinijuegoResponderData de referencia,
    /// incluyendo el texto de los tres botones y la ayuda.
    /// Se ejecuta cada vez que este GameObject se activa en escena.
    /// </summary>
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