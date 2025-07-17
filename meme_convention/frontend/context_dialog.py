# meme_convention/frontend/context_dialog.py
from __future__ import annotations
import tkinter as tk
from typing import Iterable, Optional

from utils.prefix import shortest_unique_prefixes
from utils.gui import center_window


class ContextCategoryDialog(tk.Tk):
    """
    Modal dialog that lets the user choose a category.
    Usage:
        choice = ContextCategoryDialog.ask(categories, parent=root)
    Returns lowercase category or None if cancelled.
    """

    KEY_TIMEOUT_MS = 900

    # ----------------------------------------------------
    # Public API
    # ----------------------------------------------------
    @classmethod
    def ask(cls, categories: Iterable[str], parent: tk.Tk | None = None) -> Optional[str]:
        dlg = cls(list(categories), parent)
        dlg.wait_window()  # modal
        return dlg.result

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

        self._build_ui()
        center_window(self)
        self._initial_focus()

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
                            command=lambda c=cat: self._select(c))
            btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
            grid.columnconfigure(c, weight=1)
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

    # ------------------  selection logic ----------------
    def _select(self, cat: str) -> None:
        self.current.set(cat)

    def _confirm(self) -> None:
        self.result = self.current.get().lower()
        self.destroy()

    def _cancel(self) -> None:
        self.result = None
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
