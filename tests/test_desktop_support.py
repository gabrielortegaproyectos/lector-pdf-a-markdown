from pathlib import Path

from pdf_to_md_app.desktop_support import (
    default_streamlit_flags,
    get_streamlit_app_path,
    reserve_free_port,
)


def test_default_streamlit_flags_use_embedded_localhost_defaults() -> None:
    flags = default_streamlit_flags(8765)

    assert flags["server.port"] == 8765
    assert flags["server.address"] == "127.0.0.1"
    assert flags["server.headless"] is True
    assert flags["server.fileWatcherType"] == "none"


def test_get_streamlit_app_path_points_to_project_app() -> None:
    app_path = get_streamlit_app_path(Path.cwd())
    assert app_path == Path.cwd() / "app.py"


def test_reserve_free_port_returns_positive_integer() -> None:
    port = reserve_free_port()
    assert isinstance(port, int)
    assert port > 0
