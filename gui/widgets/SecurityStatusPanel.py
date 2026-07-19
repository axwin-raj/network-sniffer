from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit
import subprocess, psutil

class SecurityStatusPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        btn = QPushButton("Check Status")
        btn.clicked.connect(self._check)
        layout.addWidget(btn)

        self.out = QTextEdit()
        layout.addWidget(self.out)

    def _check(self):
        self.out.clear()
        try:
            fw = subprocess.check_output("netsh advfirewall show allprofiles", shell=True).decode()
            status = "ON" if "State ON" in fw else "OFF"
        except:
            status = "Unknown"
        self.out.append(f"Firewall: {status}")

        try:
            av = subprocess.check_output("sc query WinDefend", shell=True).decode()
            av_status = "Running" if "RUNNING" in av else "Stopped"
        except:
            av_status = "Unknown"
        self.out.append(f"Antivirus: {av_status}")

        ports = {c.laddr.port for c in psutil.net_connections() if c.status=="LISTEN"}
        self.out.append(f"Open Ports: {sorted(ports)}")