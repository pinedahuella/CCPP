using UnityEngine;

[RequireComponent(typeof(CamaraData))]
public class CamaraController : MonoBehaviour
{
    private CamaraData _data;

    private void Awake()
    {
        _data = GetComponent<CamaraData>();
    }

    private void LateUpdate()
    {
        if (!_data.seguirJugador || _data.jugador == null) return;

        float nuevoX = Mathf.Lerp(transform.position.x, _data.jugador.position.x, _data.velocidadSmooth * Time.deltaTime);
        transform.position = new Vector3(nuevoX, transform.position.y, transform.position.z);
    }
}