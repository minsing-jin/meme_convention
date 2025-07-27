import tkinter as tk
from tkinter import ttk, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import shutil
import subprocess
import platform
from pathlib import Path


class MemeAdder:
    def __init__(self, contexts):
        self.contexts = contexts
        self.base_path = Path(__file__).parent.parent.parent / "resources" / "local_db"
        self.window = None

    def show_meme_adder_window(self):
        """Show the meme adder window with scrollable 2-column context boxes"""
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return

        # Create the main window using TkinterDnD for drag and drop support
        self.window = TkinterDnD.Tk()
        self.window.title("Meme Adder")
        self.window.geometry("800x450")

        # Configure grid weights for responsiveness
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)

        # Add title message
        title_label = tk.Label(
            self.window,
            text="Drag your meme (gif, jpeg, jpg, png....) in the context box",
            font=("Arial", 12),
            pady=10
        )
        title_label.grid(row=0, column=0, sticky="ew")

        # Create scrollable frame
        self.create_scrollable_context_grid()

        # Bind mouse wheel to canvas for scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Make window stay on top initially
        self.window.attributes('-topmost', True)
        self.window.after(100, lambda: self.window.attributes('-topmost', False))

    def create_scrollable_context_grid(self):
        """Create a scrollable grid of context boxes in 2 columns"""
        # Create main frame for scrollable area
        main_frame = tk.Frame(self.window)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Create canvas and scrollbar
        self.canvas = tk.Canvas(main_frame, bg="gray", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="gray")

        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Create window in canvas
        canvas_width = 2 * 350 + 3 * 15
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=canvas_width)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Grid canvas and scrollbar
        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Configure scrollable frame columns
        self.scrollable_frame.columnconfigure(0, weight=1)
        self.scrollable_frame.columnconfigure(1, weight=1)

        # Create context boxes in 2 columns
        self.create_context_boxes()

    def create_context_boxes(self):
        """Create context boxes arranged in 2 columns"""
        for i, context in enumerate(self.contexts):
            row = i // 2
            col = i % 2

            # Create context frame
            context_frame = tk.Frame(
                self.scrollable_frame,
                relief="solid",
                borderwidth=2,
                bg="lightgray",
                width=350,
                height=180  # 높이를 더 늘려서 버튼 공간 확보
            )
            context_frame.grid(
                row=row,
                column=col,
                padx=15,
                pady=15,
                sticky="ew"
            )
            context_frame.grid_propagate(False)

            # Context name label
            context_label = tk.Label(
                context_frame,
                text=context,
                font=("Arial", 12, "bold"),
                bg="lightgray",
                fg="black",
                wraplength=300
            )
            context_label.pack(pady=10)

            # Drop zone label
            drop_label = tk.Label(
                context_frame,
                text="Drop meme here",
                font=("Arial", 10),
                bg="lightgray",
                fg="black"
            )
            drop_label.pack()

            delete_button = tk.Button(
                context_frame,
                text="Click here to delete files",
                font=("Arial", 9),
                bg="lightgray",
                fg="black",
                relief="flat",  # 테두리 없음
                borderwidth=0,  # 테두리 두께 0
                highlightthickness=0,  # 포커스 사각선 숨김
                cursor="hand2",
                command=lambda ctx=context: self.open_context_folder(ctx)
            )
            delete_button.pack(pady=(10, 5))

            # Enable drag and drop for this context box (excluding the button)
            self.setup_drag_drop(context_frame, context)
            # Also setup drag and drop for labels
            self.setup_drag_drop(context_label, context)
            self.setup_drag_drop(drop_label, context)

    def setup_drag_drop(self, widget, context_name):
        """Setup drag and drop functionality for a context box"""
        widget.drop_target_register(DND_FILES)
        widget.dnd_bind('<<Drop>>', lambda event, ctx=context_name: self.handle_drop(event, ctx))

        # Visual feedback on drag enter/leave
        widget.dnd_bind('<<DragEnter>>', lambda event, w=widget: self.on_drag_enter(w))
        widget.dnd_bind('<<DragLeave>>', lambda event, w=widget: self.on_drag_leave(w))

    def handle_drop(self, event, context_name):
        """Handle file drop on context box"""
        file_paths = event.data.split()

        for file_path in file_paths:
            # Remove curly braces if present
            file_path = file_path.strip('{}')

            if self.is_valid_image_file(file_path):
                self._copy_to_context_folder(file_path, context_name)
            else:
                messagebox.showwarning(
                    "Invalid File",
                    f"File {os.path.basename(file_path)} is not a valid image format"
                )

    def is_valid_image_file(self, file_path):
        """Check if file is a valid image format"""
        valid_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
        file_ext = Path(file_path).suffix.lower()
        return file_ext in valid_extensions

    def _copy_to_context_folder(self, file_path, context_name):
        """이미지 파일을 기존 컨텍스트 폴더에 저장"""
        try:
            context_folder = self.base_path / context_name

            # 폴더가 존재하지 않으면 에러 메시지 표시
            if not context_folder.exists():
                messagebox.showerror(
                    "Folder Not Found",
                    f"Context folder '{context_name}' does not exist in {self.base_path}\n"
                    f"Please create the folder first: {context_folder}"
                )
                return

            file_name = os.path.basename(file_path)
            destination = context_folder / file_name

            # 파일 복사 (중복 확인 없이 바로 저장)
            shutil.copy2(file_path, destination)

            messagebox.showinfo(
                "Success",
                f"Added {file_name} to {context_name} context"
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to copy file: {str(e)}"
            )

    def open_context_folder(self, context_name):
        """컨텍스트 폴더를 파일 탐색기에서 열기"""
        try:
            context_folder = self.base_path / context_name

            # 폴더가 존재하지 않으면 에러 메시지 표시
            if not context_folder.exists():
                messagebox.showerror(
                    "Folder Not Found",
                    f"Context folder '{context_name}' does not exist in {self.base_path}\n"
                    f"Please create the folder first: {context_folder}"
                )
                return

            # 운영체제에 따라 폴더 열기
            system = platform.system()
            if system == "Windows":
                os.startfile(context_folder)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", context_folder])
            else:  # Linux
                subprocess.run(["xdg-open", context_folder])

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to open folder: {str(e)}"
            )

    def on_drag_enter(self, widget):
        """Visual feedback when drag enters widget"""
        # 버튼이 아닌 경우에만 색상 변경
        if not isinstance(widget, tk.Button):
            widget.configure(bg="lightblue")

    def on_drag_leave(self, widget):
        """Visual feedback when drag leaves widget"""
        # 버튼이 아닌 경우에만 색상 변경
        if not isinstance(widget, tk.Button):
            widget.configure(bg="lightgray")

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
