from __future__ import annotations
from pathlib import Path

import streamlit as st

from pdf_to_md_app.converter import DEFAULT_LLAMA_CLOUD_API_KEY, convert_pdf_to_markdown, get_pdf_page_count
from pdf_to_md_app.usage import DAILY_PAGE_LIMIT, can_process_pages, get_remaining_pages, register_processed_pages

TEST_PDFS = [
    (
        "Visual Learning Analytics for Educational Interventions in Primary and Secondary Schools: A Scoping Review",
        "https://files.eric.ed.gov/fulltext/EJ1441290.pdf",
    ),
    (
        "A Systematic Review of Learning Analytics-Incorporated Instructional Interventions on Learning Management Systems",
        "https://files.eric.ed.gov/fulltext/EJ1441187.pdf",
    ),
    (
        "Effectiveness of a Learning Analytics Dashboard for Increasing Student Engagement Levels",
        "https://files.eric.ed.gov/fulltext/EJ1411453.pdf",
    ),
    (
        "Visualizing Data to Support Judgement, Inference, and Decision Making in Learning Analytics: Insights from Cognitive Psychology and Visualization Science",
        "https://files.eric.ed.gov/fulltext/EJ1187510.pdf",
    ),
]


st.set_page_config(
    page_title="Lector PDF a Markdown",
    page_icon=":page_facing_up:",
    layout="wide",
)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --navy: #2F3E63;
            --blue: #4D8CD9;
            --light-blue: #DDE9F9;
            --paper: #F5F7FB;
            --ink: #1E2A44;
            --muted: #64748B;
            --white: #FFFFFF;
            --border: rgba(47, 62, 99, 0.12);
        }

        .stApp {
            background:
                radial-gradient(circle at top right, rgba(77, 140, 217, 0.14), transparent 26%),
                linear-gradient(180deg, #F8FAFD 0%, #EEF3FA 100%);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2.5rem;
        }

        .hero {
            background: linear-gradient(135deg, var(--navy) 0%, #425784 60%, var(--blue) 100%);
            color: var(--white);
            border-radius: 24px;
            padding: 2rem 2rem 1.7rem 2rem;
            box-shadow: 0 22px 50px rgba(30, 42, 68, 0.16);
            margin-bottom: 1.25rem;
        }

        .hero-grid {
            display: grid;
            grid-template-columns: minmax(0, 2.1fr) minmax(220px, 0.9fr);
            gap: 1.25rem;
            align-items: stretch;
        }

        .brand-card {
            display: flex;
            gap: 1rem;
            align-items: center;
        }

        .brand-mark {
            width: 14px;
            align-self: stretch;
            border-radius: 999px;
            background: linear-gradient(180deg, #7EB5F0 0%, #E0ECFB 100%);
        }

        .brand-copy small {
            display: block;
            letter-spacing: 0.32em;
            text-transform: uppercase;
            opacity: 0.78;
            font-size: 0.72rem;
            margin-bottom: 0.4rem;
        }

        .brand-copy h1 {
            margin: 0;
            font-size: 2.25rem;
            line-height: 1.08;
        }

        .brand-copy p {
            margin: 0.9rem 0 0 0;
            max-width: 56ch;
            color: rgba(255,255,255,0.88);
            font-size: 1rem;
        }

        .side-note {
            background: rgba(255,255,255,0.12);
            border: 1px solid rgba(255,255,255,0.18);
            border-radius: 20px;
            padding: 1.1rem 1rem;
            backdrop-filter: blur(8px);
        }

        .side-note strong {
            display: block;
            font-size: 0.95rem;
            margin-bottom: 0.45rem;
        }

        .card {
            background: rgba(255,255,255,0.94);
            border: 1px solid var(--border);
            border-radius: 22px;
            padding: 1.2rem 1.15rem;
            box-shadow: 0 14px 30px rgba(30, 42, 68, 0.07);
        }

        .section-title {
            color: var(--navy);
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 0.45rem;
        }

        .section-copy {
            color: var(--muted);
            font-size: 0.95rem;
            margin-bottom: 1rem;
        }

        .preview-shell {
            background: #FCFDFE;
            border: 1px solid rgba(47, 62, 99, 0.08);
            border-radius: 18px;
            padding: 0.4rem;
        }

        .resource-list a {
            text-decoration: none;
        }

        @media (max-width: 900px) {
            .hero-grid {
                grid-template-columns: 1fr;
            }

            .brand-copy h1 {
                font-size: 1.8rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.markdown(
        """
        <section class="hero">
          <div class="hero-grid">
            <div class="brand-card">
              <div class="brand-mark"></div>
              <div class="brand-copy">
                <small>Universidad Bernardo O'Higgins</small>
                <h1>Conversor profesional de PDF a Markdown</h1>
                <p>
                  Sube un PDF, deja que el servidor procese el documento y descarga un archivo Markdown
                  limpio para reutilizarlo en documentación, análisis o publicación.
                </p>
              </div>
            </div>
            <div class="side-note">
              <strong>Experiencia prevista</strong>
              <span>
                La conversión se ejecuta en un servidor para mantener una experiencia más estable
                en el despliegue público.
              </span>
            </div>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def resolve_server_api_key() -> str:
    try:
        if "LLAMA_CLOUD_API_KEY" in st.secrets:
            return str(st.secrets["LLAMA_CLOUD_API_KEY"]).strip()
    except Exception:
        pass
    return DEFAULT_LLAMA_CLOUD_API_KEY


def render_upload_panel() -> st.runtime.uploaded_file_manager.UploadedFile | None:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Carga tu documento</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-copy">Acepta archivos PDF. El procesamiento se realiza en un servidor externo para evitar los límites del hosting.</div>',
        unsafe_allow_html=True,
    )
    uploaded_file = st.file_uploader(
        "Selecciona un PDF",
        type=["pdf"],
        help="La app convierte el archivo a Markdown y te permite descargar el resultado.",
    )
    st.markdown("</div>", unsafe_allow_html=True)
    return uploaded_file


def render_help_panel(sample_pdf_path: Path) -> None:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Cómo probar la aplicación</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-copy">
          Puedes subir tu propio PDF o usar alguno de los recursos sugeridos para validar el flujo completo.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if sample_pdf_path.exists():
        st.download_button(
            "Descargar PDF de muestra del repositorio",
            data=sample_pdf_path.read_bytes(),
            file_name=sample_pdf_path.name,
            mime="application/pdf",
            use_container_width=True,
        )
    else:
        st.info("El PDF de muestra local no se encontró en el repositorio.")

    st.markdown("**PDFs de prueba externos**")
    st.markdown('<div class="resource-list">', unsafe_allow_html=True)
    for title, url in TEST_PDFS:
        st.markdown(f"- [{title}]({url})")
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption("Los enlaces externos abren PDFs públicos para descargar y probar la app.")
    st.markdown("</div>", unsafe_allow_html=True)


def render_result(result_markdown: str, output_filename: str, stats: dict[str, int]) -> None:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Resultado de la conversión</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-copy">Revisa una vista previa del Markdown generado y descárgalo cuando esté listo.</div>',
        unsafe_allow_html=True,
    )

    metric_columns = st.columns(5)
    metric_columns[0].metric("Páginas", stats.get("paginas", 0))
    metric_columns[1].metric("Líneas", stats["lineas"])
    metric_columns[2].metric("Palabras", stats["palabras"])
    metric_columns[3].metric("Caracteres", stats["caracteres"])
    metric_columns[4].metric("Encabezados", stats["encabezados"])

    st.download_button(
        "Descargar Markdown",
        data=result_markdown.encode("utf-8"),
        file_name=output_filename,
        mime="text/markdown",
        use_container_width=True,
    )

    st.markdown('<div class="preview-shell">', unsafe_allow_html=True)
    st.text_area(
        "Vista previa del Markdown",
        value=result_markdown,
        height=420,
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def render_images_panel(images: list[dict[str, str]]) -> None:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Imágenes detectadas</div>', unsafe_allow_html=True)
    if not images:
        st.markdown(
            '<div class="section-copy">El servicio no devolvió imágenes descargables para este documento.</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
        return

    st.markdown(
        '<div class="section-copy">Si el servicio detectó imágenes exportables, puedes descargarlas desde estos enlaces.</div>',
        unsafe_allow_html=True,
    )
    for image in images:
        label = f'{image["filename"]} ({image["category"]})'
        st.markdown(f'- [{label}]({image["url"]})')
    st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    inject_styles()
    render_header()

    left_col, right_col = st.columns([1.25, 0.95], gap="large")
    sample_pdf_path = Path("assets/sample.pdf")
    api_key = resolve_server_api_key()

    with right_col:
        render_help_panel(sample_pdf_path)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Notas operativas</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="section-copy">
              La conversión se realiza en un servidor. El límite diario de esta aplicación es de {DAILY_PAGE_LIMIT} páginas.
              Hoy quedan {get_remaining_pages()} páginas disponibles.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with left_col:
        uploaded_file = render_upload_panel()
        if uploaded_file is None:
            st.info("Cuando subas un PDF, aquí aparecerá la conversión en Markdown.")
        elif not api_key:
            st.error("La aplicación no tiene configurada la credencial del servidor.")
        else:
            uploaded_bytes = uploaded_file.getvalue()
            page_count = get_pdf_page_count(uploaded_bytes)
            remaining_pages = get_remaining_pages()
            if page_count > DAILY_PAGE_LIMIT:
                st.error(
                    f"Este archivo tiene {page_count} páginas y supera el límite diario de {DAILY_PAGE_LIMIT} páginas."
                )
                st.info("El límite diario existe para evitar exceder el cupo disponible del servicio.")
                return
            if not can_process_pages(page_count):
                st.error(
                    f"Hoy quedan {remaining_pages} páginas disponibles y este archivo requiere {page_count}."
                )
                st.info("Ese es el límite diario de la aplicación.")
                return

            st.info(
                f"Este documento tiene {page_count} páginas. Hoy quedan {remaining_pages} páginas disponibles del límite diario de {DAILY_PAGE_LIMIT}."
            )
            try:
                with st.spinner("Procesando el PDF en el servidor y generando el Markdown..."):
                    result = convert_pdf_to_markdown(
                        pdf_bytes=uploaded_bytes,
                        source_filename=uploaded_file.name,
                        api_key=api_key,
                    )
            except Exception as exc:
                st.error(
                    "No fue posible completar la conversión. "
                    "Intenta nuevamente en unos segundos."
                )
                st.exception(exc)
            else:
                usage_state = register_processed_pages(page_count)
                st.success(f"Conversión completada para `{uploaded_file.name}`.")
                st.caption(
                    f"Uso registrado: {usage_state.used_pages}/{DAILY_PAGE_LIMIT} páginas consumidas hoy."
                )
                render_result(result.markdown, result.output_filename, result.stats)
                render_images_panel(result.images)


if __name__ == "__main__":
    main()
