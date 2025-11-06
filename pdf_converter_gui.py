#!/usr/bin/env python3
"""
PDF 변환기 GUI 애플리케이션

OpenDataLoader-PDF를 사용하여 PDF를 Markdown, HTML, JSON 형식으로 변환합니다.
"""

import sys
import os
import threading
import subprocess
from pathlib import Path
from tkinter import (
    Tk, Label, Button, filedialog, messagebox, 
    Frame, StringVar, scrolledtext
)
from tkinter import ttk

try:
    import opendataloader_pdf
except ImportError:
    messagebox.showerror(
        "모듈 오류",
        "opendataloader-pdf 패키지가 설치되어 있지 않습니다.\n\n"
        "설치 방법:\n"
        "  pip install opendataloader-pdf\n\n"
        "또는 개발 환경에서:\n"
        "  cd python/opendataloader-pdf\n"
        "  pip install -e ."
    )
    sys.exit(1)


class PDFConverterGUI:
    """PDF 변환기 GUI 클래스"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sangmin's PDF 변환기")
        self.root.geometry("600x550")
        self.root.resizable(False, False)
        
        # PDF 파일 경로
        self.pdf_path = StringVar()
        self.output_dir = None
        
        # UI 구성
        self.setup_ui()
        
        # 중앙 정렬
        self.center_window()
    
    def center_window(self):
        """창을 화면 중앙에 배치"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """UI 구성 요소 생성"""
        # 메인 프레임
        main_frame = Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # 제목
        title_label = Label(
            main_frame,
            text="Sangmin's PDF 변환기",
            font=("맑은 고딕", 18, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # 설명
        desc_label = Label(
            main_frame,
            text="PDF 파일을 선택하고 원하는 형식으로 변환하세요",
            font=("맑은 고딕", 10)
        )
        desc_label.pack(pady=(0, 5))
        
        # 안내 문구
        info_label = Label(
            main_frame,
            text="검정 화면이 나와도 놀라지 마세요. 변환 과정입니다.",
            font=("맑은 고딕", 9),
            fg="gray"
        )
        info_label.pack(pady=(0, 20))
        
        # PDF 파일 선택 영역
        file_frame = Frame(main_frame)
        file_frame.pack(fill='x', pady=(0, 20))
        
        Label(file_frame, text="PDF 파일:", font=("맑은 고딕", 10)).pack(side='left', padx=(0, 10))
        
        self.file_path_label = Label(
            file_frame,
            text="파일을 선택하세요",
            font=("맑은 고딕", 9),
            fg="gray",
            anchor='w'
        )
        self.file_path_label.pack(side='left', fill='x', expand=True)
        
        Button(
            file_frame,
            text="파일 선택",
            command=self.select_pdf_file,
            font=("맑은 고딕", 9),
            padx=10
        ).pack(side='right')
        
        # 구분선
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=20)
        
        # 변환 버튼 영역
        button_frame = Frame(main_frame)
        button_frame.pack(fill='x', pady=20)
        
        # Markdown 버튼
        self.markdown_btn = Button(
            button_frame,
            text="📝 Markdown으로 변환",
            command=lambda: self.convert_pdf("markdown"),
            font=("맑은 고딕", 11),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2",
            state="disabled"
        )
        self.markdown_btn.pack(fill='x', pady=5)
        
        # HTML 버튼
        self.html_btn = Button(
            button_frame,
            text="🌐 HTML로 변환",
            command=lambda: self.convert_pdf("html"),
            font=("맑은 고딕", 11),
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2",
            state="disabled"
        )
        self.html_btn.pack(fill='x', pady=5)
        
        # JSON 버튼
        self.json_btn = Button(
            button_frame,
            text="📄 JSON으로 변환",
            command=lambda: self.convert_pdf("json"),
            font=("맑은 고딕", 11),
            bg="#FF9800",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2",
            state="disabled"
        )
        self.json_btn.pack(fill='x', pady=5)
        
        # 구분선
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=20)
        
        # 진행 상황 영역
        progress_frame = Frame(main_frame)
        progress_frame.pack(fill='x', pady=(0, 10))
        
        # 진행 상태 레이블
        self.status_label = Label(
            progress_frame,
            text="대기 중...",
            font=("맑은 고딕", 9),
            fg="gray",
            anchor='w'
        )
        self.status_label.pack(anchor='w', pady=(0, 5))
        
        # 진행 바
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            length=560
        )
        self.progress_bar.pack(fill='x', pady=(0, 10))
        
        # 로그 영역
        log_frame = Frame(main_frame)
        log_frame.pack(fill='both', expand=True)
        
        Label(log_frame, text="상세 로그:", font=("맑은 고딕", 9)).pack(anchor='w')
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=6,
            font=("Consolas", 8),
            wrap='word',
            state='disabled'
        )
        self.log_text.pack(fill='both', expand=True, pady=(5, 0))
    
    def log(self, message):
        """로그 메시지 추가"""
        self.log_text.config(state='normal')
        self.log_text.insert('end', message + '\n')
        self.log_text.see('end')
        self.log_text.config(state='disabled')
        self.root.update_idletasks()
    
    def clear_log(self):
        """로그 초기화"""
        self.log_text.config(state='normal')
        self.log_text.delete('1.0', 'end')
        self.log_text.config(state='disabled')
    
    def update_status(self, message):
        """진행 상태 업데이트"""
        self.status_label.config(text=message, fg="black")
        self.root.update_idletasks()
    
    def start_progress(self):
        """진행 바 시작"""
        self.progress_bar.start(10)  # 10ms 간격으로 애니메이션
        self.update_status("변환 중...")
    
    def stop_progress(self):
        """진행 바 중지"""
        self.progress_bar.stop()
        self.progress_bar['value'] = 0
    
    def select_pdf_file(self):
        """PDF 파일 선택 다이얼로그"""
        file_path = filedialog.askopenfilename(
            title="PDF 파일 선택",
            filetypes=[("PDF 파일", "*.pdf"), ("모든 파일", "*.*")]
        )
        
        if file_path:
            self.pdf_path.set(file_path)
            self.file_path_label.config(text=Path(file_path).name, fg="black")
            
            # 버튼 활성화
            self.markdown_btn.config(state="normal")
            self.html_btn.config(state="normal")
            self.json_btn.config(state="normal")
            
            # 출력 폴더는 PDF와 같은 폴더로 설정
            self.output_dir = str(Path(file_path).parent)
            
            self.update_status(f"파일 선택됨: {Path(file_path).name}")
            self.log(f"✅ PDF 파일 선택: {Path(file_path).name}")
    
    def convert_pdf(self, format_type):
        """PDF 변환 실행"""
        pdf_file = self.pdf_path.get()
        
        if not pdf_file or not os.path.exists(pdf_file):
            messagebox.showerror("오류", "PDF 파일을 선택해주세요.")
            return
        
        # 버튼 비활성화
        self.markdown_btn.config(state="disabled")
        self.html_btn.config(state="disabled")
        self.json_btn.config(state="disabled")
        
        # 로그 초기화
        self.clear_log()
        
        # 진행 바 시작
        self.start_progress()
        
        # 변환 스레드 시작
        thread = threading.Thread(
            target=self._convert_thread,
            args=(pdf_file, format_type),
            daemon=True
        )
        thread.start()
    
    def _convert_thread(self, pdf_file, format_type):
        """변환 작업을 별도 스레드에서 실행"""
        try:
            format_name = {
                "markdown": "Markdown",
                "html": "HTML",
                "json": "JSON"
            }.get(format_type, format_type)
            
            self.update_status(f"{format_name} 형식으로 변환 중...")
            self.log(f"🔄 {format_name} 형식으로 변환 중...")
            self.log(f"📄 파일: {Path(pdf_file).name}")
            self.log(f"📁 출력 폴더: {self.output_dir}")
            self.log("")
            
            # opendataloader_pdf.convert 함수 사용
            # quiet=True로 설정: GUI 모드에서는 sys.stdout이 None일 수 있어서 오류 발생 방지
            opendataloader_pdf.convert(
                input_path=[pdf_file],
                output_dir=self.output_dir,
                format=[format_type],
                quiet=True  # GUI 모드에서는 quiet=True 사용
            )
            
            # 출력 파일 확인
            pdf_name = Path(pdf_file).stem
            extension = {
                "markdown": ".md",
                "html": ".html",
                "json": ".json"
            }.get(format_type, "")
            
            output_file = Path(self.output_dir) / f"{pdf_name}{extension}"
            
            if output_file.exists():
                self.stop_progress()
                self.update_status(f"✅ 변환 완료! - {Path(output_file).name}")
                self.log("")
                self.log(f"✅ 변환 완료!")
                self.log(f"📝 출력 파일: {output_file}")
                self.log("")
                self.log(f"💡 파일 위치를 열려면 탐색기에서 확인하세요.")
                
                messagebox.showinfo(
                    "변환 완료",
                    f"{format_name} 형식으로 변환되었습니다!\n\n"
                    f"출력 파일:\n{output_file}"
                )
            else:
                self.stop_progress()
                self.update_status("⚠️ 변환 완료 (파일 확인 필요)")
                self.log("")
                self.log(f"⚠️  변환은 완료되었지만 출력 파일을 찾을 수 없습니다.")
                messagebox.showwarning(
                    "알림",
                    "변환은 완료되었지만 출력 파일을 찾을 수 없습니다."
                )
        
        except FileNotFoundError as e:
            self.stop_progress()
            if "java" in str(e).lower():
                error_msg = (
                    "Java가 설치되어 있지 않거나 PATH에 없습니다.\n\n"
                    "Java 11 이상이 필요합니다.\n\n"
                    "설치 방법:\n"
                    "1. https://adoptium.net/ 에서 Java 다운로드\n"
                    "2. 설치 후 프로그램을 재시작하세요"
                )
                self.update_status("❌ Java를 찾을 수 없습니다")
            else:
                error_msg = f"파일을 찾을 수 없습니다:\n{str(e)}"
                self.update_status("❌ 파일을 찾을 수 없습니다")
            
            self.log("")
            self.log(f"❌ 오류: {error_msg}")
            messagebox.showerror("변환 오류", error_msg)
        
        except subprocess.CalledProcessError as e:
            self.stop_progress()
            self.update_status(f"❌ 변환 실패 (오류 코드: {e.returncode})")
            
            # 자세한 오류 정보 수집
            error_details = []
            error_details.append(f"Java 명령 실행 실패")
            error_details.append(f"반환 코드: {e.returncode}")
            
            if hasattr(e, 'output') and e.output:
                error_details.append(f"\n출력:\n{e.output}")
            if hasattr(e, 'stderr') and e.stderr:
                error_details.append(f"\n오류 메시지:\n{e.stderr}")
            
            error_msg = "\n".join(error_details)
            
            self.log("")
            self.log(f"❌ 오류: {error_msg}")
            import traceback
            self.log(traceback.format_exc())
            
            # 사용자에게 보여줄 간단한 메시지
            user_msg = (
                f"변환 중 오류가 발생했습니다.\n\n"
                f"오류 코드: {e.returncode}\n\n"
                f"가능한 원인:\n"
                f"1. PDF 파일이 손상되었거나 암호화되어 있습니다\n"
                f"2. Java 실행 중 문제가 발생했습니다\n"
                f"3. 메모리 부족 또는 다른 시스템 오류\n\n"
                f"자세한 내용은 로그를 확인하세요."
            )
            messagebox.showerror("변환 오류", user_msg)
        
        except Exception as e:
            self.stop_progress()
            self.update_status(f"❌ 오류 발생")
            error_msg = f"변환 중 오류가 발생했습니다:\n{str(e)}"
            self.log("")
            self.log(f"❌ 오류: {error_msg}")
            import traceback
            self.log(traceback.format_exc())
            messagebox.showerror("변환 오류", error_msg)
        
        finally:
            # 진행 바 중지 및 버튼 다시 활성화
            self.root.after(0, lambda: [
                self.stop_progress(),
                self.markdown_btn.config(state="normal"),
                self.html_btn.config(state="normal"),
                self.json_btn.config(state="normal")
            ])


def main():
    """메인 함수"""
    root = Tk()
    app = PDFConverterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()


