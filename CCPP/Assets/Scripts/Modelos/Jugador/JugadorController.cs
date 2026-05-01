using UnityEngine;
/// <summary>
/// Controlador de movimiento del jugador.
/// Lee input en Update y aplica física en FixedUpdate.
/// Requiere: Rigidbody, JugadorData en el mismo GameObject.
/// </summary>
[RequireComponent(typeof(Rigidbody))]
[RequireComponent(typeof(JugadorData))]
public class JugadorController : MonoBehaviour
{
    // ── Referencias ────────────────────────────────────────────────
    private JugadorData _data;
    private Rigidbody _rb;

    // ──────────────────────────────────────────────────────────────
    #region Unity Callbacks

    private void Awake()
    {
        ObtenerReferencias();
        ConfigurarRigidbody();
    }

    private void Update()
    {
        LeerInput();
    }

    private void FixedUpdate()
    {
        if (!_data.puedeMoverse)
            return;

        AplicarMovimiento();
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Inicialización

    private void ObtenerReferencias()
    {
        _data = GetComponent<JugadorData>();
        _rb = GetComponent<Rigidbody>();
    }

    /// <summary>
    /// Congela rotación para que la física no tumbe al jugador.
    /// </summary>
    private void ConfigurarRigidbody()
    {
        _rb.freezeRotation = true;
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Input

    /// <summary>
    /// Detecta WASD y almacena la dirección normalizada en el plano XZ.
    /// Llamado en Update — no afecta la física directamente.
    /// </summary>
    private void LeerInput()
    {
        float h = Input.GetAxisRaw("Horizontal");
        float v = Input.GetAxisRaw("Vertical");
        _data.direccionInput = new Vector3(h, 0f, v).normalized;
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Física

    /// <summary>
    /// Mueve al jugador con aceleración y desaceleración suaves,
    /// respetando la velocidad máxima sin importar los FPS.
    ///
    /// Por qué NO usamos AddForce aquí:
    ///   AddForce acumula indefinidamente; para limitar la velocidad
    ///   hay que cancelar/ajustar la fuerza cada frame, lo que es
    ///   equivalente (y más claro) a manejar la velocidad directamente.
    ///
    /// Por qué es frame-rate independent:
    ///   Todo el cálculo vive en FixedUpdate, que Unity llama a intervalos
    ///   fijos (Time.fixedDeltaTime). MoveTowards avanza la misma cantidad
    ///   de unidades por segundo sin importar cuántos frames renders haya.
    /// </summary>
    private void AplicarMovimiento()
    {
        // Velocidad actual solo en el plano XZ (ignoramos Y para no
        // interferir con la gravedad ni con saltos futuros)
        Vector3 velActualXZ = new Vector3(_rb.linearVelocity.x, 0f, _rb.linearVelocity.z);

        Vector3 velObjetivo;
        float tasa;

        if (_data.direccionInput != Vector3.zero)
        {
            // Hay input → acelerar hacia la dirección deseada
            velObjetivo = _data.direccionInput * _data.velocidadMaxima;
            tasa = _data.aceleracion * Time.fixedDeltaTime;
        }
        else
        {
            // Sin input → frenar hasta cero
            velObjetivo = Vector3.zero;
            tasa = _data.desaceleracion * Time.fixedDeltaTime;
        }

        // MoveTowards nunca supera el target ni la tasa: sin overshooting
        Vector3 nuevaVelXZ = Vector3.MoveTowards(velActualXZ, velObjetivo, tasa);

        // Recomponemos con la Y original para respetar gravedad / saltos
        _rb.linearVelocity = new Vector3(nuevaVelXZ.x, _rb.linearVelocity.y, nuevaVelXZ.z);
    }

    #endregion
}