from __future__ import annotations

import os
import socket
import sys
from pathlib import Path


def get_bundle_root() -> Path:
    """Return the project root in development or the extracted bundle root when frozen."""
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS"))
    return Path(__file__).resolve().parents[2]


def get_streamlit_app_path(bundle_root: Path | None = None) -> Path:
    """Resolve the bundled Streamlit entrypoint path."""
    root = bundle_root or get_bundle_root()
    return root / "app.py"


def reserve_free_port(host: str = "127.0.0.1") -> int:
    """Reserve an ephemeral localhost port for the embedded Streamlit server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        sock.listen(1)
        return int(sock.getsockname()[1])


def default_streamlit_flags(port: int) -> dict[str, object]:
    """Return Streamlit runtime flags for the embedded desktop launcher."""
    return {
        "server.port": port,
        "server.address": "127.0.0.1",
        "server.headless": True,
        "server.fileWatcherType": "none",
        "browser.gatherUsageStats": False,
        "global.developmentMode": False,
    }


def configure_desktop_environment() -> None:
    """Set runtime env vars that make the bundled desktop app quieter and more stable."""
    os.environ.setdefault("STREAMLIT_SERVER_HEADLESS", "true")
    os.environ.setdefault("STREAMLIT_BROWSER_GATHER_USAGE_STATS", "false")
    os.environ.setdefault("STREAMLIT_SERVER_FILE_WATCHER_TYPE", "none")
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
