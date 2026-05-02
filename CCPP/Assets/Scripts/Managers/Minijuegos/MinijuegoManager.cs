using UnityEngine;

/// <summary>
/// Escucha el evento de selección de parte del cuerpo
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

    // ──────────────────────────────────────────────────────────────
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

    // ──────────────────────────────────────────────────────────────
    #region Lógica

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

    private void AlSeleccionarSaludo()
    {
        if (minijuegoSaludo == null) { Debug.LogWarning("[MinijuegoManager] minijuegoSaludo no asignado."); return; }
        minijuegoSaludo.Iniciar();
    }

    private void AlSeleccionarSenal()
    {
        if (minijuegoSenal == null) { Debug.LogWarning("[MinijuegoManager] minijuegoSenal no asignado."); return; }
        minijuegoSenal.Iniciar();
    }

    private void AlSeleccionarResponder()
    {
        if (minijuegoResponder == null) { Debug.LogWarning("[MinijuegoManager] minijuegoResponder no asignado."); return; }
        minijuegoResponder.Iniciar();
    }

    private void AlSeleccionarCantar()
    {
        if (minijuegoCanto == null) { Debug.LogWarning("[MinijuegoManager] minijuegoCanto no asignado."); return; }
        minijuegoCanto.Iniciar();
    }

    private void Advertir(ParteCuerpo parte)
    {
        Debug.LogWarning($"[MinijuegoManager] El minijuego de {parte} no está asignado en el Inspector.");
    }

    #endregion
}