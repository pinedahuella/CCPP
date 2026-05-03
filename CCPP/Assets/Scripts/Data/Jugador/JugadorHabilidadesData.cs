using UnityEngine;

/// <summary>
/// Fuente de verdad sobre que partes del cuerpo tiene desbloqueadas el jugador.
/// Solo datos, sin logica.
/// Vive en el mismo GameObject que JugadorData y JugadorController.
/// </summary>
public class JugadorHabilidadesData : MonoBehaviour
{
    [Header("Partes desbloqueadas")]
    [Tooltip("El jugador puede usar sus piernas")]
    public bool tienePiernas = true;

    [Tooltip("El jugador puede usar su pecho")]
    public bool tienePecho = true;

    [Tooltip("El jugador puede usar su cabeza")]
    public bool tieneCabeza = true;

    [Tooltip("El jugador puede usar su boca")]
    public bool tieneBoca = true;

    [Tooltip("El jugador puede usar su mano derecha")]
    public bool tieneManoDerecha = true;

    #region API Pública

    /// <summary>
    /// Devuelve si una parte especifica esta desbloqueada.
    /// Util para consultar por enum sin exponer los bools directamente.
    /// </summary>
    public bool EstaDesbloqueada(ParteCuerpo parte)
    {
        switch (parte)
        {
            case ParteCuerpo.Piernas: return tienePiernas;
            case ParteCuerpo.Pecho: return tienePecho;
            case ParteCuerpo.Cabeza: return tieneCabeza;
            case ParteCuerpo.Boca: return tieneBoca;
            case ParteCuerpo.ManoDerecha: return tieneManoDerecha;
            default:
                Debug.LogWarning($"[JugadorHabilidadesData] Parte no reconocida: {parte}");
                return false;
        }
    }

    #endregion
}