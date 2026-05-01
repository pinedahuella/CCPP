using UnityEngine;

/// <summary>
/// Manager global de misiones. Gestiona una sola misión activa a la vez.
/// Recibe el resultado del minijuego, evalúa la misión activa y la limpia al cumplirse.
/// Protegido contra referencias nulas en todos los puntos de entrada.
/// </summary>
public class MisionesGlobal : MonoBehaviour
{
    // ── Singleton ──────────────────────────────────────────────────
    public static MisionesGlobal Instancia { get; private set; }

    // ── Estado ────────────────────────────────────────────────────
    private MisionBase _misionActiva;

    public bool TieneMisionActiva => _misionActiva != null;

    // ──────────────────────────────────────────────────────────────
    #region Unity Callbacks

    private void Awake()
    {
        ConfigurarSingleton();
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Inicialización

    private void ConfigurarSingleton()
    {
        if (Instancia != null && Instancia != this)
        {
            Debug.LogWarning("[MisionesGlobal] Ya existe una instancia. Destruyendo duplicado.");
            Destroy(gameObject);
            return;
        }

        Instancia = this;
        DontDestroyOnLoad(gameObject);
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region API Pública

    /// <summary>
    /// Asigna una nueva misión activa.
    /// </summary>
    public void AsignarMision(MisionBase nuevaMision)
    {
        if (nuevaMision == null)
        {
            Debug.LogWarning("[MisionesGlobal] Se intentó asignar una misión nula. Ignorado.");
            return;
        }

        if (_misionActiva != null)
            Debug.LogWarning("[MisionesGlobal] Se reemplazó una misión activa antes de que se completara.");

        _misionActiva = nuevaMision;
    }

    /// <summary>
    /// Llamado por el minijuego al terminar.
    /// Si coincide llama Actuar(), si no llama ActuarFallo() si la misión lo soporta.
    /// En ambos casos limpia la misión activa.
    /// </summary>
    public void ReportarResultado(AccionResultado resultado)
    {
        if (_misionActiva == null)
        {
            Debug.Log("[MisionesGlobal] Resultado reportado sin misión activa. Ignorado.");
            return;
        }

        MisionBase misionResuelta = _misionActiva;
        _misionActiva = null;

        if (misionResuelta.EvaluarResultado(resultado))
        {
            misionResuelta.Actuar();
        }
        else
        {
            Debug.Log($"[MisionesGlobal] Fallo. Esperaba tipo={misionResuelta.TipoEsperado} " +
                      $"valor={misionResuelta.ValorEsperado}. " +
                      $"Recibido tipo={resultado.tipo} valor={resultado.valor}.");

            // Si la misión soporta fallo lo notifica
            if (misionResuelta is MisionPosicion misionPosicion)
                misionPosicion.ActuarFallo();
        }
    }

    /// <summary>
    /// Cancela la misión activa sin ejecutarla.
    /// </summary>
    public void CancelarMision()
    {
        if (_misionActiva == null)
        {
            Debug.Log("[MisionesGlobal] No hay misión activa que cancelar.");
            return;
        }

        Debug.Log("[MisionesGlobal] Misión cancelada.");
        _misionActiva = null;
    }

    #endregion
}