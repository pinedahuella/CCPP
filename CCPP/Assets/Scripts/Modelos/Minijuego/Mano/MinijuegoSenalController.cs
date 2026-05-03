using UnityEngine;
using UnityEngine.UI;
using System.Collections;

/// <summary>
/// Controlador del minijuego de senal.
/// Modo simple: 4 botones en orden fijo.
/// Modo complejo: mas botones en orden fijo, distintos GameObjects.
/// Barra de tiempo en ambos modos.
/// Exito → valor 2. Fallo → valor 0.
/// </summary>
[RequireComponent(typeof(MinijuegoSenalData))]
public class MinijuegoSenalController : MonoBehaviour
{
    private MinijuegoSenalData _data;
    private bool _esperandoRespuesta = false;
    private float _tiempoRestante;

    // Botones activos segun el modo
    private Button[] _botonesActivos;

    #region Unity Callbacks

    private void Awake()
    {
        _data = GetComponent<MinijuegoSenalData>();
    }

    private void Update()
    {
        if (!_esperandoRespuesta) return;

        _tiempoRestante -= Time.deltaTime;
        ActualizarBarra();

        if (_tiempoRestante <= 0f)
        {
            _esperandoRespuesta = false;
            StartCoroutine(Terminar(false));
        }
    }

    #endregion

    #region API Pública

    /// <summary>
    /// Inicializa y abre el minijuego de senal de la cruz.
    /// Configura el modo simple o complejo, genera el orden y activa el panel.
    /// Llamado desde MinijuegoManager cuando el jugador elige Senal en el panel de mano.
    /// </summary>
    public void Iniciar()
    {
        if (!ValidarReferencias()) return;

        LimpiarEstado();
        ConfigurarModo();
        ConfigurarBotones();
        MostrarOrdenVisual();
        ResetearBarra();

        _tiempoRestante = _data.tiempoLimite;
        _esperandoRespuesta = true;
        _data.panelSenal.SetActive(true);
    }

    #endregion

    #region Modo

    /// <summary>
    /// Activa los objetos del modo simple o complejo segun la configuracion y
    /// establece el array de botones activos y el orden a seguir.
    /// </summary>
    private void ConfigurarModo()
    {
        if (_data.esCompleja)
        {
            // Activar complejos, desactivar simples
            if (_data.objetosSimple != null)
                foreach (GameObject obj in _data.objetosSimple)
                    if (obj != null) obj.SetActive(false);

            if (_data.objetosComplejos != null)
                foreach (GameObject obj in _data.objetosComplejos)
                    if (obj != null) obj.SetActive(true);

            _botonesActivos = _data.botonesComplejos;
            _data.ordenAleatorio = GenerarOrden(_botonesActivos.Length);
        }
        else
        {
            // Activar simples, desactivar complejos
            if (_data.objetosComplejos != null)
                foreach (GameObject obj in _data.objetosComplejos)
                    if (obj != null) obj.SetActive(false);

            if (_data.objetosSimple != null)
                foreach (GameObject obj in _data.objetosSimple)
                    if (obj != null) obj.SetActive(true);

            _botonesActivos = _data.botones;
            _data.ordenAleatorio = GenerarOrden(_botonesActivos.Length);
        }
    }

    /// <summary>
    /// Genera un array de indices en orden secuencial (0, 1, 2, ...) para definir el orden de la senal.
    /// </summary>
    /// <param name="cantidad">Numero de botones del modo activo.</param>
    /// <returns>Array de indices en orden natural.</returns>
    private int[] GenerarOrden(int cantidad)
    {
        int[] indices = new int[cantidad];
        for (int i = 0; i < cantidad; i++) indices[i] = i;
        return indices;
    }

    #endregion

    #region Barra

    /// <summary>Actualiza el ancho de la barra de tiempo proporcional al tiempo restante.</summary>
    private void ActualizarBarra()
    {
        if (_data.barraTiempo == null) return;
        float t = Mathf.Clamp01(_tiempoRestante / _data.tiempoLimite);
        _data.barraTiempo.sizeDelta = new Vector2(_data.anchoBarraInicial * t, _data.barraTiempo.sizeDelta.y);
    }

    /// <summary>Restaura la barra de tiempo a su ancho inicial al comenzar el minijuego.</summary>
    private void ResetearBarra()
    {
        if (_data.barraTiempo == null) return;
        _data.barraTiempo.sizeDelta = new Vector2(_data.anchoBarraInicial, _data.barraTiempo.sizeDelta.y);
    }

    #endregion

    #region Lógica

    /// <summary>
    /// Escribe en el texto de cada boton el numero de posicion que le corresponde en el orden de la senal.
    /// </summary>
    private void MostrarOrdenVisual()
    {
        for (int i = 0; i < _botonesActivos.Length; i++)
        {
            if (_botonesActivos[i] == null) continue;

            int posicion = 0;
            for (int j = 0; j < _data.ordenAleatorio.Length; j++)
            {
                if (_data.ordenAleatorio[j] == i)
                {
                    posicion = j + 1;
                    break;
                }
            }

            var texto = _botonesActivos[i].GetComponentInChildren<TMPro.TextMeshProUGUI>();
            if (texto != null) texto.text = posicion.ToString();
        }
    }

    /// <summary>Asigna los listeners de click a cada boton activo del modo configurado.</summary>
    private void ConfigurarBotones()
    {
        LimpiarBotones();

        for (int i = 0; i < _botonesActivos.Length; i++)
        {
            if (_botonesActivos[i] == null) continue;

            _botonesActivos[i].gameObject.SetActive(true);
            _botonesActivos[i].interactable = true;

            int indiceCapturado = i;
            _botonesActivos[i].onClick.AddListener(() => AlPresionar(indiceCapturado));
        }
    }

    /// <summary>
    /// Verifica si el boton presionado corresponde al siguiente en el orden correcto.
    /// Si es incorrecto termina con fallo; si se completan todos, con exito.
    /// </summary>
    /// <param name="indiceBoton">Indice del boton que presiono el jugador.</param>
    private void AlPresionar(int indiceBoton)
    {
        if (!_esperandoRespuesta) return;

        int botonEsperado = _data.ordenAleatorio[_data.indiceActual];

        if (indiceBoton != botonEsperado)
        {
            _esperandoRespuesta = false;
            StartCoroutine(Terminar(false));
            return;
        }

        _botonesActivos[indiceBoton].interactable = false;
        _data.indiceActual++;

        if (_data.indiceActual >= _botonesActivos.Length)
        {
            _esperandoRespuesta = false;
            StartCoroutine(Terminar(true));
        }
    }

    /// <summary>
    /// Limpia los botones, cierra el panel y reporta el resultado a MisionesGlobal con TipoAccion.Mano.
    /// </summary>
    /// <param name="acerto">True si el jugador completo el orden correcto; false si fallo o se acabo el tiempo.</param>
    private IEnumerator Terminar(bool acerto)
    {
        LimpiarBotones();
        yield return new WaitForSeconds(0.3f);
        _data.panelSenal.SetActive(false);

        int valor = acerto ? 2 : 0;
        Debug.Log($"[MinijuegoSenal] {(acerto ? "Éxito" : "Fallo")} → TipoAccion.Mano valor={valor}");

        AccionResultado resultado = new AccionResultado(TipoAccion.Mano, valor);
        if (MisionesGlobal.Instancia != null)
            MisionesGlobal.Instancia.ReportarResultado(resultado);
        else
            Debug.LogWarning("[MinijuegoSenalController] MisionesGlobal no encontrado.");
    }

    #endregion

    #region Helpers

    /// <summary>Resetea el indice actual y la bandera de espera antes de iniciar.</summary>
    private void LimpiarEstado()
    {
        _data.indiceActual = 0;
        _esperandoRespuesta = false;
    }

    /// <summary>Elimina todos los listeners de los botones activos del modo actual.</summary>
    private void LimpiarBotones()
    {
        if (_botonesActivos == null) return;
        foreach (Button b in _botonesActivos)
            if (b != null) b.onClick.RemoveAllListeners();
    }

    /// <summary>Verifica que el panel y los botones del modo configurado esten asignados en el Inspector.</summary>
    /// <returns>True si todas las referencias son validas.</returns>
    private bool ValidarReferencias()
    {
        if (_data.panelSenal == null)
        {
            Debug.LogError("[MinijuegoSenalController] panelSenal no asignado.");
            return false;
        }
        if (!_data.esCompleja && (_data.botones == null || _data.botones.Length == 0))
        {
            Debug.LogError("[MinijuegoSenalController] botones simples no asignados.");
            return false;
        }
        if (_data.esCompleja && (_data.botonesComplejos == null || _data.botonesComplejos.Length == 0))
        {
            Debug.LogError("[MinijuegoSenalController] botonesComplejos no asignados.");
            return false;
        }
        return true;
    }

    #endregion
}