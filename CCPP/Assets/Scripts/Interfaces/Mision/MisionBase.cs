/// <summary>
/// Clase base para cualquier mision del juego.
/// Cada mision concreta hereda de aqui, declara que resultado espera
/// e implementa su propia logica en Actuar().
/// No es MonoBehaviour: se instancia y se pasa como objeto.
/// </summary>
public abstract class MisionBase
{
    /// <summary>Tipo de accion que debe devolver el minijuego para que esta mision se cumpla.</summary>
    public TipoAccion TipoEsperado { get; protected set; }
    /// <summary>Valor entero esperado del resultado; cada minijuego define su propio codigo de exito.</summary>
    public int ValorEsperado { get; protected set; }

    #region Constructor

    /// <summary>
    /// Inicializa la mision con el tipo de accion y el valor de exito esperados.
    /// </summary>
    /// <param name="tipoEsperado">Tipo de accion que debe devolver el minijuego.</param>
    /// <param name="valorEsperado">Valor de exito definido por el minijuego concreto.</param>
    protected MisionBase(TipoAccion tipoEsperado, int valorEsperado)
    {
        TipoEsperado = tipoEsperado;
        ValorEsperado = valorEsperado;
    }

    #endregion

    #region API Pública

    /// <summary>
    /// Evalua si el resultado dado cumple esta mision.
    /// </summary>
    public bool EvaluarResultado(AccionResultado resultado)
    {
        return resultado.tipo == TipoEsperado && resultado.valor == ValorEsperado;
    }

    /// <summary>
    /// Logica que se ejecuta cuando la mision se cumple.
    /// Cada mision concreta define que hace aqui:
    /// abrir puerta, avanzar dialogo, disparar evento, etc.
    /// </summary>
    public abstract void Actuar();

    #endregion
}