"""Tkinter GUI for Magic Square XX (boundary layer)."""

from __future__ import annotations

import logging
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from typing import Final

from boundary.facade import validate_and_solve
from boundary.gui.constants import (
    APP_TITLE,
    BLANK_CELL_VALUE,
    GRID_SIZE,
    WINDOW_MIN_HEIGHT,
    WINDOW_MIN_WIDTH,
)
from boundary.gui.grid_input_parser import (
    GridInputParseError,
    format_cell_for_display,
    read_grid_from_cells,
)
from boundary.gui.result_presenter import (
    NOT_IMPLEMENTED_MESSAGE,
    UNEXPECTED_ERROR_MESSAGE,
    format_facade_result,
)
from boundary.models.validation_failure_result import ValidationFailureResult

_LOGGER = logging.getLogger(__name__)

EXAMPLE_G1_GRID: Final[list[list[int]]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]


class MagicSquareApp:
    """4×4 magic square puzzle GUI — delegates solving to the boundary facade."""

    def __init__(self, root: tk.Tk) -> None:
        """Build widgets and bind actions."""
        self._root = root
        self._root.title(APP_TITLE)
        self._root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)

        self._cell_vars: list[list[tk.StringVar]] = []
        self._build_layout()
        self._load_example_grid(EXAMPLE_G1_GRID)

    def _build_layout(self) -> None:
        """Create header, grid, buttons, and result panel."""
        container = ttk.Frame(self._root, padding=16)
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(0, weight=1)

        title_font = tkfont.Font(size=14, weight="bold")
        ttk.Label(
            container,
            text="4×4 격자에 숫자를 입력하고 풀이를 실행하세요.",
            font=title_font,
        ).grid(row=0, column=0, pady=(0, 4), sticky="w")

        ttk.Label(
            container,
            text="빈칸은 비워 두거나 0을 입력하세요. (허용 범위: 0, 1~16)",
        ).grid(row=1, column=0, pady=(0, 12), sticky="w")

        grid_frame = ttk.LabelFrame(container, text="격자", padding=12)
        grid_frame.grid(row=2, column=0, pady=(0, 12))
        entry_font = tkfont.Font(size=16)

        for row in range(GRID_SIZE):
            row_vars: list[tk.StringVar] = []
            for col in range(GRID_SIZE):
                var = tk.StringVar()
                row_vars.append(var)
                entry = ttk.Entry(
                    grid_frame,
                    textvariable=var,
                    width=4,
                    justify="center",
                    font=entry_font,
                )
                entry.grid(row=row, column=col, padx=4, pady=4)
                entry.bind("<Return>", self._on_solve)
            self._cell_vars.append(row_vars)

        button_frame = ttk.Frame(container)
        button_frame.grid(row=3, column=0, pady=(0, 12), sticky="w")

        ttk.Button(button_frame, text="풀이", command=self._on_solve).grid(
            row=0, column=0, padx=(0, 8)
        )
        ttk.Button(button_frame, text="초기화", command=self._on_clear).grid(
            row=0, column=1, padx=(0, 8)
        )
        ttk.Button(
            button_frame,
            text="예제 (G1) 불러오기",
            command=lambda: self._load_example_grid(EXAMPLE_G1_GRID),
        ).grid(row=0, column=2)

        result_frame = ttk.LabelFrame(container, text="결과", padding=8)
        result_frame.grid(row=4, column=0, sticky="nsew")
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        container.rowconfigure(4, weight=1)

        self._result_text = tk.Text(
            result_frame,
            height=8,
            wrap="word",
            state="disabled",
            font=tkfont.Font(size=11),
        )
        self._result_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(
            result_frame,
            orient="vertical",
            command=self._result_text.yview,
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self._result_text.configure(yscrollcommand=scrollbar.set)

    def _read_cell_texts(self) -> list[list[str]]:
        """Return current entry values as row-major strings."""
        return [[var.get() for var in row] for row in self._cell_vars]

    def _load_example_grid(self, grid: list[list[int]]) -> None:
        """Populate entries from a sample grid."""
        for row_index, row in enumerate(grid):
            for col_index, value in enumerate(row):
                self._cell_vars[row_index][col_index].set(
                    format_cell_for_display(value)
                )
        self._set_result("예제 격자(G1)를 불러왔습니다. 풀이를 실행해 보세요.")

    def _on_clear(self) -> None:
        """Reset all cells and the result panel."""
        for row in self._cell_vars:
            for var in row:
                var.set("")
        self._set_result("격자를 초기화했습니다.")

    def _on_solve(self, _event: object | None = None) -> None:
        """Parse grid input and invoke the boundary facade."""
        try:
            grid = read_grid_from_cells(self._read_cell_texts())
        except GridInputParseError as exc:
            self._set_result(exc.message, is_error=True)
            return
        except ValueError as exc:
            _LOGGER.exception("Grid shape error while reading GUI cells")
            self._set_result(str(exc), is_error=True)
            return

        try:
            result = validate_and_solve(grid)
        except NotImplementedError:
            self._set_result(NOT_IMPLEMENTED_MESSAGE)
            return
        except Exception:
            _LOGGER.exception("Unexpected error during validate_and_solve")
            self._set_result(UNEXPECTED_ERROR_MESSAGE, is_error=True)
            return

        if isinstance(result, ValidationFailureResult) and result.is_failure:
            self._set_result(format_facade_result(result), is_error=True)
            return

        self._set_result(format_facade_result(result))

    def _set_result(self, message: str, *, is_error: bool = False) -> None:
        """Update the read-only result panel."""
        self._result_text.configure(state="normal")
        self._result_text.delete("1.0", tk.END)
        prefix = "오류: " if is_error else ""
        self._result_text.insert(tk.END, f"{prefix}{message}")
        self._result_text.configure(state="disabled")


def run_app() -> None:
    """Create the main window and start the Tk event loop."""
    logging.basicConfig(level=logging.INFO)
    root = tk.Tk()
    try:
        ttk.Style().theme_use("vista")
    except tk.TclError:
        pass
    MagicSquareApp(root)
    root.mainloop()
