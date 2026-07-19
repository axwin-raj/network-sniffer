from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton
from services.config_service import ConfigService
from utils.constants import AppConstants

class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        service = ConfigService()
        cfg = service.load() or {}

        form = QFormLayout(self)
        self.vt_key = QLineEdit(cfg.get("vt_api_key",""))
        form.addRow("VirusTotal API Key:", self.vt_key)

        self.ip_range = QLineEdit(cfg.get("default_ip_range",""))
        form.addRow("Default IP Range:", self.ip_range)

        self.port_range = QLineEdit(cfg.get("default_port_range",""))
        form.addRow("Default Port Range:", self.port_range)

        save = QPushButton("Save")
        save.clicked.connect(lambda: self._save(service))
        form.addRow(save)

    def _save(self, service):
        new_cfg = {
            "vt_api_key": self.vt_key.text(),
            "default_ip_range": self.ip_range.text(),
            "default_port_range": self.port_range.text()
        }
        service.save(new_cfg)
        self.accept()