# Lector PDF a Markdown

Aplicacion de Streamlit para convertir archivos PDF a Markdown, pensada para una experiencia simple, profesional y lista para desplegar en Streamlit Community Cloud.

## Qué hace

- Recibe un archivo PDF desde la interfaz.
- Envía el documento a un servicio externo para obtener Markdown.
- Muestra una vista previa del resultado.
- Permite descargar el archivo `.md`.
- Si el servicio detecta imágenes exportables, muestra enlaces para descargarlas.
- Ofrece un PDF de muestra local y cuatro PDFs públicos para probar la aplicación.
- Aplica un límite diario de 900 páginas para cuidar el cupo disponible del servicio.

## Requisitos

- Python `3.11`
- `uv` instalado
- `LLAMA_CLOUD_API_KEY`

## Ejecutar en local con uv

```bash
uv sync
uv run streamlit run app.py
```

La credencial del servidor debe configurarse con el nombre `LLAMA_CLOUD_API_KEY`.

## Estructura principal

- `app.py`: interfaz Streamlit.
- `src/pdf_to_md_app/converter.py`: integración del servicio de conversión PDF a Markdown.
- `src/pdf_to_md_app/utils.py`: helpers para nombre de salida y métricas.
- `.streamlit/config.toml`: tema visual base.
- `assets/sample.pdf`: PDF de muestra incluido en el repositorio.

## Cómo probar la app

Tienes tres opciones:

1. Subir tu propio PDF.
2. Descargar el archivo local [`assets/sample.pdf`](assets/sample.pdf) y volver a subirlo a la app.
3. Descargar cualquiera de estos PDFs públicos de prueba:

- [Visual Learning Analytics for Educational Interventions in Primary and Secondary Schools: A Scoping Review](https://files.eric.ed.gov/fulltext/EJ1441290.pdf)
- [A Systematic Review of Learning Analytics-Incorporated Instructional Interventions on Learning Management Systems](https://files.eric.ed.gov/fulltext/EJ1441187.pdf)
- [Effectiveness of a Learning Analytics Dashboard for Increasing Student Engagement Levels](https://files.eric.ed.gov/fulltext/EJ1411453.pdf)
- [Visualizing Data to Support Judgement, Inference, and Decision Making in Learning Analytics: Insights from Cognitive Psychology and Visualization Science](https://files.eric.ed.gov/fulltext/EJ1187510.pdf)

## Despliegue en Streamlit Community Cloud

1. Sube este proyecto a un repositorio publico en GitHub.
2. Entra a Streamlit Community Cloud y crea una nueva app conectando ese repositorio.
3. Usa `app.py` como archivo principal.
4. Streamlit detectara `requirements.txt` para instalar dependencias.
5. Configura `LLAMA_CLOUD_API_KEY` en los secrets de la app.
6. Si quieres reproducir el entorno localmente, sigue usando `uv sync` y `uv run`.

## Notas importantes

- Se fija Python `3.11` para mantener un entorno estable en desarrollo y despliegue.
- Esta version depende de una credencial configurada en el servidor y de conectividad externa.
- La app aplica un límite diario visible de 900 páginas y muestra el cupo restante del día.
- Si el servicio devuelve imágenes exportables, la interfaz muestra enlaces de descarga.
- Si la conversion falla, revisa primero que el secret del servidor este configurado y que el servicio tenga disponibilidad.
