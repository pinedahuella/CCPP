using UnityEngine;

/// <summary>
/// Al entrar el jugador al trigger desactiva un GameObject específico.
/// Solo se dispara una vez.
/// </summary>
[RequireComponent(typeof(Collider))]
public class TriggerDesactivarObjeto : MonoBehaviour
{
    [Tooltip("Objeto a desactivar al entrar el jugador")]
    public GameObject objetoADesactivar;

    private void Awake()
    {
        GetComponent<Collider>().isTrigger = true;
    }

    private void OnTriggerEnter(Collider other)
    {
        if (!other.CompareTag("Player")) return;
        if (objetoADesactivar == null) return;

        objetoADesactivar.SetActive(false);
        this.enabled = false;
    }
}