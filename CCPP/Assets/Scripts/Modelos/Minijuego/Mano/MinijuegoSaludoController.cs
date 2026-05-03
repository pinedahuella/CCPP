using UnityEngine;
using System.Collections;

/// <summary>
/// Controlador del minijuego de saludo de mano.
/// Dos botones, uno correcto aleatorio, tiempo limitado con barra visual.
/// Exito → valor 1. Fallo → valor 0.
/// </summary>
[RequireComponent(typeof(MinijuegoSaludoData))]
public class MinijuegoSaludoController : MonoBehaviour
{
    private MinijuegoSaludoData _data;
    private bool _esperandoRespuesta = false;
    private float _tiempoRestante;

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

    #region API Pública

    /// <summary>
    /// Inicializa y abre el minijuego de saludo de mano.
    /// Elige aleatoriamente el boton correcto, configura listeners y activa el panel.
    /// Llamado desde MinijuegoManager cuando el jugador elige Saludo en el panel de mano.
    /// </summary>
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
    /// Elige aleatoriamente cual boton (arriba o abajo) es el correcto y
    /// reasigna las imagenes de manos para que la del otro personaje este en el boton correcto.
    /// </summary>
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

    /// <summary>Asigna los listeners a los botones de arriba y abajo para detectar la eleccion del jugador.</summary>
    private void ConfigurarBotones()
    {
        LimpiarBotones();
        if (_data.botonArriba != null) _data.botonArriba.onClick.AddListener(() => AlPresionar(true));
        if (_data.botonAbajo != null) _data.botonAbajo.onClick.AddListener(() => AlPresionar(false));
    }

    /// <summary>
    /// Compara el boton presionado con el boton correcto aleatorio y lanza la rutina de terminar.
    /// </summary>
    /// <param name="esArriba">True si el jugador presiono el boton de arriba.</param>
    private void AlPresionar(bool esArriba)
    {
        if (!_esperandoRespuesta) return;
        _esperandoRespuesta = false;
        StartCoroutine(Terminar(esArriba == _data.botonCorrectoEsArriba));
    }

    /// <summary>
    /// Muestra la imagen de exito si acierta, cierra el panel y reporta el resultado a MisionesGlobal con TipoAccion.Mano.
    /// </summary>
    /// <param name="acerto">True si el jugador presiono el boton correcto.</param>
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

    #region Helpers

    /// <summary>Resetea la bandera de espera y reactiva ambos botones antes de iniciar.</summary>
    private void LimpiarEstado()
    {
        _esperandoRespuesta = false;
        ReactivarBotones();
    }

    /// <summary>Elimina todos los listeners de los botones arriba y abajo.</summary>
    private void LimpiarBotones()
    {
        if (_data.botonArriba != null) _data.botonArriba.onClick.RemoveAllListeners();
        if (_data.botonAbajo != null) _data.botonAbajo.onClick.RemoveAllListeners();
    }

    /// <summary>Reactiva la visibilidad de ambos botones para el siguiente intento.</summary>
    private void ReactivarBotones()
    {
        if (_data.botonArriba != null) _data.botonArriba.gameObject.SetActive(true);
        if (_data.botonAbajo != null) _data.botonAbajo.gameObject.SetActive(true);
    }

    /// <summary>Verifica que el panel y los dos botones esten asignados en el Inspector.</summary>
    /// <returns>True si todas las referencias son validas.</returns>
    private bool ValidarReferencias()
    {
        if (_data.panelSaludo == null) { Debug.LogError("[MinijuegoSaludoController] panelSaludo no asignado."); return false; }
        if (_data.botonArriba == null || _data.botonAbajo == null) { Debug.LogError("[MinijuegoSaludoController] Botones no asignados."); return false; }
        return true;
    }

    #endregion
}