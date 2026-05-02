using UnityEngine;

/// <summary>
/// Contenedor de una conversación completa.
/// Clase serializable, se rellena inline en el Inspector.
/// Sin lógica, solo datos.
/// </summary>
[System.Serializable]
public class DialogoData
{
    [Tooltip("Lista de líneas de esta conversación en orden")]
    public DialogoLinea[] lineas;
}