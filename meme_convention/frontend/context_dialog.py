from __future__ import annotations
import tkinter as tk
from typing import Iterable, Optional

from utils.music_player import MusicPlayer
from utils.prefix import shortest_unique_prefixes
from utils.gui import center_window


class ContextCategoryDialog(tk.Toplevel):
    """
    Modal dialog that lets the user choose a category with optional background music.
    Usage:
        choice = ContextCategoryDialog.ask(categories, parent=root)
    Returns lowercase category or None if cancelled.
    """

    KEY_TIMEOUT_MS = 900

    # Class-level music player and settings
    _music_player = None
    _music_enabled = True

    # ----------------------------------------------------
    # Public API
    # ----------------------------------------------------
    @classmethod
    def ask(cls, categories: Iterable[str], parent: tk.Tk | None = None) -> Optional[str]:
        # Initialize music player if not already done
        if cls._music_player is None:
            cls._music_player = MusicPlayer()

        dlg = cls(list(categories), parent)
        dlg.wait_window()  # modal
        return dlg.result

    @classmethod
    def get_music_enabled(cls) -> bool:
        """Get the current music setting"""
        return cls._music_enabled

    @classmethod
    def set_music_enabled(cls, enabled: bool):
        """Set the music setting globally"""
        cls._music_enabled = enabled

    # ----------------------------------------------------
    # Internals
    # ----------------------------------------------------
    def __init__(self, categories: list[str], parent: tk.Tk | None):
        super().__init__(parent)
        self.title("Select Context Category")
        self.configure(bg="#1f2937")
        self.resizable(False, False)
        self.transient(parent)  # always on top of parent
        self.grab_set()  # modal

        self.categories = categories
        self.prefixes = shortest_unique_prefixes(categories)
        self.result: Optional[str] = None  # set on confirm
        self._buffer: str = ""
        self._buffer_job = None
        self._buttons: dict[str, tk.Button] = {}  # Store button references

        # Music control variables
        self.music_var = tk.BooleanVar(value=self._music_enabled)
        self.music_started = False

        self._build_ui()
        center_window(self)
        self._initial_focus()

        # Handle music based on checkbox state
        self._handle_music_change()

    # ------------------  UI build  ----------------------
    def _build_ui(self) -> None:
        header = tk.Label(self, text="Select Context Category",
                          font=("Arial", 18, "bold"),
                          fg="white", bg="#374151", pady=10, width=30)
        header.pack(fill="x")

        info = tk.Label(self, text="Type shortcut or click a button",
                        font=("Arial", 11), fg="white", bg="#1f2937")
        info.pack(pady=(10, 20))

        self.current = tk.StringVar(value=self.categories[0])
        current_lbl = tk.Label(self, textvariable=self.current,
                               font=("Arial", 12, "bold"),
                               fg="white", bg="#3182ce", padx=12, pady=3)
        current_lbl.pack()

        # Button grid -------------------------------------------------
        grid = tk.Frame(self, bg="#1f2937")
        grid.pack(padx=20, pady=20)
        cols = min(5, max(2, (len(self.categories) + 1) // 2))
        for i, cat in enumerate(self.categories):
            r, c = divmod(i, cols)
            btn = tk.Button(grid,
                            text=f"{cat.upper()}\n({self.prefixes[cat].upper()})",
                            width=12, height=2,
                            bg="#e2e8f0", fg="black",
                            font=("Arial", 10, "bold"),
                            relief="raised",
                            borderwidth=2,
                            command=lambda c=cat: self._select(c))
            btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
            grid.columnconfigure(c, weight=1)
            self._buttons[cat] = btn  # Store button reference

        # Set initial selection
        self._update_button_styles()

        # Music checkbox - moved here, above confirm/cancel buttons
        music_frame = tk.Frame(self, bg="#1f2937")
        music_frame.pack(pady=(10, 5))

        music_checkbox = tk.Checkbutton(
            music_frame,
            text="🎵 Play Background Music",
            variable=self.music_var,
            command=self._handle_music_change,
            font=("Arial", 11),
            fg="white",
            bg="#1f2937",
            selectcolor="#374151",
            activebackground="#1f2937",
            activeforeground="white"
        )
        music_checkbox.pack()

        # Confirm/cancel ---------------------------------------------
        bar = tk.Frame(self, bg="#1f2937")
        bar.pack(pady=(0, 15))

        tk.Button(bar, text="✓ Confirm (Enter)",
                  command=self._confirm,
                  bg="#22c55e", width=14).pack(side="left", padx=8)
        tk.Button(bar, text="✗ Exit (Esc)",
                  command=self._cancel,
                  bg="#ef4444", width=10).pack(side="left", padx=8)

        # Key bindings
        self.bind("<Key>", self._handle_key)
        self.bind("<Return>", lambda e: self._confirm())
        self.bind("<Escape>", lambda e: self._cancel())
        self.bind("<Control-c>", lambda e: self._confirm())
        self.bind("<Control-e>", lambda e: self._cancel())

    def _initial_focus(self) -> None:
        self.focus_set()

    # ------------------  Music handling  ----------------
    def _handle_music_change(self):
        """Handle music checkbox state changes"""
        # Update the class-level setting
        self.__class__._music_enabled = self.music_var.get()

        if self.music_var.get():
            # Start music if checkbox is checked and not already playing
            if not self._music_player.is_playing:
                success = self._music_player.play_random_music()
                if success:
                    self.music_started = True
                    print("🎵 Music started in context dialog")
            else:
                # 이미 재생 중이면 계속 재생
                self._music_player.ensure_music_playing()
                self.music_started = True
                print("🎵 Music continues from previous session")
        else:
            # Stop music if checkbox is unchecked
            if self.music_started:
                self._music_player.stop_music()
                self.music_started = False

    # ------------------  selection logic ----------------
    def _select(self, cat: str) -> None:
        self.current.set(cat)
        self._update_button_styles()

    def _update_button_styles(self) -> None:
        """Update button styles to highlight the selected category."""
        current_cat = self.current.get()

        for cat, btn in self._buttons.items():
            if cat == current_cat:
                # Selected button: thicker border, different colors
                btn.configure(
                    bg="#66efaf",  # Green background
                    fg="Green",  # Green text
                    relief="solid",  # Solid border style
                    borderwidth=2,  # Thicker border
                    highlightbackground="#66efaf",  # Green highlight
                    highlightthickness=2
                )
            else:
                # Non-selected buttons: default style
                btn.configure(
                    bg="#e2e8f0",  # Light gray background
                    fg="black",  # Black text
                    relief="raised",  # Raised border style
                    borderwidth=2,  # Normal border
                    highlightbackground="#d1d5db",  # Gray highlight
                    highlightthickness=0
                )

    def _confirm(self) -> None:
        self.result = self.current.get().lower()
        self._stop_music_and_close()

    def _cancel(self) -> None:
        self.result = None
        if self.music_started and self._music_player.is_playing:
            self._music_player.stop_music()
        self.destroy()

    def _stop_music_and_close(self):
        """Close dialog but keep music playing for autocomplete process"""
        self.destroy()

    # ------------------  buffered shortcut ---------------
    def _handle_key(self, event) -> None:
        if event.state & 0x4:  # Ctrl
            return  # handled by bindings above
        ch = event.char.lower()
        if not ch.isalnum():
            self._reset_buf()
            return
        self._buffer += ch
        if self._buffer_job:
            self.after_cancel(self._buffer_job)
        self._buffer_job = self.after(self.KEY_TIMEOUT_MS, self._reset_buf)

        matches = [c for c in self.categories if c.lower().startswith(self._buffer)]
        if len(matches) == 1:
            self._select(matches[0])
            self._reset_buf()

    def _reset_buf(self) -> None:
        self._buffer = ""
        self._buffer_job = None
