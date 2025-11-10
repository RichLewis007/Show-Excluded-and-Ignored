# Scan progress dialog.
from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ScanProgressDialog(QDialog):
    # Modal dialog showing background scan progress and controls.

    scanRequested = Signal()
    pauseRequested = Signal()
    cancelRequested = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Scanning…")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)
        self.resize(720, 260)

        self._summary_label = QLabel("Ready to scan.", self)
        self._summary_label.setWordWrap(True)

        self._path_label = QLabel("", self)
        self._path_label.setWordWrap(True)
        self._path_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self._path_label.setMinimumWidth(680)
        self._path_label.setMinimumHeight(48)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        self._scan_button = QPushButton("Scan", self)
        self._scan_button.clicked.connect(self.scanRequested.emit)
        button_layout.addWidget(self._scan_button)

        self._pause_button = QPushButton("Pause", self)
        self._pause_button.clicked.connect(self.pauseRequested.emit)
        button_layout.addWidget(self._pause_button)

        self._cancel_button = QPushButton("Cancel", self)
        self._cancel_button.clicked.connect(self.cancelRequested.emit)
        button_layout.addWidget(self._cancel_button)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        layout.addWidget(self._summary_label)
        layout.addWidget(self._path_label)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.set_running(False)

    # ------------------------------------------------------------------
    # State helpers

    def prepare_for_scan(self, root_path: Path) -> None:
        # Prime the dialog before a new scan begins.
        self._summary_label.setText(f"Scanning {root_path}…")
        self._path_label.clear()
        self.set_running(True)

    def set_running(self, running: bool) -> None:
        # Toggle button availability based on scan activity.
        self._scan_button.setEnabled(not running)
        self._pause_button.setEnabled(running)
        self._cancel_button.setEnabled(running)

    def update_progress(self, scanned: int, matched: int, current_path: str) -> None:
        # Update the progress details shown in the dialog.
        self._summary_label.setText(f"Scanning… {matched} matches / {scanned} items")
        if current_path:
            self._path_label.setText(current_path)
        else:
            self._path_label.clear()

    def show_finished(self) -> None:
        # Display completion message and reset controls.
        self._summary_label.setText("Finished scanning.")
        self._path_label.clear()
        self.set_running(False)

    def show_error(self, message: str) -> None:
        # Display error feedback and reset controls.
        self._summary_label.setText(message)
        self._path_label.clear()
        self.set_running(False)

    def show_status(self, message: str) -> None:
        # Display an informational status update and reset controls.
        self._summary_label.setText(message)
        self._path_label.clear()
        self.set_running(False)
