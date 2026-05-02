Shader "Custom/SpriteWindSway"
{
    Properties
    {
        _MainTex        ("Sprite Texture", 2D)  = "white" {}
        _Color          ("Tint", Color)          = (1,1,1,1)

        [Header(Wind)]
        _WindStrength   ("Strength",   Range(0, 0.15)) = 0.03
        _WindSpeed      ("Speed",      Range(0, 5))    = 1.2
        _WindFrequency  ("Frequency",  Range(0, 10))   = 2.5
        _WindGust       ("Gust",       Range(0, 1))    = 0.4
        _RootHeight     ("Root Height (UV Y)", Range(0, 1)) = 0.1
    }

    SubShader
    {
        Tags
        {
            "Queue"           = "Transparent"
            "RenderType"      = "Transparent"
            "RenderPipeline"  = "UniversalPipeline"
            "IgnoreProjector" = "True"
        }

        Blend SrcAlpha OneMinusSrcAlpha
        Cull   Off
        Lighting Off
        ZWrite On
        ZTest  LEqual

        Pass
        {
            Name "SpriteWindSway"
            Tags { "LightMode" = "Universal2D" }

            HLSLPROGRAM
            #pragma vertex   vert
            #pragma fragment frag
            #pragma multi_compile_instancing

            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

            // ─── Estructuras ──────────────────────────────────────────────
            struct Attributes
            {
                float4 positionOS : POSITION;
                float2 uv         : TEXCOORD0;
                float4 color      : COLOR;
                UNITY_VERTEX_INPUT_INSTANCE_ID
            };

            struct Varyings
            {
                float4 positionHCS : SV_POSITION;
                float2 uv          : TEXCOORD0;
                float4 color       : COLOR;
                UNITY_VERTEX_OUTPUT_STEREO
            };

            // ─── Texturas ─────────────────────────────────────────────────
            TEXTURE2D(_MainTex);
            SAMPLER(sampler_MainTex);
            float4 _MainTex_ST;

            // ─── CBuffer (SRP Batcher compatible) ────────────────────────
            CBUFFER_START(UnityPerMaterial)
                float4 _Color;
                float  _WindStrength;
                float  _WindSpeed;
                float  _WindFrequency;
                float  _WindGust;
                float  _RootHeight;
            CBUFFER_END

            // ─── Función de viento ────────────────────────────────────────
            //  Devuelve desplazamiento X en espacio objeto.
            //  uvY  → 0 = raíz (sin movimiento), 1 = punta (máx movimiento)
            float WindOffset(float uvY, float2 worldXZ)
            {
                float t = _Time.y * _WindSpeed;

                // Ola primaria (movimiento principal de la brisa)
                float wave1 = sin(t * _WindFrequency + worldXZ.x * 0.7);

                // Ola secundaria (micro-vibración de hoja, frecuencia más alta)
                float wave2 = sin(t * _WindFrequency * 2.7 + worldXZ.x * 1.3) * 0.3;

                // Ráfaga: impulso lento que varía la intensidad (sensación de viento variable)
                float gust  = (sin(t * 0.4 + worldXZ.x * 0.2) * 0.5 + 0.5) * _WindGust;

                float wind  = (wave1 + wave2) * (1.0 + gust);

                // Factor de influencia: 0 en la raíz, 1 en la punta (curva cuadrática)
                float influence = saturate((uvY - _RootHeight) / (1.0 - _RootHeight));
                influence = influence * influence;   // curvatura suave

                return wind * _WindStrength * influence;
            }

            // ─── Vertex shader ────────────────────────────────────────────
            Varyings vert(Attributes IN)
            {
                Varyings OUT;
                UNITY_SETUP_INSTANCE_ID(IN);
                UNITY_INITIALIZE_VERTEX_OUTPUT_STEREO(OUT);

                // UV transformada (para leer uvY correctamente antes de ST)
                float2 rawUV = IN.uv;

                // Posición mundo para fase espacial del viento
                float3 worldPos = TransformObjectToWorld(IN.positionOS.xyz);

                // Calcular desplazamiento y aplicarlo en espacio objeto (solo eje X)
                float dx = WindOffset(rawUV.y, worldPos.xz);
                IN.positionOS.x += dx;

                OUT.positionHCS = TransformObjectToHClip(IN.positionOS.xyz);
                OUT.uv          = TRANSFORM_TEX(rawUV, _MainTex);
                OUT.color       = IN.color * _Color;
                return OUT;
            }

            // ─── Fragment shader ──────────────────────────────────────────
            half4 frag(Varyings IN) : SV_Target
            {
                half4 texColor   = SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, IN.uv);
                half4 finalColor = texColor * IN.color;
                clip(finalColor.a - 0.01);
                return finalColor;
            }

            ENDHLSL
        }
    }

    FallBack "Sprites/Default"
}