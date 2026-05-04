using System.Collections;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class MainMenuController : MonoBehaviour
{
    [Header("Escena")]
    [Tooltip("Nombre exacto de la escena a cargar (como aparece en Build Settings)")]
    public string sceneName = "GameScene";

    [Header("Fade")]
    public Image fadeImage;
    [Range(0.3f, 3f)]
    public float fadeDuration = 1f;

    public GameObject[] objetosDesactivas;

    // Evita que se presionen los botones dos veces durante el fade
    private bool _isTransitioning = false;

    // ─────────────────────────────────────────────
    //  Botones
    // ─────────────────────────────────────────────

    public void OnPlayButton()
    {
        if (_isTransitioning) return;

        foreach (var item in objetosDesactivas)
        {
                item.SetActive(false);  
        }

        StartCoroutine(FadeAndDo(() => SceneManager.LoadScene(sceneName)));
    }

    public void OnQuitButton()
    {
        if (_isTransitioning) return;

        foreach (var item in objetosDesactivas)
        {
            item.SetActive(false);
        }

        StartCoroutine(FadeAndDo(() =>
        {
#if UNITY_EDITOR
            UnityEditor.EditorApplication.isPlaying = false;
#else
            Application.Quit();
#endif
        }));
    }

    // ─────────────────────────────────────────────
    //  Fade
    // ─────────────────────────────────────────────

    private IEnumerator FadeAndDo(System.Action onComplete)
    {
        _isTransitioning = true;

        // Activar imagen y asegurarse que empieza en alfa 0
        fadeImage.gameObject.SetActive(true);
        SetAlpha(0f);

        float elapsed = 0f;

        while (elapsed < fadeDuration)
        {
            elapsed += Time.deltaTime;
            SetAlpha(Mathf.Clamp01(elapsed / fadeDuration));
            yield return null;
        }

        SetAlpha(1f);

        // Acción: cargar escena o salir
        onComplete?.Invoke();
    }

    private void SetAlpha(float alpha)
    {
        Color c = fadeImage.color;
        c.a = alpha;
        fadeImage.color = c;
    }
}