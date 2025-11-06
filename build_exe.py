#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 변환기 GUI 앱을 exe로 빌드하는 스크립트

사용법:
    python build_exe.py
"""

import subprocess
import sys
import os
from pathlib import Path

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def check_pyinstaller():
    """PyInstaller가 설치되어 있는지 확인"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def install_pyinstaller():
    """PyInstaller 설치"""
    print("PyInstaller 설치 중...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def check_opendataloader():
    """opendataloader-pdf가 설치되어 있는지 확인"""
    try:
        import opendataloader_pdf
        return True
    except ImportError:
        return False

def install_opendataloader():
    """opendataloader-pdf 설치"""
    print("opendataloader-pdf 설치 중...")
    
    # 프로젝트 내의 Python 패키지가 있는지 확인
    python_pkg_path = Path("python/opendataloader-pdf")
    if python_pkg_path.exists():
        print("로컬 opendataloader-pdf 패키지 설치 중...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-e", str(python_pkg_path)
        ])
    else:
        print("PyPI에서 opendataloader-pdf 설치 중...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "opendataloader-pdf"
        ])

def build_exe():
    """exe 파일 빌드"""
    print("\n" + "="*60)
    print("PDF Converter GUI App Build Start")
    print("="*60 + "\n")
    
    # 1. 필요한 패키지 확인 및 설치
    if not check_pyinstaller():
        install_pyinstaller()
    
    if not check_opendataloader():
        install_opendataloader()
    
    # 2. PyInstaller로 빌드
    print("\nBuilding exe file with PyInstaller...")
    print("-" * 60)
    
    spec_file = Path("build_exe.spec")
    if spec_file.exists():
        cmd = [sys.executable, "-m", "PyInstaller", str(spec_file), "--clean"]
    else:
        # spec 파일이 없으면 기본 옵션으로 빌드
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",  # 콘솔 창 숨김
            "--name=PDF변환기",
            "--hidden-import=opendataloader_pdf",
            "--hidden-import=opendataloader_pdf.wrapper",
            "pdf_converter_gui.py"
        ]
    
    try:
        subprocess.check_call(cmd)
        print("\n" + "="*60)
        print("Build Complete!")
        print("="*60)
        print(f"\nExe file location: dist/PDF변환기.exe")
        print("\nYou can now run the exe file!")
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()


