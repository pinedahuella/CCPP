using UnityEngine;

/// <summary>
/// Gestiona la reproduccion de dialogos linea por linea.
/// Completamente independiente del resto del juego.
/// Recibe un DialogoData, lo ejecuta y dispara OnDialogoTerminado al acabar.
/// </summary>
[RequireComponent(typeof(DialogoUIData))]
public class DialogoController : MonoBehaviour
{
    private DialogoUIData _data;

    private DialogoData _dialogoActual;
    private int _indiceActual;
    private bool _dialogoActivo;

    /// <summary>
    /// Se dispara cuando el dialogo actual termina completamente.
    /// Cualquier sistema que inicie un dialogo puede suscribirse aqui.
    /// </summary>
    public static event System.Action OnDialogoTerminado;

    #region Unity Callbacks

    private void Awake()
    {
        _data = GetComponent<DialogoUIData>();
    }

    private void Update()
    {
        if (!_dialogoActivo) return;

        if (Input.GetKeyDown(_data.teclaAvanzar))
            Avanzar();
    }

    #endregion

    #region API Pública

    /// <summary>
    /// Inicia un dialogo dado un DialogoData.
    /// Si hay un dialogo activo lo interrumpe y comienza el nuevo.
    /// </summary>
    public void Iniciar(DialogoData dialogo)
    {
        if (dialogo == null)
        {
            Debug.LogWarning("[DialogoController] Se intentó iniciar un diálogo nulo.");
            return;
        }

        if (dialogo.lineas == null || dialogo.lineas.Length == 0)
        {
            Debug.LogWarning("[DialogoController] El diálogo no tiene líneas.");
            return;
        }

        _dialogoActual = dialogo;
        _indiceActual = 0;
        _dialogoActivo = true;

        _data.panelDialogo.SetActive(true);
        MostrarLineaActual();
    }

    #endregion

    #region Lógica

    /// <summary>
    /// Avanza a la siguiente linea o termina el dialogo.
    /// </summary>
    private void Avanzar()
    {
        _indiceActual++;

        if (_indiceActual >= _dialogoActual.lineas.Length)
        {
            Terminar();
            return;
        }

        MostrarLineaActual();
    }

    /// <summary>
    /// Muestra la linea actual en la UI.
    /// </summary>
    private void MostrarLineaActual()
    {
        if (!ValidarReferenciasUI()) return;

        DialogoLinea linea = _dialogoActual.lineas[_indiceActual];

        // Texto
        _data.textoDialogo.text = linea.texto;

        // Imagenes — se muestra solo la del lado activo
        if (linea.esIzquierda)
        {
            MostrarImagen(_data.imagenIzquierda, linea.imagen);
            OcultarImagen(_data.imagenDerecha);
        }
        else
        {
            MostrarImagen(_data.imagenDerecha, linea.imagen);
            OcultarImagen(_data.imagenIzquierda);
        }
    }

    private void MostrarImagen(UnityEngine.UI.Image imagen, Sprite sprite)
    {
        if (imagen == null) return;
        imagen.sprite = sprite;
        imagen.gameObject.SetActive(sprite != null);
    }

    private void OcultarImagen(UnityEngine.UI.Image imagen)
    {
        if (imagen == null) return;
        imagen.gameObject.SetActive(false);
    }

    /// <summary>
    /// Cierra el panel y dispara el evento de fin.
    /// </summary>
    private void Terminar()
    {
        _dialogoActivo = false;
        _dialogoActual = null;
        CerrarPanel();
        OnDialogoTerminado?.Invoke();
    }

    private void CerrarPanel()
    {
        if (_data != null && _data.panelDialogo != null)
            _data.panelDialogo.SetActive(false);
    }

    private bool ValidarReferenciasUI()
    {
        if (_data.textoDialogo == null)
        {
            Debug.LogError("[DialogoController] textoDialogo no asignado en DialogoUIData.");
            return false;
        }
        return true;
    }

    #endregion
}