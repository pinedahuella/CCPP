using UnityEngine;

/// <summary>
/// Controlador de la camara principal. Lee los datos de CamaraData
/// y mueve la camara suavemente en LateUpdate para que siempre siga
/// al jugador por el eje X sin interferir con Y ni Z.
/// </summary>
[RequireComponent(typeof(CamaraData))]
public class CamaraController : MonoBehaviour
{
    private CamaraData _data;

    private void Awake()
    {
        _data = GetComponent<CamaraData>();
    }

    /// <summary>
    /// Mueve la camara hacia la posicion X del jugador con interpolacion suave.
    /// Se ejecuta en LateUpdate para que el jugador ya haya actualizado su posicion.
    /// </summary>
    private void LateUpdate()
    {
        if (!_data.seguirJugador || _data.jugador == null) return;

        float nuevoX = Mathf.Lerp(transform.position.x, _data.jugador.position.x, _data.velocidadSmooth * Time.deltaTime);
        transform.position = new Vector3(nuevoX, transform.position.y, transform.position.z);
    }
}