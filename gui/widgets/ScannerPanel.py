from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QTextEdit
from PySide6.QtCore import Qt
from core.scanners.port_scanner import ArpHostScanner
from services.nmap_service import NmapService
from core.scanners.vuln_scanner import VulnScanner
from nmap import PortScanner


class NmapService:
    def __init__(self):
        self.scanner = PortScanner()

    def scan_vuln(self, target: str, scan_type: str):
        # Basic example using default vuln scripts
        args = "-Pn --script vuln" if scan_type == "Vuln" else "-Pn"

        result = self.scanner.scan(
            hosts=target,
            arguments=args
        )
        return result


class ScannerPanel(QWidget):
    def __init__(self, cfg):
        self.scanner = ArpHostScanner()
        super().__init__()
        self.cfg = cfg
        layout = QVBoxLayout(self)

        # ARP host discovery
        btn_hosts = QPushButton("Discover Hosts")
        btn_hosts.clicked.connect(self._discover)
        layout.addWidget(btn_hosts)

        # Port/Vuln mode
        self.mode = QComboBox()
        self.mode.addItems(["quick","advanced","full"])
        layout.addWidget(self.mode)

        btn_scan = QPushButton("Scan Vulnerabilities")
        btn_scan.clicked.connect(self._vuln_scan)
        layout.addWidget(btn_scan)

        self.out = QTextEdit()
        layout.addWidget(self.out)

        self.ps = ArpHostScanner()
        self.nm = NmapService()

    def _discover(self):
        self.out.clear()
        for host in self.ps.discover_hosts(self.cfg["default_ip_range"]):
            self.out.append(f"{host['ip']} - {host['mac']}")

    def _vuln_scan(self):
        target = self.cfg["default_ip_range"].split('/')[0]
        res = self.nm.scan_ports(target, self.mode.currentText())
        self.out.clear()
        if "error" in res:
            self.out.append("Error: " + res["error"])
        else:
            for host, data in res.items():
                self.out.append(f"Host: {host}")
                for proto in data.all_protocols():
                    for port in data[proto]:
                        self.out.append(f" {proto}/{port}: {data[proto][port]['state']}")