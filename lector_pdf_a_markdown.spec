# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

project_root = Path.cwd()

datas = [
    (str(project_root / "app.py"), "."),
    (str(project_root / "assets"), "assets"),
    (str(project_root / ".streamlit"), ".streamlit"),
]

hiddenimports = [
    "streamlit.web.bootstrap",
    "streamlit.runtime.caching",
    "streamlit.web.server",
    "pdf_to_md_app",
]

analysis = Analysis(
    ["src/pdf_to_md_app/desktop.py"],
    pathex=[str(project_root / "src"), str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(analysis.pure)

exe = EXE(
    pyz,
    analysis.scripts,
    [],
    exclude_binaries=True,
    name="Lector PDF a Markdown",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

app = BUNDLE(
    exe,
    name="Lector PDF a Markdown.app",
    icon=None,
    bundle_identifier="cl.automatika.lectorpdfmarkdown",
    info_plist={
        "CFBundleName": "Lector PDF a Markdown",
        "CFBundleDisplayName": "Lector PDF a Markdown",
        "CFBundleShortVersionString": "0.1.0",
        "CFBundleVersion": "0.1.0",
        "NSHighResolutionCapable": True,
        "LSApplicationCategoryType": "public.app-category.productivity",
    },
)

coll = COLLECT(
    exe,
    analysis.binaries,
    analysis.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="Lector PDF a Markdown",
)
