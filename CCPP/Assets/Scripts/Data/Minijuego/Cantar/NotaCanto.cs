using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// Datos y estado de una nota musical que cae en el minijuego de canto.
/// MonoBehaviour, vive en cada GameObject de nota.
/// </summary>
public class NotaCanto : MonoBehaviour
{
    [Tooltip("Image de la nota")]
    public Image imagen;

    [HideInInspector] public int carril;
    [HideInInspector] public float velocidad;
    [HideInInspector] public bool activa = false;


    [Tooltip("Posición inicial de esta nota, asignar manualmente en el Inspector")]
    public Vector2 posicionInicial;

    private RectTransform _rect;

    private void Start()
    {
        _rect = GetComponent<RectTransform>();
    }

    /// <summary>
    /// Activa esta nota en el carril indicado con la velocidad dada,
    /// restaurando su posicion inicial y mostrando su imagen.
    /// </summary>
    /// <param name="carrilAsignado">Indice del carril (0-3) al que pertenece la nota.</param>
    /// <param name="velocidadAsignada">Pixeles por segundo a los que cae la nota.</param>
    public void Activar(int carrilAsignado, float velocidadAsignada)
    {
        if (_rect == null)
            _rect = GetComponent<RectTransform>();

        carril = carrilAsignado;
        velocidad = velocidadAsignada;
        activa = true;
        _rect.anchoredPosition = posicionInicial;

        if (imagen != null)
            imagen.gameObject.SetActive(true);
    }

    /// <summary>
    /// Desactiva esta nota: oculta la imagen y restaura la posicion inicial.
    /// </summary>
    public void Desactivar()
    {
        activa = false;

        if (_rect == null)
            _rect = GetComponent<RectTransform>();

        _rect.anchoredPosition = posicionInicial;

        if (imagen != null)
            imagen.gameObject.SetActive(false);
    }

    /// <summary>Posicion anclada actual del RectTransform de esta nota.</summary>
    public Vector2 PosicionActual => GetComponent<RectTransform>().anchoredPosition;

    /// <summary>
    /// Desplaza la nota hacia abajo en el canvas segun su velocidad y el delta de tiempo.
    /// </summary>
    /// <param name="delta">Time.deltaTime del frame actual.</param>
    public void MoverAbajo(float delta)
    {
        if (_rect == null)
            _rect = GetComponent<RectTransform>();

        _rect.anchoredPosition += Vector2.down * velocidad * delta;
    }
}