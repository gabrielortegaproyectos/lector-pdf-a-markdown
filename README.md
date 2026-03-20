# Lector PDF a Markdown

Aplicacion de Streamlit para convertir archivos PDF a Markdown con `marker-pdf`, pensada para una experiencia simple, profesional y lista para desplegar en Streamlit Community Cloud.

La conversion intenta reducir el pico de memoria procesando el PDF pagina por pagina y concatenando el Markdown final.

## Qué hace

- Recibe un archivo PDF desde la interfaz.
- Convierte el documento a Markdown usando la misma base lógica del notebook original.
- Procesa el PDF pagina por pagina para intentar bajar el pico de RAM.
- Muestra una vista previa del resultado.
- Permite descargar el archivo `.md`.
- Ofrece un PDF de muestra local y cuatro PDFs públicos para probar la aplicación.

## Requisitos

- Python `3.11`
- `uv` instalado

## Ejecutar en local con uv

```bash
uv sync
uv run streamlit run app.py
```

La primera ejecución puede tardar más porque `marker-pdf` necesita preparar sus modelos.

## Empaquetar como app para macOS

Esta opción genera un bundle `.app` con `PyInstaller` para ejecutar la interfaz como aplicación de escritorio en Mac. La app empaquetada levanta Streamlit internamente y abre la interfaz en el navegador por defecto, sin exigir que el usuario use la terminal.

### Requisitos para el build en Mac

- macOS
- Python `3.11`
- `uv` instalado

### Generar el `.app`

```bash
uv sync --extra mac-app
sh scripts/build_macos_app.sh
```

El bundle se generará en:

```text
dist/Lector PDF a Markdown.app
```

### Qué incluye el bundle

- El launcher de escritorio en `src/pdf_to_md_app/desktop.py`
- La app principal `app.py`
- El PDF de muestra en `assets/sample.pdf`
- La configuración visual de `.streamlit/config.toml`

### Notas para distribución en Mac

- El primer arranque puede tardar por la carga de modelos de `marker-pdf`.
- Si vas a distribuir la app a otros usuarios, puede ser necesario firmarla y notarizarla con las herramientas de Apple.
- Aunque sea una app `.app`, el consumo de memoria de `marker-pdf` sigue siendo alto. Un Mac con poca RAM puede sufrir el mismo problema que un hosting gratuito.

## Estructura principal

- `app.py`: interfaz Streamlit.
- `src/pdf_to_md_app/converter.py`: carga de modelos y conversión PDF a Markdown.
- `src/pdf_to_md_app/utils.py`: helpers para nombre de salida y métricas.
- `src/pdf_to_md_app/desktop.py`: launcher para la app de escritorio en macOS.
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
5. Si quieres reproducir el entorno localmente, sigue usando `uv sync` y `uv run`.

## Notas importantes

- Se fija Python `3.11` porque `marker-pdf` puede presentar problemas de instalacion en Python `3.14`.
- En hosting gratuito, la primera carga de modelos puede tardar mas que las siguientes.
- Aunque ahora se procesa pagina por pagina para reducir picos de memoria, `marker-pdf` sigue cargando modelos pesados y puede seguir fallando en entornos con poca RAM.
- Si un PDF muy grande falla por memoria o tiempo, prueba con un documento mas pequeño para confirmar que el flujo funciona.
