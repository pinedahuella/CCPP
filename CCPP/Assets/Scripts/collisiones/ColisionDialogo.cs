using UnityEngine;

/// <summary>
/// Al colisionar con el jugador lanza un dialogo, bloquea movimiento
/// y al terminar lo reactiva. Se puede repetir al regresar.
/// </summary>
public class ColisionDialogo : MonoBehaviour
{
    [Header("Dialogo")]
    public DialogoData dialogo;

    [Header("Jugador")]
    public JugadorData jugadorData;

    private DialogoController _dialogoController;
    private bool _disparado = false;

    private void Awake()
    {
        _dialogoController = FindFirstObjectByType<DialogoController>();
        jugadorData = FindFirstObjectByType<JugadorData>();
    }

    /// <summary>
    /// Al colisionar con el jugador inicia el dialogo y bloquea el movimiento.
    /// Se ignora si ya hay un dialogo activo en este trigger.
    /// </summary>
    private void OnCollisionEnter(Collision other)
    {
        if (_disparado) return;
        if (!other.gameObject.CompareTag("Player")) return;

        if (_dialogoController == null)
        {
            Debug.LogWarning("[ColisionDialogo] No se encontro DialogoController.");
            return;
        }

        _disparado = true;

        if (jugadorData != null) jugadorData.puedeMoverse = false;

        DialogoController.OnDialogoTerminado += AlTerminarDialogo;
        _dialogoController.Iniciar(dialogo);
    }

    /// <summary>
    /// Se llama al terminar el dialogo: desuscribe el handler,
    /// reactiva el movimiento del jugador y permite disparar el dialogo de nuevo.
    /// </summary>
    private void AlTerminarDialogo()
    {
        DialogoController.OnDialogoTerminado -= AlTerminarDialogo;
        if (jugadorData != null) jugadorData.puedeMoverse = true;
        _disparado = false;
    }
}