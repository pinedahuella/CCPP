using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Video;
using UnityEngine.SceneManagement;
using System.Collections;

/// <summary>
/// Al colisionar con el jugador dispara la cinemática final:
/// desactiva objetos → paneles automáticos con fade → video con fade de audio
/// → pantalla de gracias → escena de inicio.
/// </summary>
[RequireComponent(typeof(Collider))]
public class FinalJuego : MonoBehaviour
{
    [Header("Jugador")]
    public JugadorData jugadorData;

    [Header("Objetos a desactivar y activar")]
    public GameObject[] objetosADesactivar;
    public GameObject[] objetosAActivar;

    [Header("Fade")]
    [Tooltip("Image negra que cubre toda la pantalla para los fades")]
    public Image imagenNegra;
    [Tooltip("Velocidad del fade in/out")]
    public float velocidadFade = 2f;

    [Header("Paneles finales")]
    public GameObject[] paneles;
    [Tooltip("Segundos que se muestra cada panel ya visible")]
    public float tiempoPorPanel = 3f;

    [Header("Video")]
    public VideoPlayer videoPlayer;
    public AudioSource audioVideo;
    [Tooltip("Segundos antes del fin del video en que empieza el fade de audio")]
    public float tiempoFadeAntesDeFin = 3f;

    [Header("Pantalla final")]
    public GameObject panelGracias;
    public float tiempoPantallaGracias = 3f;

    [Header("Escena de inicio")]
    public string nombreEscenaInicio = "Inicio";

    private bool _disparado = false;

    // ──────────────────────────────────────────────────────────────
    #region Unity Callbacks

    private void Awake()
    {
        GetComponent<Collider>().isTrigger = true;

        if (paneles != null)
            foreach (GameObject p in paneles)
                if (p != null) p.SetActive(false);

        if (panelGracias != null) panelGracias.SetActive(false);

        // Imagen negra empieza transparente
        if (imagenNegra != null)
        {
            imagenNegra.gameObject.SetActive(true);
            SetAlphaNegra(0f);
        }
    }

    private void OnTriggerEnter(Collider other)
    {
        if (_disparado) return;
        if (!other.CompareTag("Player")) return;

        _disparado = true;
        StartCoroutine(SecuenciaFinal());
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Secuencia Final

    private IEnumerator SecuenciaFinal()
    {
        // 1 — Bloquear jugador
        if (jugadorData != null) jugadorData.puedeMoverse = false;

        // 2 — Fade in negro inicial
        yield return StartCoroutine(FadeNegra(0f, 1f));

        // 3 — Desactivar / activar objetos
        if (objetosADesactivar != null)
            foreach (GameObject obj in objetosADesactivar)
                if (obj != null) obj.SetActive(false);

        if (objetosAActivar != null)
            foreach (GameObject obj in objetosAActivar)
                if (obj != null) obj.SetActive(true);

        // 4 — Paneles automáticos
        yield return StartCoroutine(MostrarPaneles());

        // 5 — Video
        yield return StartCoroutine(ReproducirVideo());

        // 6 — Fade in negro antes de gracias
        yield return StartCoroutine(FadeNegra(0f, 1f));

        // 7 — Pantalla de gracias
        if (panelGracias != null) panelGracias.SetActive(true);
        yield return StartCoroutine(FadeNegra(1f, 0f));
        yield return new WaitForSeconds(tiempoPantallaGracias);

        // 8 — Fade out final y cargar escena
        yield return StartCoroutine(FadeNegra(0f, 1f));
        SceneManager.LoadScene(nombreEscenaInicio);
    }

    private IEnumerator MostrarPaneles()
    {
        if (paneles == null) yield break;

        foreach (GameObject panel in paneles)
        {
            if (panel == null) continue;

            // Fade out negro → mostrar panel
            panel.SetActive(true);
            yield return StartCoroutine(FadeNegra(1f, 0f));

            // Esperar tiempo visible
            yield return new WaitForSeconds(tiempoPorPanel);

            // Fade in negro → ocultar panel
            yield return StartCoroutine(FadeNegra(0f, 1f));
            panel.SetActive(false);
        }
    }

    private IEnumerator ReproducirVideo()
    {
        if (videoPlayer == null) yield break;

        videoPlayer.gameObject.SetActive(true);
        videoPlayer.Play();

        yield return new WaitUntil(() => videoPlayer.isPrepared);

        // Fade out negro para revelar video
        yield return StartCoroutine(FadeNegra(1f, 0f));

        float duracion = (float)videoPlayer.length;
        float tiempoEsperaAntesFade = duracion - tiempoFadeAntesDeFin;

        if (tiempoEsperaAntesFade > 0f)
            yield return new WaitForSeconds(tiempoEsperaAntesFade);

        // Fade de audio mientras termina el video
        if (audioVideo != null)
        {
            float volumenInicial = audioVideo.volume;
            float tiempoTranscurrido = 0f;

            while (tiempoTranscurrido < tiempoFadeAntesDeFin)
            {
                tiempoTranscurrido += Time.deltaTime;
                float t = Mathf.Clamp01(tiempoTranscurrido / tiempoFadeAntesDeFin);
                audioVideo.volume = Mathf.Lerp(volumenInicial, 0f, t);
                yield return null;
            }

            audioVideo.volume = 0f;
        }
        else
        {
            yield return new WaitUntil(() => !videoPlayer.isPlaying);
        }

        videoPlayer.Stop();
        videoPlayer.gameObject.SetActive(false);
    }

    #endregion

    // ──────────────────────────────────────────────────────────────
    #region Fade

    private IEnumerator FadeNegra(float desde, float hasta)
    {
        if (imagenNegra == null) yield break;

        float tiempoTranscurrido = 0f;
        float duracion = Mathf.Abs(hasta - desde) / velocidadFade;

        while (tiempoTranscurrido < duracion)
        {
            tiempoTranscurrido += Time.deltaTime;
            float t = Mathf.Clamp01(tiempoTranscurrido / duracion);
            SetAlphaNegra(Mathf.Lerp(desde, hasta, t));
            yield return null;
        }

        SetAlphaNegra(hasta);
    }

    private void SetAlphaNegra(float alpha)
    {
        if (imagenNegra == null) return;
        Color c = imagenNegra.color;
        c.a = alpha;
        imagenNegra.color = c;
    }

    #endregion
}