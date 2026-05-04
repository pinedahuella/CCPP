using UnityEngine;
using System.Collections;

/// <summary>
/// Trigger de transicion entre zonas.
/// Al chocar el jugador: bloquea movimiento, baja cuadro negro,
/// teletransporta, intercambia zonas, sube cuadro negro y reactiva movimiento.
/// Requiere: Collider con isTrigger = true en el mismo GameObject.
/// </summary>
[RequireComponent(typeof(TransicionZonaData))]
[RequireComponent(typeof(Collider))]
public class TransicionZonaController : MonoBehaviour
{
    private TransicionZonaData _data;
    private JugadorData _jugadorData;
    private bool _enTransicion = false;

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

    #region Inicialización

    /// <summary>
    /// Garantiza que el Collider tenga isTrigger = true, corrigiendolo automaticamente si no lo esta.
    /// </summary>
    private void AsegurarTrigger()
    {
        Collider col = GetComponent<Collider>();
        if (!col.isTrigger)
        {
            col.isTrigger = true;
            Debug.LogWarning("[TransicionZonaController] Collider no era trigger. Se corrigió automáticamente.");
        }
    }

    /// <summary>Verifica que el cuadro negro, los puntos de teletransporte y la camara esten asignados.</summary>
    /// <returns>True si todas las referencias son validas para ejecutar la transicion.</returns>
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

    #region Transición

    /// <summary>
    /// Ejecuta la secuencia de transicion: bloquea movimiento, baja el cuadro negro,
    /// teletransporta jugador y camara, intercambia zonas y sube el cuadro negro.
    /// </summary>
    /// <param name="jugador">Transform del jugador que activo el trigger.</param>

    private IEnumerator EjecutarTransicion(Transform jugador)
    {
        _enTransicion = true;

        // 1 — Bloquear movimiento y input
        _jugadorData.puedeMoverse = false;
        _jugadorData.direccionInput = Vector3.zero;

        // 2 — Obtener rigidbody y desactivar física INMEDIATAMENTE
        Rigidbody rb = jugador.GetComponent<Rigidbody>();
        if (rb != null)
        {
            rb.isKinematic = true;
            rb.Sleep();
        }

        if (_data.audioTransicion != null)
            _data.audioTransicion.Play();

        // 3 — Bajar cuadro negro
        yield return StartCoroutine(MoverCuadro(0f));

        // 4 — Intercambiar zonas
        if (_data.zonaEntrada != null)
            _data.zonaEntrada.SetActive(true);

        if (_data.zonaSalida != null)
            _data.zonaSalida.SetActive(false);

        // 5 — Esperar 3 frames para que Unity procese todos los colliders nuevos
        yield return null;
        yield return null;
        yield return null;

        // 6 — Teletransportar con Physics.SyncTransforms para forzar actualización
        jugador.position = _data.puntoJugador.position;
        jugador.rotation = _data.puntoJugador.rotation;
        _data.camara.position = _data.puntoCamara.position;
        Physics.SyncTransforms();

        // 7 — Esperar un FixedUpdate para que la física registre la nueva posición
        yield return new WaitForFixedUpdate();
        yield return new WaitForFixedUpdate();

        // 8 — Reactivar física limpia
        if (rb != null)
        {
            rb.isKinematic = false;
            rb.linearVelocity = Vector3.zero;
            rb.angularVelocity = Vector3.zero;
            rb.Sleep();
            yield return new WaitForFixedUpdate();
            rb.WakeUp();
        }

        // 9 — Cambiar audio caminata si aplica
        if (_data.nuevaCaminata != null && _jugadorData.audioCaminata != null)
            _jugadorData.audioCaminata.clip = _data.nuevaCaminata;

        // 10 — Cambiar seguimiento cámara si aplica
        CamaraData camaraData = _data.camara.GetComponent<CamaraData>();
        if (camaraData != null)
            camaraData.seguirJugador = _data.SeguirJugadorSiguiente;

        // 11 — Subir cuadro negro
        yield return StartCoroutine(MoverCuadro(2f));

        // 12 — Reactivar movimiento
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