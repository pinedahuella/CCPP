using System.Collections;
using UnityEngine;
using UnityEngine.UI;

/// <summary>
/// Controlador del minijuego de pierna.
/// Genera el orden aleatorio, gestiona los clicks en la cuadricula,
/// actualiza las conexiones visuales y reporta el resultado a MisionesGlobal.
/// </summary>
[RequireComponent(typeof(MinijuegoPiernaData))]
public class MinijuegoPiernaController : MonoBehaviour
{
    private MinijuegoPiernaData _data;

    private RectTransform _posicionCadera;
    private RectTransform _posicionRodilla;
    private RectTransform _posicionPie;

    #region Unity Callbacks

    private void Awake()
    {
        _data = GetComponent<MinijuegoPiernaData>();
    }

    #endregion

    #region API Pública

    /// <summary>
    /// Inicializa y abre el minijuego.
    /// Llamado desde CuerpoUIController cuando el jugador selecciona Piernas.
    /// </summary>
    public void Iniciar()
    {
        if (!ValidarReferencias())
            return;

        LimpiarEstado();
        GenerarOrdenAleatorio();
        ConfigurarImagenesOrden();
        ConfigurarBotonesCeldas();
        OcultarConexiones();

        _data.panelMinijuego.SetActive(true);
    }

    #endregion

    #region Inicialización

    /// <summary>Verifica que el panel y el array de 9 celdas esten asignados en el Inspector.</summary>
    /// <returns>True si las referencias son validas; false si falta alguna.</returns>
    private bool ValidarReferencias()
    {
        if (_data.panelMinijuego == null)
        {
            Debug.LogError("[MinijuegoPiernaController] panelMinijuego no asignado.");
            return false;
        }
        if (_data.celdas == null || _data.celdas.Length != 9)
        {
            Debug.LogError("[MinijuegoPiernaController] Se necesitan exactamente 9 celdas.");
            return false;
        }
        return true;
    }

    /// <summary>
    /// Limpia el estado de celdas y variables del turno anterior.
    /// </summary>
    private void LimpiarEstado()
    {
        _data.turnoActual = 0;
        _posicionCadera = null;
        _posicionRodilla = null;
        _posicionPie = null;

        foreach (CeldaCuadriculaData celda in _data.celdas)
        {
            if (celda != null)
            {
                celda.Limpiar();
                // Agregar estas dos lineas:
                if (celda.boton != null)
                {
                    celda.boton.gameObject.SetActive(true);
                    celda.boton.interactable = true;
                }
            }
        }
    }

    /// <summary>
    /// Mezcla las 3 partes en orden aleatorio usando Fisher-Yates.
    /// </summary>
    private void GenerarOrdenAleatorio()
    {
        PartePierna[] partes = { PartePierna.Cadera, PartePierna.Rodilla, PartePierna.Pie };

        for (int i = partes.Length - 1; i > 0; i--)
        {
            int j = Random.Range(0, i + 1);
            PartePierna temp = partes[i];
            partes[i] = partes[j];
            partes[j] = temp;
        }

        _data.ordenAleatorio = partes;
    }

    /// <summary>
    /// Asigna los sprites al panel de orden y los hace visibles.
    /// </summary>
    private void ConfigurarImagenesOrden()
    {
        for (int i = 0; i < 3; i++)
        {
            UnityEngine.UI.Image img = _data.ObtenerImagenOrden(i);
            if (img == null) continue;

            Sprite sprite = _data.ObtenerSprite(_data.ordenAleatorio[i]);
            img.sprite = sprite;
            img.gameObject.SetActive(true);

            // Transparencia completa = visible
            Color c = img.color;
            c.a = 1f;
            img.color = c;
        }
    }

    /// <summary>
    /// Asigna listeners a los botones de cada celda.
    /// </summary>
    private void ConfigurarBotonesCeldas()
    {
        foreach (CeldaCuadriculaData celda in _data.celdas)
        {
            if (celda == null || celda.boton == null) continue;

            celda.boton.onClick.RemoveAllListeners();

            // Captura local para el lambda
            CeldaCuadriculaData celdaCapturada = celda;
            celda.boton.onClick.AddListener(() => AlClickearCelda(celdaCapturada));
        }
    }

    /// <summary>Desactiva las imagenes de linea entre partes al iniciar para que no se muestren de antemano.</summary>
    private void OcultarConexiones()
    {
        if (_data.lineaCaderaRodilla != null)
            _data.lineaCaderaRodilla.gameObject.SetActive(false);

        if (_data.lineaRodillaPie != null)
            _data.lineaRodillaPie.gameObject.SetActive(false);
    }

    #endregion

    #region Lógica de Clicks

    /// <summary>
    /// Gestiona el click en una celda: coloca la parte en turno, desvanece su imagen de orden,
    /// guarda su posicion para conexiones visuales y avanza el turno.
    /// </summary>
    /// <param name="celda">Celda que el jugador acabo de seleccionar.</param>
    private void AlClickearCelda(CeldaCuadriculaData celda)
    {
        if (celda == null) return;
        if (celda.EstaOcupada) return;
        if (_data.turnoActual >= 3) return;

        PartePierna parteActual = _data.ordenAleatorio[_data.turnoActual];

        // Colocar parte en la celda
        ColocarParteEnCelda(celda, parteActual);

        // Desvanecer imagen del panel de orden
        DesvanecerImagenOrden(_data.turnoActual);

        // Guardar posicion para conexiones
        GuardarPosicion(parteActual, celda.GetComponent<RectTransform>());

        // Actualizar conexiones visuales
        ActualizarConexiones();

        _data.turnoActual++;

        // Si ya se colocaron las 3 partes, esperar y reportar
        if (_data.turnoActual >= 3)
            StartCoroutine(EsperarYReportar());
    }

    /// <summary>
    /// Asigna la parte a la celda y muestra el sprite correspondiente en la imagen de la celda.
    /// </summary>
    /// <param name="celda">Celda donde se coloca la parte.</param>
    /// <param name="parte">Parte de la pierna a colocar.</param>
    private void ColocarParteEnCelda(CeldaCuadriculaData celda, PartePierna parte)
    {
        celda.parteOcupante = parte;

        if (celda.imagenParte != null)
        {
            celda.imagenParte.sprite = _data.ObtenerSprite(parte);
            celda.imagenParte.gameObject.SetActive(true);
        }
    }

    /// <summary>
    /// Reduce el alpha de la imagen del panel de orden al 25% para indicar que esa parte ya fue colocada.
    /// </summary>
    /// <param name="indice">Indice del slot de orden (0-2) a desvanecer.</param>
    private void DesvanecerImagenOrden(int indice)
    {
        UnityEngine.UI.Image img = _data.ObtenerImagenOrden(indice);
        if (img == null) return;

        Color c = img.color;
        c.a = 0.25f;
        img.color = c;
    }

    /// <summary>
    /// Guarda el RectTransform de la celda donde se coloco cada parte
    /// para poder calcular las conexiones visuales entre ellas.
    /// </summary>
    /// <param name="parte">Parte de la pierna que se acaba de colocar.</param>
    /// <param name="rect">RectTransform de la celda donde fue colocada.</param>
    private void GuardarPosicion(PartePierna parte, RectTransform rect)
    {
        switch (parte)
        {
            case PartePierna.Cadera: _posicionCadera = rect; break;
            case PartePierna.Rodilla: _posicionRodilla = rect; break;
            case PartePierna.Pie: _posicionPie = rect; break;
        }
    }

    #endregion

    #region Conexiones Visuales

    /// <summary>
    /// Actualiza posicion y visibilidad de las lineas de conexion
    /// segun que partes ya han sido colocadas.
    /// Usa el punto medio entre dos RectTransform como posicion de la linea
    /// y rota la imagen para apuntar de uno al otro.
    /// </summary>
    private void ActualizarConexiones()
    {
        if (_posicionCadera != null && _posicionRodilla != null)
            ActualizarLinea(_data.lineaCaderaRodilla, _posicionCadera, _posicionRodilla);

        if (_posicionRodilla != null && _posicionPie != null)
            ActualizarLinea(_data.lineaRodillaPie, _posicionRodilla, _posicionPie);
    }

    /// <summary>
    /// Posiciona, rota y redimensiona la imagen de linea para que conecte visualmente dos RectTransforms.
    /// </summary>
    /// <param name="linea">Imagen de linea a actualizar.</param>
    /// <param name="desde">RectTransform de la parte origen.</param>
    /// <param name="hasta">RectTransform de la parte destino.</param>
    private void ActualizarLinea(UnityEngine.UI.Image linea, RectTransform desde, RectTransform hasta)
    {
        if (linea == null || desde == null || hasta == null) return;

        linea.gameObject.SetActive(true);

        RectTransform lineaRect = linea.GetComponent<RectTransform>();
        RectTransform parentRect = lineaRect.parent as RectTransform;

        // Convertir posiciones al espacio local del parent directamente
        Vector2 posDesde = parentRect.InverseTransformPoint(desde.position);
        Vector2 posHasta = parentRect.InverseTransformPoint(hasta.position);

        lineaRect.pivot = new Vector2(0.5f, 0.5f);
        lineaRect.anchoredPosition = (posDesde + posHasta) / 2f;

        Vector2 direccion = posHasta - posDesde;
        float angulo = Mathf.Atan2(direccion.y, direccion.x) * Mathf.Rad2Deg;
        lineaRect.localRotation = Quaternion.Euler(0f, 0f, angulo);

        float distancia = direccion.magnitude;
        lineaRect.localScale = Vector3.one;
        lineaRect.sizeDelta = new Vector2(distancia, 60f);
    }

    #endregion

    #region Reporte

    /// <summary>
    /// Espera el tiempo configurado, cierra el panel y reporta el resultado de postura a MisionesGlobal.
    /// </summary>
    private IEnumerator EsperarYReportar()
    {
        DesactivarBotones();
        yield return new WaitForSeconds(_data.tiempoEspera);
        _data.panelMinijuego.SetActive(false);

        int valorPostura = EvaluarPostura();
        AccionResultado resultado = new AccionResultado(TipoAccion.Postura, valorPostura);

        if (MisionesGlobal.Instancia != null)
            MisionesGlobal.Instancia.ReportarResultado(resultado);
        else
            Debug.LogWarning("[MinijuegoPiernaController] MisionesGlobal no encontrado al reportar.");
    }

    /// <summary>
    /// Desactiva la interaccion de todos los botones de celda sin opacar las imagenes ya colocadas.
    /// </summary>
    private void DesactivarBotones()
    {
        foreach (CeldaCuadriculaData celda in _data.celdas)
        {
            if (celda != null && celda.boton != null)
            {
                celda.boton.onClick.RemoveAllListeners();

                // Mantener color normal para no opacar las imagenes colocadas
                ColorBlock colores = celda.boton.colors;
                colores.disabledColor = Color.white;
                celda.boton.colors = colores;

                celda.boton.interactable = false;
            }
        }
    }

    #endregion


    #region Reporte

    /// <summary>
    /// Evalua la disposicion de las partes de la pierna en la cuadricula
    /// y devuelve el codigo de postura: 1=parado, 2=sentado, 3=arrodillado, 0=no reconocida.
    /// </summary>
    /// <returns>Codigo de postura reconocida o 0 si no coincide con ninguna valida.</returns>
    private int EvaluarPostura()
    {
        // Obtener fila y columna de cada parte
        int cadFila = -1, cadCol = -1;
        int rodFila = -1, rodCol = -1;
        int pieFila = -1, pieCol = -1;

        foreach (CeldaCuadriculaData celda in _data.celdas)
        {
            if (!celda.EstaOcupada) continue;

            switch (celda.parteOcupante.Value)
            {
                case PartePierna.Cadera: cadFila = celda.fila; cadCol = celda.columna; break;
                case PartePierna.Rodilla: rodFila = celda.fila; rodCol = celda.columna; break;
                case PartePierna.Pie: pieFila = celda.fila; pieCol = celda.columna; break;
            }
        }

        // 1 - Parado: misma columna, cadera < rodilla < pie en fila
        if (cadCol == rodCol && rodCol == pieCol &&
            cadFila < rodFila && rodFila < pieFila)
        {
            Debug.Log("[Postura] Parado (1)");
            return 1;
        }

        // 2 - Sentado: pie y rodilla misma columna, rodilla arriba del pie,
        //              cadera misma fila que rodilla distinta columna
        if (pieCol == rodCol && rodFila < pieFila &&
            cadFila == rodFila && cadCol != rodCol)
        {
            Debug.Log("[Postura] Sentado (2)");
            return 2;
        }

        // 3 - Arrodillado: cadera y rodilla misma columna, cadera arriba,
        //                  pie misma fila que rodilla distinta columna
        if (cadCol == rodCol && cadFila < rodFila &&
            pieFila == rodFila && pieCol != rodCol)
        {
            Debug.Log("[Postura] Arrodillado (3)");
            return 3;
        }

        Debug.Log("[Postura] No reconocida (0)");
        return 0;
    }
    #endregion
}