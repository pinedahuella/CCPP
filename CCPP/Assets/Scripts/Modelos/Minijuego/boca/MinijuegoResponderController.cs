using UnityEngine;
using System.Collections;

/// <summary>
/// Controlador del minijuego de responder.
/// 3 botones con respuesta correcta definida por int.
/// Espacio transparenta ayuda pero acelera el tiempo.
/// Éxito → valor 1. Fallo → valor 0.
/// </summary>
[RequireComponent(typeof(MinijuegoResponderData))]
public class MinijuegoResponderController : MonoBehaviour
{
    private MinijuegoResponderData _data;

    // ──────────────────────────────────────────────────────────────
    #region Unity Callbacks

    private void Awake()
    {
        _data = GetComponent<MinijuegoResponderData>();
    }

    private void Update()
    {
        if (!_data.esperandoRespuesta) return;

        ActualizarBarra();
        DetectarAyuda();
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region API Pública

    public void Iniciar()
    {
        if (!ValidarReferencias()) return;

        LimpiarEstado();
        ConfigurarContenido();
        ConfigurarBotones();
        ResetearAyuda();

        _data.panelResponder.SetActive(true);
        _data.esperandoRespuesta = true;
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Update

    private void ActualizarBarra()
    {
        _data.tiempoRestante -= Time.deltaTime * _data.multiplicadorVelocidad;

        float t = Mathf.Clamp01(_data.tiempoRestante / _data.tiempoLimite);
        float nuevoAncho = _data.anchoBarraInicial * t;
        _data.barraTiempo.sizeDelta = new Vector2(nuevoAncho, _data.barraTiempo.sizeDelta.y);

        if (_data.tiempoRestante <= 0f)
        {
            _data.esperandoRespuesta = false;
            Debug.Log("[MinijuegoResponder] Fallo - tiempo agotado");
            StartCoroutine(Terminar(false));
        }
    }

    private void DetectarAyuda()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            // Transparentar imagen de ayuda
            if (_data.imagenAyuda != null)
            {
                Color c = _data.imagenAyuda.color;
                c.a = Mathf.Max(0f, c.a - _data.alphaAyudaPorEspacio);
                _data.imagenAyuda.color = c;
            }

            // Acelerar barra
            _data.multiplicadorVelocidad *= _data.aceleracionBarraPorEspacio;

            Debug.Log($"[MinijuegoResponder] Ayuda usada — " +
                      $"alphaAyuda={_data.imagenAyuda?.color.a:F2} " +
                      $"multiplicador={_data.multiplicadorVelocidad:F2}");
        }
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Configuración

    private void ConfigurarContenido()
    {
        if (_data.textoBoton0 != null) _data.textoBoton0.text = _data.textoBotones[0];
        if (_data.textoBoton1 != null) _data.textoBoton1.text = _data.textoBotones[1];
        if (_data.textoBoton2 != null) _data.textoBoton2.text = _data.textoBotones[2];

        if (_data.textoAyuda != null)
            _data.textoAyuda.text = _data.textoAyudaContenido;
    }

    private void ConfigurarBotones()
    {
        LimpiarBotones();
        if (_data.boton0 != null) _data.boton0.onClick.AddListener(() => AlResponder(0));
        if (_data.boton1 != null) _data.boton1.onClick.AddListener(() => AlResponder(1));
        if (_data.boton2 != null) _data.boton2.onClick.AddListener(() => AlResponder(2));
    }

    private void ResetearAyuda()
    {
        if (_data.imagenAyuda != null)
        {
            Color c = _data.imagenAyuda.color;
            c.a = 1f;
            _data.imagenAyuda.color = c;
        }
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Lógica

    private void AlResponder(int indice)
    {
        if (!_data.esperandoRespuesta) return;
        _data.esperandoRespuesta = false;

        bool correcto = indice == _data.indiceRespuestaCorrecta
                        && _data.indiceRespuestaCorrecta >= 0
                        && _data.indiceRespuestaCorrecta <= 2;

        Debug.Log($"[MinijuegoResponder] Botón {indice} presionado — " +
                  $"correcto={correcto}");

        StartCoroutine(Terminar(correcto));
    }

    private IEnumerator Terminar(bool acerto)
    {
        LimpiarBotones();
        yield return new WaitForSeconds(0.4f);
        _data.panelResponder.SetActive(false);

        int valor = acerto ? 1 : 0;
        Debug.Log($"[MinijuegoResponder] Resultado → TipoAccion.Boca valor={valor}");

        AccionResultado resultado = new AccionResultado(TipoAccion.Boca, valor);
        if (MisionesGlobal.Instancia != null)
            MisionesGlobal.Instancia.ReportarResultado(resultado);
        else
            Debug.LogWarning("[MinijuegoResponderController] MisionesGlobal no encontrado.");
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Helpers

    private void LimpiarEstado()
    {
        _data.tiempoRestante = _data.tiempoLimite;
        _data.multiplicadorVelocidad = 1f;
        _data.esperandoRespuesta = false;

        if (_data.barraTiempo != null)
            _data.barraTiempo.sizeDelta = new Vector2(_data.anchoBarraInicial, _data.barraTiempo.sizeDelta.y);
    }

    private void LimpiarBotones()
    {
        if (_data.boton0 != null) _data.boton0.onClick.RemoveAllListeners();
        if (_data.boton1 != null) _data.boton1.onClick.RemoveAllListeners();
        if (_data.boton2 != null) _data.boton2.onClick.RemoveAllListeners();
    }

    private bool ValidarReferencias()
    {
        if (_data.panelResponder == null)
        {
            Debug.LogError("[MinijuegoResponderController] panelResponder no asignado.");
            return false;
        }
        if (_data.barraTiempo == null)
        {
            Debug.LogError("[MinijuegoResponderController] barraTiempo no asignada.");
            return false;
        }
        return true;
    }

    #endregion
}