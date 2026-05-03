/// <summary>
/// Resultado que devuelve cualquier minijuego al terminar.
/// Solo datos, sin logica.
/// </summary>
public struct AccionResultado
{
    /// <summary>Tipo de accion que reporta el minijuego (Postura, Mano, Pecho, Cabeza, Boca).</summary>
    public TipoAccion tipo;
    /// <summary>Codigo de resultado devuelto por el minijuego; cada uno define sus propios valores.</summary>
    public int valor;

    /// <summary>
    /// Crea un nuevo resultado con el tipo y valor indicados.
    /// </summary>
    /// <param name="tipo">Tipo de accion del minijuego que termino.</param>
    /// <param name="valor">Codigo de resultado (p. ej. 1 = exito, 0 = fallo).</param>
    public AccionResultado(TipoAccion tipo, int valor)
    {
        this.tipo = tipo;
        this.valor = valor;
    }
}