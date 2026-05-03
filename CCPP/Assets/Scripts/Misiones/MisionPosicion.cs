using UnityEngine;
using System;

/// <summary>
/// Mision que espera una postura especifica.
/// Acepta callbacks de acierto y fallo para que
/// cada mision concreta defina que hacer en cada caso.
/// </summary>
public class MisionPosicion : MisionBase
{
    private readonly Action _onAcierto;
    private readonly Action _onFallo;

    /// <summary>
    /// Crea una mision de postura con callbacks para acierto y fallo.
    /// </summary>
    /// <param name="tipo">Tipo de accion esperada (Postura, Mano, etc.).</param>
    /// <param name="valor">Codigo de postura correcta (1=parado, 2=sentado, 3=arrodillado).</param>
    /// <param name="onAcierto">Accion que se ejecuta cuando el resultado coincide.</param>
    /// <param name="onFallo">Accion que se ejecuta cuando el resultado no coincide.</param>
    public MisionPosicion(TipoAccion tipo, int valor, Action onAcierto, Action onFallo)
        : base(tipo, valor)
    {
        _onAcierto = onAcierto;
        _onFallo = onFallo;
    }

    /// <summary>
    /// Se llama cuando el resultado coincide con lo esperado.
    /// </summary>
    public override void Actuar()
    {
        _onAcierto?.Invoke();
    }

    /// <summary>
    /// Se llama cuando el resultado NO coincide con lo esperado.
    /// </summary>
    public void ActuarFallo()
    {
        _onFallo?.Invoke();
    }
}