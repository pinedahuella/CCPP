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

    // ── Estado ────────────────────────────────────────────────────
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

    public void Desactivar()
    {
        activa = false;

        if (_rect == null)
            _rect = GetComponent<RectTransform>();

        _rect.anchoredPosition = posicionInicial;

        if (imagen != null)
            imagen.gameObject.SetActive(false);
    }

    public Vector2 PosicionActual => GetComponent<RectTransform>().anchoredPosition;

    public void MoverAbajo(float delta)
    {
        if (_rect == null)
            _rect = GetComponent<RectTransform>();

        _rect.anchoredPosition += Vector2.down * velocidad * delta;
    }
}