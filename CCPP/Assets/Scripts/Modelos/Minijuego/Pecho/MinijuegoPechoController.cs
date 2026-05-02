using UnityEngine;
using System.Collections;

/// <summary>
/// Controlador del minijuego de ritmo del pecho.
/// Un círculo externo se achica hacia el corazón.
/// El jugador debe hacer click cuando coincidan.
/// Éxito N veces → valor 1. Fallo → valor 0.
/// </summary>
[RequireComponent(typeof(MinijuegoPechoData))]
public class MinijuegoPechoController : MonoBehaviour
{
    private MinijuegoPechoData _data;

    // ──────────────────────────────────────────────────────────────
    #region Unity Callbacks

    private void Awake()
    {
        _data = GetComponent<MinijuegoPechoData>();
    }

    private void Update()
    {
        if (!_data.esperandoClick) return;

        // Achicar el círculo
        _data.tamanoActual -= _data.velocidadActual * Time.deltaTime;

        // Aplicar tamaño al círculo externo
        _data.circuloExterno.sizeDelta = new Vector2(_data.tamanoActual, _data.tamanoActual);

        // Si el círculo pasó el tamaño mínimo sin click → fallo
        if (_data.tamanoActual <= _data.tamanoCorazon - _data.margenAcierto)
        {
            _data.esperandoClick = false;
            Debug.Log("[MinijuegoPecho] Fallo - click tardío o no presionado");
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
        _data.panelPecho.SetActive(true);

        _data.botonCorazon.onClick.RemoveAllListeners();
        _data.botonCorazon.onClick.AddListener(AlClickearCorazon);

        IniciarRonda();
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Lógica de Ronda

    private void IniciarRonda()
    {
        _data.tamanoActual = _data.tamanoInicial;
        _data.velocidadActual = Random.Range(_data.velocidadMin, _data.velocidadMax);
        _data.esperandoClick = true;

        _data.circuloExterno.sizeDelta = new Vector2(_data.tamanoActual, _data.tamanoActual);

        Debug.Log($"[MinijuegoPecho] Ronda {_data.rondaActual + 1}/{_data.rondasTotales} " +
                  $"— velocidad={_data.velocidadActual:F1}");
    }

    private void AlClickearCorazon()
    {
        if (!_data.esperandoClick) return;

        float diferencia = Mathf.Abs(_data.tamanoActual - _data.tamanoCorazon);

        if (diferencia <= _data.margenAcierto)
        {
            // Acierto
            _data.esperandoClick = false;
            _data.rondaActual++;

            Debug.Log($"[MinijuegoPecho] Acierto ronda {_data.rondaActual}/{_data.rondasTotales} " +
                      $"— diferencia={diferencia:F1}");

            if (_data.rondaActual >= _data.rondasTotales)
            {
                StartCoroutine(Terminar(true));
            }
            else
            {
                // Pequeña pausa antes de la siguiente ronda
                StartCoroutine(PausaEntreRondas());
            }
        }
        else
        {
            // Click fuera del margen
            _data.esperandoClick = false;
            Debug.Log($"[MinijuegoPecho] Fallo - diferencia={diferencia:F1} fuera del margen={_data.margenAcierto}");
            StartCoroutine(Terminar(false));
        }
    }

    private IEnumerator PausaEntreRondas()
    {
        yield return new WaitForSeconds(0.3f);
        IniciarRonda();
    }

    private IEnumerator Terminar(bool acerto)
    {
        yield return new WaitForSeconds(0.5f);

        _data.panelPecho.SetActive(false);
        _data.botonCorazon.onClick.RemoveAllListeners();

        int valor = acerto ? 1 : 0;
        string descripcion = acerto ? "Éxito - todas las rondas completadas" : "Fallo";
        Debug.Log($"[MinijuegoPecho] {descripcion} → TipoAccion.Pecho valor={valor}");

        AccionResultado resultado = new AccionResultado(TipoAccion.Pecho, valor);

        if (MisionesGlobal.Instancia != null)
            MisionesGlobal.Instancia.ReportarResultado(resultado);
        else
            Debug.LogWarning("[MinijuegoPechoController] MisionesGlobal no encontrado.");
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Helpers

    private void LimpiarEstado()
    {
        _data.rondaActual = 0;
        _data.esperandoClick = false;
        _data.tamanoActual = _data.tamanoInicial;

        if (_data.circuloExterno != null)
            _data.circuloExterno.sizeDelta = new Vector2(_data.tamanoInicial, _data.tamanoInicial);
    }

    private bool ValidarReferencias()
    {
        if (_data.panelPecho == null)
        {
            Debug.LogError("[MinijuegoPechoController] panelPecho no asignado.");
            return false;
        }
        if (_data.circuloExterno == null)
        {
            Debug.LogError("[MinijuegoPechoController] circuloExterno no asignado.");
            return false;
        }
        if (_data.botonCorazon == null)
        {
            Debug.LogError("[MinijuegoPechoController] botonCorazon no asignado.");
            return false;
        }
        return true;
    }

    #endregion
}