# network_toolkit/gui/widgets/ProcessManagerPanel.py

import logging
import psutil
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QPushButton, QMessageBox
)

logger = logging.getLogger("ProcessManagerPanel")


class ProcessManagerPanel(QWidget):
    """
    UI panel that lists running processes and allows terminating the selected one.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logger
        self._setup_ui()
        self.refresh_process_list()

    def _setup_ui(self) -> None:
        """Construct widgets and layout."""
        self.setWindowTitle("Process Manager")

        layout = QVBoxLayout(self)

        # List of running processes
        self.process_list_widget = QListWidget()
        layout.addWidget(self.process_list_widget)

        # Refresh button
        self.refresh_btn = QPushButton("Refresh Processes")
        self.refresh_btn.clicked.connect(self.refresh_process_list)
        layout.addWidget(self.refresh_btn)

        # Kill process button
        self.kill_btn = QPushButton("Kill Selected Process")
        self.kill_btn.clicked.connect(self.kill_selected_process)
        layout.addWidget(self.kill_btn)

    def refresh_process_list(self) -> None:
        """Reload the QListWidget with current processes and CPU usage."""
        self.process_list_widget.clear()
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                pid = proc.info['pid']
                name = proc.info['name'] or "N/A"
                cpu = proc.info['cpu_percent']
                item_text = f"{pid} - {name} - CPU: {cpu}%"
                self.process_list_widget.addItem(item_text)
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                self.logger.debug("Skipping process listing: %s", e)

    def kill_selected_process(self) -> None:
        """Terminate the process selected in the list."""
        item = self.process_list_widget.currentItem()
        if item is None:
            QMessageBox.warning(self, "No Selection", "Please select a process to kill.")
            return

        pid_str = item.text().split(" - ", 1)[0]
        try:
            pid = int(pid_str)
            proc = psutil.Process(pid)
            proc.terminate()
            proc.wait(timeout=3)
            QMessageBox.information(self, "Terminated", f"Process {pid} has been terminated.")
            self.refresh_process_list()
        except Exception as e:
            self.logger.error("Failed to terminate process %s: %s", pid_str, e)
            QMessageBox.critical(
                self,
                "Error",
                f"Could not terminate process {pid_str}.\nError: {e}"
            )