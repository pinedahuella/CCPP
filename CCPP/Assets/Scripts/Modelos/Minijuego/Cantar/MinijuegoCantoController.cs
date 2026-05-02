using UnityEngine;
using UnityEngine.UI;
using System.Collections;

/// <summary>
/// Controlador del minijuego de canto.
/// 4 pools independientes por carril. Detección por Y mundial.
/// Éxito → valor 2. Fallo → valor 0.
/// </summary>
[RequireComponent(typeof(MinijuegoCantoData))]
public class MinijuegoCantoController : MonoBehaviour
{
    private MinijuegoCantoData _data;
    private Coroutine[] _flashCoroutines = new Coroutine[4];

    // ──────────────────────────────────────────────────────────────
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

    // ──────────────────────────────────────────────────────────────
    #region API Pública

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

    // ──────────────────────────────────────────────────────────────
    #region Notas

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

    private void ActualizarTimerNota()
    {
        _data.timerNota -= Time.deltaTime;
        if (_data.timerNota <= 0f)
        {
            LanzarNota();
            _data.timerNota = _data.intervaloNotas;
        }
    }

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

    // ──────────────────────────────────────────────────────────────
    #region Botones

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

    private void LimpiarBotones()
    {
        if (_data.botones == null) return;
        foreach (var b in _data.botones)
            if (b != null) b.onClick.RemoveAllListeners();
    }

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

    // ──────────────────────────────────────────────────────────────
    #region Flash Rojo

    private void DispararFlashRojo(int carril)
    {
        // Cancelar corrutina anterior del mismo carril si existe
        if (_flashCoroutines[carril] != null)
            StopCoroutine(_flashCoroutines[carril]);

        _flashCoroutines[carril] = StartCoroutine(FlashRojo(carril));
    }

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

    // ──────────────────────────────────────────────────────────────
    #region Fallo y Fin

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

    // ──────────────────────────────────────────────────────────────
    #region Helpers

    private void LimpiarEstado()
    {
        _data.notasAcertadas = 0;
        _data.fallosActuales = 0;
        _data.timerNota = _data.intervaloNotas;
        _data.minijuegoActivo = false;

        for (int i = 0; i < _flashCoroutines.Length; i++)
            _flashCoroutines[i] = null;
    }

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