using UnityEngine;

/// <summary>
/// Escucha el evento de selección de parte del cuerpo
/// y dispara el minijuego correspondiente.
/// Agregar nuevos minijuegos aquí conforme se implementen.
/// </summary>
public class MinijuegoManager : MonoBehaviour
{
    // ── Referencias a minijuegos ───────────────────────────────────
    [Header("Minijuegos")]
    [Tooltip("Controlador del minijuego de pierna")]
    public MinijuegoPiernaController minijuegoPierna;

    // Agregar aquí los demás conforme se implementen:
    // public MinijuegoPechoController    minijuegoPecho;
    // public MinijuegoCabezaController   minijuegoCabeza;
    // public MinijuegoBocaController     minijuegoBoca;
    // public MinijuegomanoDerechaController minijuegoManoDerecha;

    // ──────────────────────────────────────────────────────────────
    #region Unity Callbacks

    private void OnEnable()
    {
        CuerpoUIController.OnParteSeleccionada += AlSeleccionarParte;
    }

    private void OnDisable()
    {
        CuerpoUIController.OnParteSeleccionada -= AlSeleccionarParte;
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Lógica

    private void AlSeleccionarParte(ParteCuerpo parte)
    {
        switch (parte)
        {
            case ParteCuerpo.Piernas:
                IniciarMinijuego(minijuegoPierna, parte);
                break;

            // Descomentar conforme se implementen:
            // case ParteCuerpo.Pecho:
            //     IniciarMinijuego(minijuegoPecho, parte);
            //     break;
            // case ParteCuerpo.Cabeza:
            //     IniciarMinijuego(minijuegoCabeza, parte);
            //     break;
            // case ParteCuerpo.Boca:
            //     IniciarMinijuego(minijuegoBoca, parte);
            //     break;
            // case ParteCuerpo.ManoDerecha:
            //     IniciarMinijuego(minijuegoManoDerecha, parte);
            //     break;

            default:
                Debug.LogWarning($"[MinijuegoManager] No hay minijuego implementado para: {parte}");
                break;
        }
    }

    /// <summary>
    /// Valida la referencia antes de iniciar para evitar errores de nulo.
    /// </summary>
    private void IniciarMinijuego(MinijuegoPiernaController controlador, ParteCuerpo parte)
    {
        if (controlador == null)
        {
            Debug.LogWarning($"[MinijuegoManager] El minijuego de {parte} no está asignado en el Inspector.");
            return;
        }

        controlador.Iniciar();
    }

    #endregion
}