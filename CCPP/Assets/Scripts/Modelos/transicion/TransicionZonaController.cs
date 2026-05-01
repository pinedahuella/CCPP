using UnityEngine;
using System.Collections;

/// <summary>
/// Trigger de transición entre zonas.
/// Al chocar el jugador: bloquea movimiento, baja cuadro negro,
/// teletransporta, intercambia zonas, sube cuadro negro y reactiva movimiento.
/// Requiere: Collider con isTrigger = true en el mismo GameObject.
/// </summary>
[RequireComponent(typeof(TransicionZonaData))]
[RequireComponent(typeof(Collider))]
public class TransicionZonaController : MonoBehaviour
{
    // ── Referencias ────────────────────────────────────────────────
    private TransicionZonaData _data;
    private JugadorData _jugadorData;
    private bool _enTransicion = false;

    // ──────────────────────────────────────────────────────────────
    #region Unity Callbacks

    private void Awake()
    {
        _data = GetComponent<TransicionZonaData>();
        AsegurarTrigger();
    }

    private void OnTriggerEnter(Collider other)
    {
        if (_enTransicion) return;
        if (!other.CompareTag("Player")) return;

        _jugadorData = other.GetComponent<JugadorData>();

        if (_jugadorData == null)
        {
            Debug.LogWarning("[TransicionZonaController] El jugador no tiene JugadorData.");
            return;
        }

        if (!ValidarReferencias()) return;

        StartCoroutine(EjecutarTransicion(other.transform));
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Inicialización

    private void AsegurarTrigger()
    {
        Collider col = GetComponent<Collider>();
        if (!col.isTrigger)
        {
            col.isTrigger = true;
            Debug.LogWarning("[TransicionZonaController] Collider no era trigger. Se corrigió automáticamente.");
        }
    }

    private bool ValidarReferencias()
    {
        if (_data.cuadroNegro == null)
        {
            Debug.LogError("[TransicionZonaController] cuadroNegro no asignado.");
            return false;
        }
        if (_data.puntoJugador == null)
        {
            Debug.LogError("[TransicionZonaController] puntoJugador no asignado.");
            return false;
        }
        if (_data.puntoCamara == null)
        {
            Debug.LogError("[TransicionZonaController] puntoCamara no asignado.");
            return false;
        }
        if (_data.camara == null)
        {
            Debug.LogError("[TransicionZonaController] camara no asignada.");
            return false;
        }
        return true;
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Transición

    private IEnumerator EjecutarTransicion(Transform jugador)
    {
        _enTransicion = true;

        // 1 — Bloquear movimiento
        _jugadorData.puedeMoverse = false;

        if (_data.audioTransicion != null)
            _data.audioTransicion.Play();

        // 2 — Bajar cuadro negro hasta Y = 0
        yield return StartCoroutine(MoverCuadro(0f));

        // 3 — Teletransportar jugador y cámara
        jugador.position = _data.puntoJugador.position;
        _data.camara.position = _data.puntoCamara.position;

        // 4 — Intercambiar zonas
        if (_data.zonaEntrada != null)
            _data.zonaEntrada.SetActive(true);

        if (_data.zonaSalida != null)
            _data.zonaSalida.SetActive(false);

        if (_data.nuevaCaminata != null && _jugadorData.audioCaminata != null)
            _jugadorData.audioCaminata.clip = _data.nuevaCaminata;

        CamaraData camaraData = _data.camara.GetComponent<CamaraData>();
        if (camaraData != null)
            camaraData.seguirJugador = _data.SeguirJugadorSiguiente;

        // 5 — Subir cuadro negro hasta Y = 2
        yield return StartCoroutine(MoverCuadro(2f));

        // 6 — Reactivar movimiento
        _jugadorData.puedeMoverse = true;

        _enTransicion = false;
    }

    /// <summary>
    /// Mueve el cuadro negro suavemente hasta el Y destino.
    /// </summary>
    private IEnumerator MoverCuadro(float yDestino)
    {
        Vector3 posInicial = _data.cuadroNegro.localPosition;
        Vector3 posDestino = new Vector3(posInicial.x, yDestino, posInicial.z);

        float distancia = Mathf.Abs(posInicial.y - yDestino);
        if (distancia < 0.001f) yield break;

        float tiempoTotal = distancia / _data.velocidadTransicion;
        float tiempoTranscurrido = 0f;

        while (tiempoTranscurrido < tiempoTotal)
        {
            tiempoTranscurrido += Time.deltaTime;
            float t = Mathf.Clamp01(tiempoTranscurrido / tiempoTotal);
            _data.cuadroNegro.localPosition = Vector3.Lerp(posInicial, posDestino, t);
            yield return null;
        }

        _data.cuadroNegro.localPosition = posDestino;
    }

    #endregion
}