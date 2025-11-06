# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller 설정 파일
PDF 변환기 GUI 앱을 exe로 빌드합니다.
"""

import os
import sys
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files

# opendataloader_pdf 패키지의 데이터 파일 자동 수집
datas = collect_data_files('opendataloader_pdf')

block_cipher = None

a = Analysis(
    ['pdf_converter_gui.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'opendataloader_pdf',
        'opendataloader_pdf.wrapper',
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
        'tkinter.ttk',
        'importlib.resources',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    collect_submodules=['opendataloader_pdf'],
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="Sangmin's PDF 변환기",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI 앱이므로 콘솔 창 숨김
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 아이콘 파일이 있다면 여기에 경로 지정
)


