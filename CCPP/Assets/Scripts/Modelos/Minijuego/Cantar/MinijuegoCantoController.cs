using UnityEngine;
using UnityEngine.UI;
using System.Collections;

/// <summary>
/// Controlador del minijuego de canto.
/// 4 pools independientes por carril. Deteccion por Y mundial.
/// Exito → valor 2. Fallo → valor 0.
/// </summary>
[RequireComponent(typeof(MinijuegoCantoData))]
public class MinijuegoCantoController : MonoBehaviour
{
    private MinijuegoCantoData _data;
    private Coroutine[] _flashCoroutines = new Coroutine[4];

    #region Unity Callbacks

    private void Awake()
    {
        _data = GetComponent<MinijuegoCantoData>();
    }

    private void Update()
    {
        if (!_data.minijuegoActivo) return;

        MoverNotas();
        ActualizarTimerNota();
    }

    #endregion

    #region API Pública

    /// <summary>
    /// Inicializa y abre el minijuego de canto.
    /// Resetea el estado, desactiva notas previas, configura botones y activa el panel.
    /// Llamado desde MinijuegoManager cuando el jugador elige Cantar en el panel de boca.
    /// </summary>
    public void Iniciar()
    {
        if (!ValidarReferencias()) return;

        LimpiarEstado();
        DesactivarTodasLasNotas();
        ResetearColoresBotones();
        ConfigurarBotones();

        _data.panelCanto.SetActive(true);
        _data.minijuegoActivo = true;
    }

    #endregion

    #region Notas

    /// <summary>
    /// Desplaza todas las notas activas hacia abajo y detecta cuando una nota pasa el margen del boton sin ser presionada.
    /// </summary>
    private void MoverNotas()
    {
        for (int carril = 0; carril < 4; carril++)
        {
            NotaCanto[] pool = ObtenerPool(carril);
            if (pool == null) continue;

            float botonY = _data.botones[carril].GetComponent<RectTransform>().position.y;

            foreach (NotaCanto nota in pool)
            {
                if (nota == null || !nota.activa) continue;

                nota.MoverAbajo(Time.deltaTime);

                float notaY = nota.GetComponent<RectTransform>().position.y;

                if (notaY < botonY - _data.margenAcierto)
                {
                    nota.Desactivar();
                    DispararFlashRojo(carril);
                    RegistrarFallo($"nota carril {carril} pasó sin presionar");
                }
            }
        }
    }

    /// <summary>Reduce el temporizador y lanza una nueva nota cuando llega a cero, reiniciando el intervalo.</summary>
    private void ActualizarTimerNota()
    {
        _data.timerNota -= Time.deltaTime;
        if (_data.timerNota <= 0f)
        {
            LanzarNota();
            _data.timerNota = _data.intervaloNotas;
        }
    }

    /// <summary>
    /// Elige un carril aleatorio, busca una nota inactiva en su pool y la activa con velocidad aleatoria.
    /// </summary>
    private void LanzarNota()
    {
        int carril = Random.Range(0, 4);
        NotaCanto[] pool = ObtenerPool(carril);
        if (pool == null) return;

        foreach (NotaCanto nota in pool)
        {
            if (nota == null || nota.activa) continue;

            float velocidad = Random.Range(_data.velocidadMin, _data.velocidadMax);
            float botonY = _data.botones[carril].GetComponent<RectTransform>().position.y;

            RectTransform rectNota = nota.GetComponent<RectTransform>();
            Vector3 pos = rectNota.position;
            pos.y = botonY + _data.posYInicial;
            rectNota.position = pos;

            nota.Activar(carril, velocidad);
            Debug.Log($"[MinijuegoCanto] Nota lanzada carril={carril} velocidad={velocidad:F1}");
            return;
        }
    }

    /// <summary>Desactiva todas las notas de todos los carriles para dejar el minijuego en estado limpio.</summary>
    private void DesactivarTodasLasNotas()
    {
        for (int i = 0; i < 4; i++)
        {
            NotaCanto[] pool = ObtenerPool(i);
            if (pool == null) continue;
            foreach (NotaCanto nota in pool)
                if (nota != null) nota.Desactivar();
        }
    }

    /// <summary>
    /// Devuelve el array de notas del carril especificado.
    /// </summary>
    /// <param name="carril">Indice del carril (0-3).</param>
    /// <returns>Array de NotaCanto del carril o null si el indice es invalido.</returns>
    private NotaCanto[] ObtenerPool(int carril)
    {
        switch (carril)
        {
            case 0: return _data.notasCarril0;
            case 1: return _data.notasCarril1;
            case 2: return _data.notasCarril2;
            case 3: return _data.notasCarril3;
            default:
                Debug.LogWarning($"[MinijuegoCanto] Carril inválido: {carril}");
                return null;
        }
    }

    #endregion

    #region Botones

    /// <summary>Asigna los listeners de click a cada boton de carril segun su indice.</summary>
    private void ConfigurarBotones()
    {
        LimpiarBotones();
        for (int i = 0; i < _data.botones.Length; i++)
        {
            if (_data.botones[i] == null) continue;
            int carrilCapturado = i;
            _data.botones[i].onClick.AddListener(() => AlPresionarBoton(carrilCapturado));
        }
    }

    /// <summary>
    /// Evalua si hay una nota en la zona de acierto del carril presionado.
    /// Registra acierto o fallo segun la posicion de la nota.
    /// </summary>
    /// <param name="carril">Indice del carril cuyo boton fue presionado.</param>
    private void AlPresionarBoton(int carril)
    {
        if (!_data.minijuegoActivo) return;

        NotaCanto[] pool = ObtenerPool(carril);
        if (pool == null) return;

        float botonY = _data.botones[carril].GetComponent<RectTransform>().position.y;

        foreach (NotaCanto nota in pool)
        {
            if (nota == null || !nota.activa) continue;

            float notaY = nota.GetComponent<RectTransform>().position.y;
            float diferencia = Mathf.Abs(notaY - botonY);

            Debug.Log($"[MinijuegoCanto] Botón {carril} — notaY={notaY:F1} botonY={botonY:F1} dif={diferencia:F1} margen={_data.margenAcierto}");

            if (diferencia <= _data.margenAcierto)
            {
                nota.Desactivar();
                _data.notasAcertadas++;
                Debug.Log($"[MinijuegoCanto] Acierto carril={carril} ({_data.notasAcertadas}/{_data.notasParaGanar})");

                if (_data.notasAcertadas >= _data.notasParaGanar)
                {
                    _data.minijuegoActivo = false;
                    StartCoroutine(Terminar(true));
                }
                return;
            }
        }

        DispararFlashRojo(carril);
        RegistrarFallo($"botón {carril} sin nota en zona");
    }

    /// <summary>Elimina todos los listeners de los botones de carril.</summary>
    private void LimpiarBotones()
    {
        if (_data.botones == null) return;
        foreach (var b in _data.botones)
            if (b != null) b.onClick.RemoveAllListeners();
    }

    /// <summary>Restaura el color blanco de todos los botones de carril al iniciar o terminar el minijuego.</summary>
    private void ResetearColoresBotones()
    {
        for (int i = 0; i < 4; i++)
        {
            if (_data.botones != null && _data.botones.Length > i && _data.botones[i] != null)
            {
                Image img = _data.botones[i].GetComponent<Image>();
                if (img != null) img.color = Color.white;
            }
        }
    }

    #endregion

    #region Flash Rojo

    /// <summary>
    /// Cancela el flash anterior del carril (si existe) y lanza uno nuevo para indicar error.
    /// </summary>
    /// <param name="carril">Indice del carril donde ocurrio el fallo.</param>
    private void DispararFlashRojo(int carril)
    {
        // Cancelar corrutina anterior del mismo carril si existe
        if (_flashCoroutines[carril] != null)
            StopCoroutine(_flashCoroutines[carril]);

        _flashCoroutines[carril] = StartCoroutine(FlashRojo(carril));
    }

    /// <summary>
    /// Pone el boton del carril en rojo durante 0.3 segundos y luego lo devuelve a blanco.
    /// </summary>
    /// <param name="carril">Indice del carril a iluminar en rojo.</param>
    private IEnumerator FlashRojo(int carril)
    {
        if (_data.botones[carril] == null) yield break;

        Image img = _data.botones[carril].GetComponent<Image>();
        if (img == null) yield break;

        img.color = Color.red;
        yield return new WaitForSeconds(0.3f);
        img.color = Color.white;

        _flashCoroutines[carril] = null;
    }

    #endregion

    #region Fallo y Fin

    /// <summary>
    /// Incrementa el contador de fallos y termina el minijuego si se supero el limite permitido.
    /// </summary>
    /// <param name="motivo">Descripcion del fallo para el log de depuracion.</param>
    private void RegistrarFallo(string motivo)
    {
        if (!_data.minijuegoActivo) return;

        _data.fallosActuales++;
        Debug.Log($"[MinijuegoCanto] Fallo {_data.fallosActuales}/{_data.fallosPermitidos} — {motivo}");

        if (_data.fallosActuales >= _data.fallosPermitidos)
        {
            _data.minijuegoActivo = false;
            StartCoroutine(Terminar(false));
        }
    }

    /// <summary>
    /// Limpia el estado del minijuego, cierra el panel y reporta el resultado a MisionesGlobal con TipoAccion.Boca.
    /// </summary>
    /// <param name="acerto">True si el jugador acierto las notas necesarias; false si supero los fallos.</param>
    private IEnumerator Terminar(bool acerto)
    {
        LimpiarBotones();
        DesactivarTodasLasNotas();
        ResetearColoresBotones();
        yield return new WaitForSeconds(0.4f);
        _data.panelCanto.SetActive(false);

        int valor = acerto ? 2 : 0;
        Debug.Log($"[MinijuegoCanto] Resultado → TipoAccion.Boca valor={valor}");

        AccionResultado resultado = new AccionResultado(TipoAccion.Boca, valor);
        if (MisionesGlobal.Instancia != null)
            MisionesGlobal.Instancia.ReportarResultado(resultado);
        else
            Debug.LogWarning("[MinijuegoCantoController] MisionesGlobal no encontrado.");
    }

    #endregion

    #region Helpers

    /// <summary>Resetea contadores de notas, fallos, timer y la lista de corrutinas de flash.</summary>
    private void LimpiarEstado()
    {
        _data.notasAcertadas = 0;
        _data.fallosActuales = 0;
        _data.timerNota = _data.intervaloNotas;
        _data.minijuegoActivo = false;

        for (int i = 0; i < _flashCoroutines.Length; i++)
            _flashCoroutines[i] = null;
    }

    /// <summary>Verifica que el panel y los 4 botones de carril esten asignados en el Inspector.</summary>
    /// <returns>True si todas las referencias son validas.</returns>
    private bool ValidarReferencias()
    {
        if (_data.panelCanto == null)
        {
            Debug.LogError("[MinijuegoCantoController] panelCanto no asignado.");
            return false;
        }
        if (_data.botones == null || _data.botones.Length != 4)
        {
            Debug.LogError("[MinijuegoCantoController] Se necesitan exactamente 4 botones.");
            return false;
        }
        return true;
    }

    #endregion
}