using UnityEngine;
using System;

/// <summary>
/// Misión que espera una postura específica.
/// Acepta callbacks de acierto y fallo para que
/// cada misión concreta defina qué hacer en cada caso.
/// </summary>
public class MisionPosicion : MisionBase
{
    private readonly Action _onAcierto;
    private readonly Action _onFallo;

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