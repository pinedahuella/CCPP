using UnityEngine;

/// <summary>
/// Escucha el evento de seleccion de parte del cuerpo
/// y dispara el minijuego o panel correspondiente.
/// </summary>
public class MinijuegoManager : MonoBehaviour
{
    [Header("Minijuegos")]
    public MinijuegoPiernaController minijuegoPierna;
    public MinijuegoPechoController minijuegoPecho;
    public MinijuegoCerebroController minijuegoCerebro;

    [Header("Mano")]
    public PanelManoController panelMano;
    public MinijuegoSaludoController minijuegoSaludo;
    public MinijuegoSenalController minijuegoSenal;

    [Header("Boca")]
    public PanelBocaController panelBoca;
    public MinijuegoResponderController minijuegoResponder;
    public MinijuegoCantoController minijuegoCanto;

    #region Unity Callbacks

    private void OnEnable()
    {
        CuerpoUIController.OnParteSeleccionada += AlSeleccionarParte;
        PanelManoController.OnSaludoSeleccionado += AlSeleccionarSaludo;
        PanelManoController.OnSenalSeleccionada += AlSeleccionarSenal;
        PanelBocaController.OnResponderSeleccionado += AlSeleccionarResponder;
        PanelBocaController.OnCantarSeleccionado += AlSeleccionarCantar;
    }

    private void OnDisable()
    {
        CuerpoUIController.OnParteSeleccionada -= AlSeleccionarParte;
        PanelManoController.OnSaludoSeleccionado -= AlSeleccionarSaludo;
        PanelManoController.OnSenalSeleccionada -= AlSeleccionarSenal;
        PanelBocaController.OnResponderSeleccionado -= AlSeleccionarResponder;
        PanelBocaController.OnCantarSeleccionado -= AlSeleccionarCantar;
    }

    #endregion

    #region Lógica

    /// <summary>
    /// Recibe la parte del cuerpo seleccionada por el jugador y lanza el minijuego o panel correspondiente.
    /// </summary>
    /// <param name="parte">Parte del cuerpo que el jugador selecciono en la UI.</param>
    private void AlSeleccionarParte(ParteCuerpo parte)
    {
        switch (parte)
        {
            case ParteCuerpo.Piernas:
                if (minijuegoPierna == null) { Advertir(parte); return; }
                minijuegoPierna.Iniciar();
                break;

            case ParteCuerpo.Pecho:
                if (minijuegoPecho == null) { Advertir(parte); return; }
                minijuegoPecho.Iniciar();
                break;

            case ParteCuerpo.Cabeza:
                if (minijuegoCerebro == null) { Advertir(parte); return; }
                minijuegoCerebro.Iniciar();
                break;

            case ParteCuerpo.ManoDerecha:
                if (panelMano == null) { Advertir(parte); return; }
                panelMano.AbrirPanel();
                break;

            case ParteCuerpo.Boca:
                if (panelBoca == null) { Advertir(parte); return; }
                panelBoca.AbrirPanel();
                break;

            default:
                Debug.LogWarning($"[MinijuegoManager] No hay minijuego implementado para: {parte}");
                break;
        }
    }

    /// <summary>Inicia el minijuego de saludo de mano cuando el jugador elige esa opcion en el panel.</summary>
    private void AlSeleccionarSaludo()
    {
        if (minijuegoSaludo == null) { Debug.LogWarning("[MinijuegoManager] minijuegoSaludo no asignado."); return; }
        minijuegoSaludo.Iniciar();
    }

    /// <summary>Inicia el minijuego de senal cuando el jugador elige esa opcion en el panel de mano.</summary>
    private void AlSeleccionarSenal()
    {
        if (minijuegoSenal == null) { Debug.LogWarning("[MinijuegoManager] minijuegoSenal no asignado."); return; }
        minijuegoSenal.Iniciar();
    }

    /// <summary>Inicia el minijuego de responder preguntas cuando el jugador lo elige en el panel de boca.</summary>
    private void AlSeleccionarResponder()
    {
        if (minijuegoResponder == null) { Debug.LogWarning("[MinijuegoManager] minijuegoResponder no asignado."); return; }
        minijuegoResponder.Iniciar();
    }

    /// <summary>Inicia el minijuego de canto cuando el jugador lo elige en el panel de boca.</summary>
    private void AlSeleccionarCantar()
    {
        if (minijuegoCanto == null) { Debug.LogWarning("[MinijuegoManager] minijuegoCanto no asignado."); return; }
        minijuegoCanto.Iniciar();
    }

    /// <summary>
    /// Emite un warning en consola indicando que el minijuego de la parte indicada no esta asignado.
    /// </summary>
    /// <param name="parte">Parte del cuerpo cuyo minijuego falta en el Inspector.</param>
    private void Advertir(ParteCuerpo parte)
    {
        Debug.LogWarning($"[MinijuegoManager] El minijuego de {parte} no está asignado en el Inspector.");
    }

    #endregion
}