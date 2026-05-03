using UnityEngine;
using UnityEngine.UI;
using System.Collections;

/// <summary>
/// Controlador del minijuego de señal.
/// Modo simple: 4 botones en orden fijo.
/// Modo complejo: más botones en orden fijo, distintos GameObjects.
/// Barra de tiempo en ambos modos.
/// Éxito → valor 2. Fallo → valor 0.
/// </summary>
[RequireComponent(typeof(MinijuegoSenalData))]
public class MinijuegoSenalController : MonoBehaviour
{
    private MinijuegoSenalData _data;
    private bool _esperandoRespuesta = false;
    private float _tiempoRestante;

    // Botones activos según el modo
    private Button[] _botonesActivos;

    // ──────────────────────────────────────────────────────────────
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

    // ──────────────────────────────────────────────────────────────
    #region API Pública

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

    // ──────────────────────────────────────────────────────────────
    #region Modo

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

    private int[] GenerarOrden(int cantidad)
    {
        int[] indices = new int[cantidad];
        for (int i = 0; i < cantidad; i++) indices[i] = i;
        return indices;
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Barra

    private void ActualizarBarra()
    {
        if (_data.barraTiempo == null) return;
        float t = Mathf.Clamp01(_tiempoRestante / _data.tiempoLimite);
        _data.barraTiempo.sizeDelta = new Vector2(_data.anchoBarraInicial * t, _data.barraTiempo.sizeDelta.y);
    }

    private void ResetearBarra()
    {
        if (_data.barraTiempo == null) return;
        _data.barraTiempo.sizeDelta = new Vector2(_data.anchoBarraInicial, _data.barraTiempo.sizeDelta.y);
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Lógica

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

    // ──────────────────────────────────────────────────────────────
    #region Helpers

    private void LimpiarEstado()
    {
        _data.indiceActual = 0;
        _esperandoRespuesta = false;
    }

    private void LimpiarBotones()
    {
        if (_botonesActivos == null) return;
        foreach (Button b in _botonesActivos)
            if (b != null) b.onClick.RemoveAllListeners();
    }

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