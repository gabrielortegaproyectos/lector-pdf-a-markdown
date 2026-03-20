# Lector PDF a Markdown

Aplicacion de Streamlit para convertir archivos PDF a Markdown con `LlamaParse`, pensada para una experiencia simple, profesional y lista para desplegar en Streamlit Community Cloud.

## Qué hace

- Recibe un archivo PDF desde la interfaz.
- Envía el documento a LlamaParse para obtener Markdown sin depender de la RAM local del hosting.
- Muestra una vista previa del resultado.
- Permite descargar el archivo `.md`.
- Ofrece un PDF de muestra local y cuatro PDFs públicos para probar la aplicación.

## Requisitos

- Python `3.11`
- `uv` instalado
- `LLAMA_CLOUD_API_KEY`

## Ejecutar en local con uv

```bash
uv sync
export LLAMA_CLOUD_API_KEY=llx-...
uv run streamlit run app.py
```

Tambien puedes definir la API key como secret en Streamlit Cloud usando el nombre `LLAMA_CLOUD_API_KEY`.

## Estructura principal

- `app.py`: interfaz Streamlit.
- `src/pdf_to_md_app/converter.py`: integración con LlamaParse y conversión PDF a Markdown.
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
- Esta version depende de LlamaParse, asi que requiere internet y una API key valida.
- LlamaParse consume creditos segun el modo usado. Revisa su pricing antes de abrir la app al publico.
- Si la conversion falla, revisa primero que la API key este bien configurada y que el servicio tenga disponibilidad.
