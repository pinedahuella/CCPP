using UnityEngine;

/// <summary>
/// Al colisionar con el jugador lanza un diálogo, bloquea movimiento
/// y al terminar lo reactiva. Se puede repetir al regresar.
/// </summary>
public class ColisionDialogo : MonoBehaviour
{
    [Header("Diálogo")]
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

    private void OnCollisionEnter(Collision other)
    {
        if (_disparado) return;
        if (!other.gameObject.CompareTag("Player")) return;

        if (_dialogoController == null)
        {
            Debug.LogWarning("[ColisionDialogo] No se encontró DialogoController.");
            return;
        }

        _disparado = true;

        if (jugadorData != null) jugadorData.puedeMoverse = false;

        DialogoController.OnDialogoTerminado += AlTerminarDialogo;
        _dialogoController.Iniciar(dialogo);
    }

    private void AlTerminarDialogo()
    {
        DialogoController.OnDialogoTerminado -= AlTerminarDialogo;
        if (jugadorData != null) jugadorData.puedeMoverse = true;
        _disparado = false;
    }
}