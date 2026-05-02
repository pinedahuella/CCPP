using UnityEngine;
using System.Collections;

/// <summary>
/// Controlador del minijuego de cerebro.
/// El jugador mantiene el alpha del cerebro con espacio
/// y hace click en los distractores para alejarlos.
/// Sobrevivir N segundos → valor 1. Fallo → valor 0.
/// </summary>
[RequireComponent(typeof(MinijuegoCerebroData))]
public class MinijuegoCerebroController : MonoBehaviour
{
    private MinijuegoCerebroData _data;

    // ──────────────────────────────────────────────────────────────
    #region Unity Callbacks

    private void Awake()
    {
        _data = GetComponent<MinijuegoCerebroData>();
    }

    private void Update()
    {
        if (!_data.minijuegoActivo) return;

        ActualizarTiempo();
        ActualizarCerebro();
        ActualizarDisstractores();
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region API Pública

    public void Iniciar()
    {
        if (!ValidarReferencias()) return;

        LimpiarEstado();
        ConfigurarDisstractores();

        _data.panelCerebro.SetActive(true);
        _data.minijuegoActivo = true;

        // Alpha inicial del cerebro al máximo
        SetAlphaCerebro(1f);
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Update Logic

    private void ActualizarTiempo()
    {
        _data.tiempoTranscurrido += Time.deltaTime;

        if (_data.tiempoTranscurrido >= _data.tiempoSobrevivir)
        {
            _data.minijuegoActivo = false;
            Debug.Log($"[MinijuegoCerebro] Éxito - sobrevivió {_data.tiempoSobrevivir}s");
            StartCoroutine(Terminar(true));
        }
    }

    private void ActualizarCerebro()
    {
        // Perder alpha constantemente
        float alphaActual = _data.imagenCerebro.color.a;
        alphaActual -= _data.perdidaAlpha * Time.deltaTime;

        // Espacio rellena alpha
        if (Input.GetKeyDown(KeyCode.Space))
        {
            alphaActual += _data.gananciaAlpha;
            Debug.Log($"[MinijuegoCerebro] Espacio presionado — alpha={Mathf.Clamp01(alphaActual):F2}");
        }

        alphaActual = Mathf.Clamp01(alphaActual);
        SetAlphaCerebro(alphaActual);

        // Si el alpha llega a 0 → fallo
        if (alphaActual <= 0f)
        {
            _data.minijuegoActivo = false;
            Debug.Log("[MinijuegoCerebro] Fallo - cerebro desvanecido");
            StartCoroutine(Terminar(false));
        }
    }

    private void ActualizarDisstractores()
    {
        if (_data.distractores == null) return;

        Vector2 posCerebro = _data.rectCerebro.anchoredPosition;

        foreach (DistractorCerebro distractor in _data.distractores)
        {
            if (distractor == null || !distractor.activo) continue;

            RectTransform rect = distractor.GetComponent<RectTransform>();

            // Mover hacia el cerebro
            Vector2 direccion = (posCerebro - rect.anchoredPosition).normalized;
            rect.anchoredPosition += direccion * distractor.velocidadActual * Time.deltaTime;

            // Detectar colisión por distancia
            float distancia = Vector2.Distance(rect.anchoredPosition, posCerebro);
            if (distancia <= _data.radioColision)
            {
                _data.minijuegoActivo = false;
                Debug.Log($"[MinijuegoCerebro] Fallo - distractor tocó el cerebro");
                StartCoroutine(Terminar(false));
                return;
            }
        }
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Configuración

    private void ConfigurarDisstractores()
    {
        if (_data.distractores == null) return;

        foreach (DistractorCerebro distractor in _data.distractores)
        {
            if (distractor == null) continue;

            // SEGURO ADICIONAL: Si por alguna razón la posición es cero, 
            // intentar capturarla de nuevo si sabemos que no debería ser el centro.
            if (distractor.posicionOriginal == Vector2.zero)
            {
                distractor.posicionOriginal = distractor.GetComponent<RectTransform>().anchoredPosition;
            }

            float velocidad = Random.Range(_data.velocidadMin, _data.velocidadMax);
            distractor.Resetear(velocidad);

            // Configurar botón
            distractor.boton.onClick.RemoveAllListeners();
            DistractorCerebro capturado = distractor;
            distractor.boton.onClick.AddListener(() =>
                capturado.AlClickear(_data.velocidadMin, _data.velocidadMax));
        }
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Terminar

    private IEnumerator Terminar(bool acerto)
    {
        // Desactivar botones de distractores
        if (_data.distractores != null)
            foreach (DistractorCerebro d in _data.distractores)
                if (d != null && d.boton != null)
                    d.boton.onClick.RemoveAllListeners();

        yield return new WaitForSeconds(0.5f);
        _data.panelCerebro.SetActive(false);

        int valor = acerto ? 1 : 0;
        Debug.Log($"[MinijuegoCerebro] Resultado → TipoAccion.Cabeza valor={valor}");

        AccionResultado resultado = new AccionResultado(TipoAccion.Cabeza, valor);

        if (MisionesGlobal.Instancia != null)
            MisionesGlobal.Instancia.ReportarResultado(resultado);
        else
            Debug.LogWarning("[MinijuegoCerebroController] MisionesGlobal no encontrado.");
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Helpers

    private void LimpiarEstado()
    {
        _data.tiempoTranscurrido = 0f;
        _data.minijuegoActivo = false;
    }

    private void SetAlphaCerebro(float alpha)
    {
        Color c = _data.imagenCerebro.color;
        c.a = alpha;
        _data.imagenCerebro.color = c;
    }

    private bool ValidarReferencias()
    {
        if (_data.panelCerebro == null)
        {
            Debug.LogError("[MinijuegoCerebroController] panelCerebro no asignado.");
            return false;
        }
        if (_data.imagenCerebro == null)
        {
            Debug.LogError("[MinijuegoCerebroController] imagenCerebro no asignada.");
            return false;
        }
        if (_data.rectCerebro == null)
        {
            Debug.LogError("[MinijuegoCerebroController] rectCerebro no asignado.");
            return false;
        }
        if (_data.distractores == null || _data.distractores.Length != 4)
        {
            Debug.LogError("[MinijuegoCerebroController] Se necesitan exactamente 4 distractores.");
            return false;
        }
        return true;
    }

    #endregion
}