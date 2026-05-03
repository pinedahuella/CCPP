using UnityEngine;
using UnityEngine.UI;
using TMPro;

/// <summary>
/// Referencias a los elementos UI del panel de dialogo.
/// MonoBehaviour, sin logica, solo datos.
/// </summary>
public class DialogoUIData : MonoBehaviour
{
    [Header("Panel")]
    [Tooltip("Panel raíz del diálogo, se activa y desactiva")]
    public GameObject panelDialogo;

    [Header("Texto")]
    [Tooltip("TextMeshPro donde se muestra el texto de cada línea")]
    public TextMeshProUGUI textoDialogo;

    [Header("Imágenes de personaje")]
    [Tooltip("Imagen del lado izquierdo")]
    public Image imagenIzquierda;

    [Tooltip("Imagen del lado derecho")]
    public Image imagenDerecha;

    [Header("Configuración")]
    [Tooltip("Tecla para avanzar al siguiente diálogo")]
    public KeyCode teclaAvanzar = KeyCode.Space;
}