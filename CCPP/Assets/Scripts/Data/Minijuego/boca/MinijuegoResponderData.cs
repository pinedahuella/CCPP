using UnityEngine;
using UnityEngine.UI;
using TMPro;

/// <summary>
/// Datos del minijuego de responder.
/// Solo datos, sin logica.
/// </summary>
public class MinijuegoResponderData : MonoBehaviour
{
    [Header("Panel")]
    public GameObject panelResponder;

    [Header("Pregunta")]
    [Tooltip("Imagen superior con la pregunta o contexto visual")]
    public Image imagenPregunta;

    [Header("Barra de tiempo")]
    [Tooltip("RectTransform de la barra que se acorta con el tiempo")]
    public RectTransform barraTiempo;
    [Tooltip("Ancho inicial de la barra en píxeles")]
    public float anchoBarraInicial = 600f;

    [Header("Botones de respuesta")]
    public Button boton0;
    public Button boton1;
    public Button boton2;
    public TextMeshProUGUI textoBoton0;
    public TextMeshProUGUI textoBoton1;
    public TextMeshProUGUI textoBoton2;

    [Header("Ayuda")]
    [Tooltip("Texto con la respuesta correcta, tapado por imagenAyuda")]
    public TextMeshProUGUI textoAyuda;
    [Tooltip("Imagen que tapa la respuesta, se transparenta con espacio")]
    public Image imagenAyuda;
    [Tooltip("Cuánto alpha pierde la imagen de ayuda por cada espacio")]
    public float alphaAyudaPorEspacio = 0.15f;
    [Tooltip("Cuánto se acelera la barra por cada espacio usado")]
    public float aceleracionBarraPorEspacio = 1.5f;

    [Header("Configuración")]
    [Tooltip("Tiempo total para responder en segundos")]
    public float tiempoLimite = 10f;

    [Header("Contenido")]
    [Tooltip("Texto de los 3 botones")]
    public string[] textoBotones = new string[3] { "Opción A", "Opción B", "Opción C" };

    [Tooltip("Índice del botón correcto: 0, 1 o 2. Menor a 0 o mayor a 2 = ninguno correcto")]
    public int indiceRespuestaCorrecta = 0;

    [Tooltip("Texto que revela la ayuda")]
    public string textoAyudaContenido = "La respuesta es...";

    [HideInInspector] public float tiempoRestante;
    [HideInInspector] public float multiplicadorVelocidad = 1f;
    [HideInInspector] public bool esperandoRespuesta = false;
}