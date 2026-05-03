using UnityEngine;
using System.Collections;

/// <summary>
/// Controlador del minijuego de responder.
/// 3 botones con respuesta correcta definida por int.
/// Espacio transparenta ayuda pero acelera el tiempo.
/// Exito → valor 1. Fallo → valor 0.
/// </summary>
[RequireComponent(typeof(MinijuegoResponderData))]
public class MinijuegoResponderController : MonoBehaviour
{
    private MinijuegoResponderData _data;

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

    #region API Pública

    /// <summary>
    /// Inicializa y abre el minijuego de responder preguntas sobre la misa.
    /// Carga el contenido de la pregunta, configura botones y activa el panel.
    /// Llamado desde MinijuegoManager cuando el jugador elige Responder en el panel de boca.
    /// </summary>
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

    #region Update

    /// <summary>
    /// Reduce el tiempo restante aplicando el multiplicador de velocidad y actualiza el ancho de la barra.
    /// Si el tiempo se agota, termina con fallo.
    /// </summary>
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

    /// <summary>
    /// Detecta si el jugador presiona espacio para revelar parcialmente la ayuda
    /// y acelera la barra como penalizacion.
    /// </summary>
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

    #region Configuración

    /// <summary>Aplica el texto de los botones y el texto de ayuda al estado actual del Data.</summary>
    private void ConfigurarContenido()
    {
        if (_data.textoBoton0 != null) _data.textoBoton0.text = _data.textoBotones[0];
        if (_data.textoBoton1 != null) _data.textoBoton1.text = _data.textoBotones[1];
        if (_data.textoBoton2 != null) _data.textoBoton2.text = _data.textoBotones[2];

        if (_data.textoAyuda != null)
            _data.textoAyuda.text = _data.textoAyudaContenido;
    }

    /// <summary>Asigna los listeners de click a los tres botones de respuesta.</summary>
    private void ConfigurarBotones()
    {
        LimpiarBotones();
        if (_data.boton0 != null) _data.boton0.onClick.AddListener(() => AlResponder(0));
        if (_data.boton1 != null) _data.boton1.onClick.AddListener(() => AlResponder(1));
        if (_data.boton2 != null) _data.boton2.onClick.AddListener(() => AlResponder(2));
    }

    /// <summary>Restaura el alpha de la imagen de ayuda a 1 (completamente opaca) al iniciar.</summary>
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

    #region Lógica

    /// <summary>
    /// Compara el boton presionado con el indice de respuesta correcta y termina el minijuego.
    /// </summary>
    /// <param name="indice">Indice del boton presionado (0, 1 o 2).</param>
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

    /// <summary>
    /// Cierra el panel y reporta el resultado a MisionesGlobal con TipoAccion.Boca.
    /// </summary>
    /// <param name="acerto">True si el jugador eligio la respuesta correcta.</param>
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

    #region Helpers

    /// <summary>Resetea el tiempo restante, el multiplicador de velocidad y la barra al ancho inicial.</summary>
    private void LimpiarEstado()
    {
        _data.tiempoRestante = _data.tiempoLimite;
        _data.multiplicadorVelocidad = 1f;
        _data.esperandoRespuesta = false;

        if (_data.barraTiempo != null)
            _data.barraTiempo.sizeDelta = new Vector2(_data.anchoBarraInicial, _data.barraTiempo.sizeDelta.y);
    }

    /// <summary>Elimina todos los listeners de los tres botones de respuesta.</summary>
    private void LimpiarBotones()
    {
        if (_data.boton0 != null) _data.boton0.onClick.RemoveAllListeners();
        if (_data.boton1 != null) _data.boton1.onClick.RemoveAllListeners();
        if (_data.boton2 != null) _data.boton2.onClick.RemoveAllListeners();
    }

    /// <summary>Verifica que el panel y la barra de tiempo esten asignados en el Inspector.</summary>
    /// <returns>True si todas las referencias son validas.</returns>
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