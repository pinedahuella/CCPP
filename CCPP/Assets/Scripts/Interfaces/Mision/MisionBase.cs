/// <summary>
/// Clase base para cualquier misión del juego.
/// Cada misión concreta hereda de aquí, declara qué resultado espera
/// e implementa su propia lógica en Actuar().
/// No es MonoBehaviour: se instancia y se pasa como objeto.
/// </summary>
public abstract class MisionBase
{
    // ── Condición de cumplimiento ──────────────────────────────────
    public TipoAccion TipoEsperado { get; protected set; }
    public int ValorEsperado { get; protected set; }

    // ──────────────────────────────────────────────────────────────
    #region Constructor

    protected MisionBase(TipoAccion tipoEsperado, int valorEsperado)
    {
        TipoEsperado = tipoEsperado;
        ValorEsperado = valorEsperado;
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region API Pública

    /// <summary>
    /// Evalúa si el resultado dado cumple esta misión.
    /// </summary>
    public bool EvaluarResultado(AccionResultado resultado)
    {
        return resultado.tipo == TipoEsperado && resultado.valor == ValorEsperado;
    }

    /// <summary>
    /// Lógica que se ejecuta cuando la misión se cumple.
    /// Cada misión concreta define qué hace aquí:
    /// abrir puerta, avanzar diálogo, disparar evento, etc.
    /// </summary>
    public abstract void Actuar();

    #endregion
}