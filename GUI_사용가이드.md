# PDF 변환기 GUI 앱 사용 가이드

OpenDataLoader-PDF를 활용한 PDF 변환기 GUI 애플리케이션입니다.

## 📋 기능

- PDF 파일을 선택하여 변환
- 3가지 형식으로 변환 가능:
  - 📝 **Markdown** (.md)
  - 🌐 **HTML** (.html)
  - 📄 **JSON** (.json)
- 변환 진행 상황 실시간 확인
- 변환된 파일 자동 저장

## 🚀 실행 방법

### 방법 1: Python으로 직접 실행

```bash
# 1. 필요한 패키지 설치
pip install -r requirements_gui.txt

# 또는 개발 환경에서 opendataloader-pdf 설치
cd python/opendataloader-pdf
pip install -e .
cd ../..

# 2. GUI 앱 실행
python pdf_converter_gui.py
```

### 방법 2: exe 파일로 실행

```bash
# 1. exe 파일 빌드
python build_exe.py

# 2. 빌드된 exe 파일 실행
# dist/PDF변환기.exe 파일을 더블클릭하여 실행
```

## 📖 사용법

1. **PDF 파일 선택**
   - "파일 선택" 버튼을 클릭
   - 변환할 PDF 파일을 선택

2. **변환 형식 선택**
   - 원하는 버튼 클릭:
     - 📝 **Markdown으로 변환** (녹색 버튼)
     - 🌐 **HTML로 변환** (파란색 버튼)
     - 📄 **JSON으로 변환** (주황색 버튼)

3. **결과 확인**
   - 변환 완료 후 메시지 창이 표시됩니다
   - 변환된 파일은 PDF 파일과 같은 폴더에 저장됩니다
   - 로그 영역에서 변환 진행 상황을 확인할 수 있습니다

## 📁 출력 파일 위치

변환된 파일은 **원본 PDF 파일과 같은 폴더**에 저장됩니다.

예시:
```
원본 파일: C:\Documents\report.pdf
변환 파일: C:\Documents\report.md (또는 .html, .json)
```

## ⚙️ 사전 요구사항

### 필수

1. **Java 11 이상**
   - 다운로드: https://adoptium.net/ (권장)
   - 또는 https://www.oracle.com/java/technologies/downloads/
   - 설치 후 시스템 PATH에 Java가 포함되어 있어야 합니다

2. **Python 3.9 이상**
   - GUI 앱 실행 시 필요

### Python 패키지

```bash
pip install -r requirements_gui.txt
```

또는 개별 설치:
```bash
pip install opendataloader-pdf pyinstaller
```

## 🔧 exe 파일 빌드

### 자동 빌드 스크립트 사용

```bash
python build_exe.py
```

이 스크립트는:
- 필요한 패키지를 자동으로 확인 및 설치
- PyInstaller를 사용하여 exe 파일 생성
- 빌드된 exe는 `dist/PDF변환기.exe`에 저장됩니다

### 수동 빌드

```bash
# PyInstaller 직접 사용
pyinstaller --onefile --windowed --name=PDF변환기 pdf_converter_gui.py
```

또는 spec 파일 사용:
```bash
pyinstaller build_exe.spec
```

## ❓ 문제 해결

### "Java를 찾을 수 없습니다" 오류

**해결 방법:**
1. Java가 설치되어 있는지 확인:
   ```bash
   java -version
   ```
2. Java가 설치되어 있다면 시스템 PATH에 추가되었는지 확인
3. 터미널/프로그램을 재시작

### "opendataloader-pdf 패키지를 찾을 수 없습니다" 오류

**해결 방법:**
```bash
# PyPI에서 설치
pip install opendataloader-pdf

# 또는 개발 모드로 설치
cd python/opendataloader-pdf
pip install -e .
```

### 변환 중 오류 발생

1. PDF 파일이 손상되지 않았는지 확인
2. PDF 파일이 암호화되어 있지 않은지 확인
3. 로그 영역의 오류 메시지를 확인

## 💡 주요 특징

- **기존 오픈소스 최대 활용**: `opendataloader_pdf.convert()` 함수를 직접 사용
- **사용자 친화적 UI**: tkinter 기반의 깔끔한 인터페이스
- **비동기 처리**: 변환 작업을 별도 스레드에서 실행하여 UI가 멈추지 않음
- **실시간 로그**: 변환 진행 상황을 실시간으로 확인 가능
- **에러 처리**: 친절한 한국어 오류 메시지 제공

## 📝 참고사항

- 변환된 파일은 기본적으로 원본 PDF와 같은 폴더에 저장됩니다
- 변환 중에는 버튼이 비활성화되어 중복 실행을 방지합니다
- Java가 설치되어 있지 않으면 변환이 실패합니다 (GUI 앱 자체는 실행됨)

## 🔗 관련 링크

- [OpenDataLoader-PDF 프로젝트](https://github.com/opendataloader-project/opendataloader-pdf)
- [사용 가이드](사용가이드.md)
- [README](README.md)



