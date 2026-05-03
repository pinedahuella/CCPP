using UnityEngine;

/// <summary>
/// Contenedor de una conversacion completa.
/// Clase serializable, se rellena inline en el Inspector.
/// Sin logica, solo datos.
/// </summary>
[System.Serializable]
public class DialogoData
{
    [Tooltip("Lista de líneas de esta conversación en orden")]
    public DialogoLinea[] lineas;
}