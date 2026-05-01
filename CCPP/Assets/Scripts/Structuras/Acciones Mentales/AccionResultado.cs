/// <summary>
/// Resultado que devuelve cualquier minijuego al terminar.
/// Solo datos, sin lógica.
/// </summary>
public struct AccionResultado
{
    public TipoAccion tipo;
    public int valor;

    public AccionResultado(TipoAccion tipo, int valor)
    {
        this.tipo = tipo;
        this.valor = valor;
    }
}