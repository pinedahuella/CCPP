using UnityEngine;
using System.Collections;
using UnityEngine.UI;

/// <summary>
/// Controlador del minijuego de señal.
/// 4 botones deben presionarse en orden aleatorio en tiempo limitado.
/// Éxito → valor 2. Fallo → valor 0.
/// </summary>
[RequireComponent(typeof(MinijuegoSenalData))]
public class MinijuegoSenalController : MonoBehaviour
{
    private MinijuegoSenalData _data;
    private bool _esperandoRespuesta = false;
    private float _tiempoRestante;

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
        GenerarOrdenAleatorio();
        ConfigurarBotones();
        MostrarOrdenVisual();

        _tiempoRestante = _data.tiempoLimite;
        _esperandoRespuesta = true;
        _data.panelSenal.SetActive(true);
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Lógica

    /// <summary>
    /// Genera un orden aleatorio de los 4 índices usando Fisher-Yates.
    /// </summary>
    private void GenerarOrdenAleatorio()
    {
        int[] indices = { 0, 1, 2, 3 };

        _data.ordenAleatorio = indices;
    }

    /// <summary>
    /// Muestra el número de orden encima de cada botón.
    /// Usa el texto del propio botón para indicar en qué posición va.
    /// </summary>
    private void MostrarOrdenVisual()
    {
        for (int i = 0; i < _data.botones.Length; i++)
        {
            if (_data.botones[i] == null) continue;

            // El índice en ordenAleatorio indica la posición de este botón
            // ordenAleatorio[posicion] = indiceDeBotobn
            // Buscamos en qué posición está el botón i
            int posicion = 0;
            for (int j = 0; j < _data.ordenAleatorio.Length; j++)
            {
                if (_data.ordenAleatorio[j] == i)
                {
                    posicion = j + 1; // 1-based para mostrar
                    break;
                }
            }

            // Mostrar el número en el texto del botón
            var texto = _data.botones[i].GetComponentInChildren<TMPro.TextMeshProUGUI>();
            if (texto != null)
                texto.text = posicion.ToString();
        }
    }

    private void ConfigurarBotones()
    {
        LimpiarBotones();

        for (int i = 0; i < _data.botones.Length; i++)
        {
            if (_data.botones[i] == null) continue;

            _data.botones[i].gameObject.SetActive(true);
            _data.botones[i].interactable = true;

            int indiceCapturado = i;
            _data.botones[i].onClick.AddListener(() => AlPresionar(indiceCapturado));
        }
    }

    private void AlPresionar(int indiceBoton)
    {
        if (!_esperandoRespuesta) return;

        int botonEsperado = _data.ordenAleatorio[_data.indiceActual];

        if (indiceBoton != botonEsperado)
        {
            // Orden incorrecto
            _esperandoRespuesta = false;
            StartCoroutine(Terminar(false));
            return;
        }

        _data.indiceActual++;

        // Desactivar el botón presionado
        _data.botones[indiceBoton].interactable = false;

        if (_data.indiceActual >= 4)
        {
            // Todos presionados en orden
            _esperandoRespuesta = false;
            StartCoroutine(Terminar(true));
        }
    }

    private IEnumerator Terminar(bool acerto)
    {
        LimpiarBotones();
        yield return new WaitForSeconds(0.3f);
        _data.panelSenal.SetActive(false);
        Reportar(acerto ? 2 : 0);
    }

    private void Reportar(int valor)
    {
        string descripcion = valor == 2 ? "Éxito - Señal completada" : "Fallo - Señal incorrecta o tiempo agotado";
        Debug.Log($"[MinijuegoSenal] {descripcion} → TipoAccion.Mano valor={valor}");

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
        foreach (Button b in _data.botones)
            if (b != null) b.onClick.RemoveAllListeners();
    }

    private bool ValidarReferencias()
    {
        if (_data.panelSenal == null)
        {
            Debug.LogError("[MinijuegoSenalController] panelSenal no asignado.");
            return false;
        }
        if (_data.botones == null || _data.botones.Length != 4)
        {
            Debug.LogError("[MinijuegoSenalController] Se necesitan exactamente 4 botones.");
            return false;
        }
        return true;
    }

    #endregion
}