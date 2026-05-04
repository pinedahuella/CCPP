using UnityEngine;

/// <summary>
/// Manager global de misiones. Gestiona una sola mision activa a la vez.
/// Recibe el resultado del minijuego, evalua la mision activa y la limpia al cumplirse.
/// Protegido contra referencias nulas en todos los puntos de entrada.
/// </summary>
public class MisionesGlobal : MonoBehaviour
{
    public static MisionesGlobal Instancia { get; private set; }

    private MisionBase _misionActiva;

    /// <summary>True si hay una mision pendiente de resolver en este momento.</summary>
    public bool TieneMisionActiva => _misionActiva != null;

    #region Unity Callbacks

    private void Awake()
    {
        ConfigurarSingleton();
    }

    private void OnDestroy()
    {
        if (Instancia == this)
            Instancia = null;
    }
    #endregion



    #region Inicialización

    /// <summary>
    /// Aplica el patron Singleton: si ya existe una instancia destruye este duplicado,
    /// de lo contrario se registra como instancia global y persiste entre escenas.
    /// </summary>
    private void ConfigurarSingleton()
    {
        if (Instancia != null && Instancia != this)
        {
            Debug.LogWarning("[MisionesGlobal] Ya existe una instancia. Destruyendo duplicado.");
            Destroy(gameObject);
            return;
        }

        Instancia = this;


    }

    #endregion

    #region API Pública

    /// <summary>
    /// Asigna una nueva mision activa.
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
    /// Si coincide llama Actuar(), si no llama ActuarFallo() si la mision lo soporta.
    /// En ambos casos limpia la mision activa.
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

            // Si la mision soporta fallo lo notifica
            if (misionResuelta is MisionPosicion misionPosicion)
                misionPosicion.ActuarFallo();
        }
    }

    /// <summary>
    /// Cancela la mision activa sin ejecutarla.
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