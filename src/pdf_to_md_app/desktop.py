from __future__ import annotations

import threading
import time
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path

from streamlit.web import bootstrap

from pdf_to_md_app.desktop_support import (
    configure_desktop_environment,
    default_streamlit_flags,
    get_streamlit_app_path,
    reserve_free_port,
)


HEALTH_TIMEOUT_SECONDS = 120
HEALTH_POLL_INTERVAL_SECONDS = 0.5


def show_startup_error(message: str) -> None:
    """Display a simple GUI error dialog if possible."""
    try:
        import tkinter
        from tkinter import messagebox

        root = tkinter.Tk()
        root.withdraw()
        messagebox.showerror("Lector PDF a Markdown", message)
        root.destroy()
    except Exception:
        print(message)


def wait_for_streamlit(url: str, timeout_seconds: int = HEALTH_TIMEOUT_SECONDS) -> bool:
    """Poll the Streamlit health endpoint until it responds or times out."""
    deadline = time.time() + timeout_seconds
    health_url = f"{url}/healthz"
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(health_url, timeout=2) as response:
                if response.status == 200:
                    return True
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            time.sleep(HEALTH_POLL_INTERVAL_SECONDS)
    return False


def run_embedded_streamlit(app_path: Path, port: int) -> None:
    """Start Streamlit in-process using the project entrypoint."""
    bootstrap.run(
        str(app_path),
        is_hello=False,
        args=[],
        flag_options=default_streamlit_flags(port),
    )


def main() -> None:
    configure_desktop_environment()

    app_path = get_streamlit_app_path()
    if not app_path.exists():
        show_startup_error(
            "No se encontró el archivo principal de la aplicación. "
            "Vuelve a generar el bundle de macOS y prueba otra vez."
        )
        raise SystemExit(1)

    port = reserve_free_port()
    url = f"http://127.0.0.1:{port}"

    server_thread = threading.Thread(
        target=run_embedded_streamlit,
        args=(app_path, port),
        daemon=False,
        name="streamlit-desktop-server",
    )
    server_thread.start()

    if not wait_for_streamlit(url):
        show_startup_error(
            "La aplicación no logró iniciar a tiempo. "
            "Es posible que el modelo necesite más memoria o más tiempo de carga."
        )
        raise SystemExit(1)

    webbrowser.open(url)
    server_thread.join()


if __name__ == "__main__":
    main()
