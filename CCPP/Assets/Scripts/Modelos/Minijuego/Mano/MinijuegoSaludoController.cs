using UnityEngine;
using System.Collections;

/// <summary>
/// Controlador del minijuego de saludo de mano.
/// Dos botones, uno correcto aleatorio, tiempo limitado con barra visual.
/// Éxito → valor 1. Fallo → valor 0.
/// </summary>
[RequireComponent(typeof(MinijuegoSaludoData))]
public class MinijuegoSaludoController : MonoBehaviour
{
    private MinijuegoSaludoData _data;
    private bool _esperandoRespuesta = false;
    private float _tiempoRestante;

    // ──────────────────────────────────────────────────────────────
    #region Unity Callbacks

    private void Awake()
    {
        _data = GetComponent<MinijuegoSaludoData>();
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
        AsignarManoAleatoria();
        ConfigurarBotones();
        ResetearBarra();

        if (_data.imagenExito != null)
            _data.imagenExito.SetActive(false);

        _tiempoRestante = _data.tiempoLimite;
        _esperandoRespuesta = true;
        _data.panelSaludo.SetActive(true);
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

    private void AsignarManoAleatoria()
    {
        _data.botonCorrectoEsArriba = Random.value > 0.5f;

        Transform padreCorrecto = _data.botonCorrectoEsArriba ? _data.botonArriba.transform : _data.botonAbajo.transform;
        Transform padreIncorrecto = _data.botonCorrectoEsArriba ? _data.botonAbajo.transform : _data.botonArriba.transform;

        if (_data.imagenManoOtro != null)
            _data.imagenManoOtro.transform.SetParent(padreCorrecto, false);

        if (_data.imagenManoJugador != null)
            _data.imagenManoJugador.transform.SetParent(padreIncorrecto, false);
    }

    private void ConfigurarBotones()
    {
        LimpiarBotones();
        if (_data.botonArriba != null) _data.botonArriba.onClick.AddListener(() => AlPresionar(true));
        if (_data.botonAbajo != null) _data.botonAbajo.onClick.AddListener(() => AlPresionar(false));
    }

    private void AlPresionar(bool esArriba)
    {
        if (!_esperandoRespuesta) return;
        _esperandoRespuesta = false;
        StartCoroutine(Terminar(esArriba == _data.botonCorrectoEsArriba));
    }

    private IEnumerator Terminar(bool acerto)
    {
        LimpiarBotones();

        if (acerto)
        {
            _data.botonArriba.gameObject.SetActive(false);
            _data.botonAbajo.gameObject.SetActive(false);
            if (_data.imagenExito != null) _data.imagenExito.SetActive(true);
            yield return new WaitForSeconds(_data.tiempoExito);
        }

        _data.panelSaludo.SetActive(false);
        ReactivarBotones();

        int valor = acerto ? 1 : 0;
        Debug.Log($"[MinijuegoSaludo] {(acerto ? "Éxito" : "Fallo")} → TipoAccion.Mano valor={valor}");

        AccionResultado resultado = new AccionResultado(TipoAccion.Mano, valor);
        if (MisionesGlobal.Instancia != null)
            MisionesGlobal.Instancia.ReportarResultado(resultado);
        else
            Debug.LogWarning("[MinijuegoSaludoController] MisionesGlobal no encontrado.");
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Helpers

    private void LimpiarEstado()
    {
        _esperandoRespuesta = false;
        ReactivarBotones();
    }

    private void LimpiarBotones()
    {
        if (_data.botonArriba != null) _data.botonArriba.onClick.RemoveAllListeners();
        if (_data.botonAbajo != null) _data.botonAbajo.onClick.RemoveAllListeners();
    }

    private void ReactivarBotones()
    {
        if (_data.botonArriba != null) _data.botonArriba.gameObject.SetActive(true);
        if (_data.botonAbajo != null) _data.botonAbajo.gameObject.SetActive(true);
    }

    private bool ValidarReferencias()
    {
        if (_data.panelSaludo == null) { Debug.LogError("[MinijuegoSaludoController] panelSaludo no asignado."); return false; }
        if (_data.botonArriba == null || _data.botonAbajo == null) { Debug.LogError("[MinijuegoSaludoController] Botones no asignados."); return false; }
        return true;
    }

    #endregion
}