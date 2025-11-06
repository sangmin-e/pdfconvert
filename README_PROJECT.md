# Sangmin's PDF 변환기

OpenDataLoader-PDF를 활용한 PDF 변환기 GUI 애플리케이션입니다.

PDF 파일을 Markdown, HTML, JSON 형식으로 변환할 수 있는 사용자 친화적인 Windows GUI 애플리케이션입니다.

## 🌟 주요 기능

- 📝 **Markdown 변환** - PDF를 Markdown 형식으로 변환
- 🌐 **HTML 변환** - PDF를 HTML 형식으로 변환  
- 📄 **JSON 변환** - PDF를 JSON 형식으로 변환
- 🎨 **직관적인 GUI** - tkinter 기반의 깔끔한 인터페이스
- ⚡ **실시간 진행 상황** - 진행 바와 상태 레이블로 변환 진행 상황 확인
- 🔄 **비동기 처리** - 변환 중에도 UI가 멈추지 않음

## 📋 사전 요구사항

### 필수
- **Java 11 이상** 필수
  - 다운로드: https://adoptium.net/ (권장)
  - 또는: https://www.oracle.com/java/technologies/downloads/
  - 설치 후 시스템 PATH에 Java가 포함되어 있어야 합니다

- **Windows 10 이상**

## 🚀 사용 방법

### exe 파일 실행

1. `dist/Sangmin's PDF 변환기.exe` 파일을 다운로드
2. 더블클릭하여 실행
3. "파일 선택" 버튼을 클릭하여 PDF 파일 선택
4. 원하는 형식 버튼 클릭 (Markdown, HTML, JSON)

### Python으로 실행

```bash
# 1. 필요한 패키지 설치
pip install -r requirements_gui.txt

# 2. GUI 앱 실행
python pdf_converter_gui.py
```

## 📁 변환된 파일 위치

변환된 파일은 **원본 PDF 파일과 같은 폴더**에 저장됩니다.

예시:
- 원본: `C:\Documents\문서.pdf`
- 변환: `C:\Documents\문서.md` (또는 .html, .json)

## 🔧 빌드 방법

### exe 파일 빌드

```bash
python build_exe.py
```

또는 PyInstaller 직접 사용:

```bash
python -m PyInstaller build_exe.spec --clean
```

빌드된 exe 파일은 `dist/` 폴더에 생성됩니다.

## 📦 배포 파일

배포 시 다음 파일만 전달하면 됩니다:
- `dist/Sangmin's PDF 변환기.exe`
- `배포_README.txt` (사용 설명서)

**중요:** 사용자 PC에 Java 11 이상이 설치되어 있어야 합니다.

## 🛠️ 개발

### 프로젝트 구조

```
pdf_converter_gui.py      # GUI 애플리케이션 메인 파일
build_exe.py              # exe 빌드 스크립트
build_exe.spec            # PyInstaller 설정 파일
requirements_gui.txt      # Python 패키지 의존성
```

### 의존성

- `opendataloader-pdf` - PDF 변환 엔진
- `pyinstaller` - exe 파일 빌드용

## 📝 참고사항

- 변환 중 CMD 검정 화면이 나타날 수 있으나 정상적인 변환 과정입니다
- 변환된 파일은 원본 PDF와 같은 폴더에 저장됩니다
- Java가 설치되어 있지 않으면 변환이 실패합니다

## 📄 라이선스

이 프로젝트는 OpenDataLoader-PDF 오픈소스를 기반으로 제작되었습니다.

OpenDataLoader-PDF: Mozilla Public License 2.0

## 🙏 감사의 말

- [OpenDataLoader-PDF](https://github.com/opendataloader-project/opendataloader-pdf) 프로젝트에 감사드립니다.

