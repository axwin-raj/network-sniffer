from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QColor, QBrush

from core.analyzer import PacketAnalyzer
from core.detection import ThreatDetector, AdBlocker
from utils.constants import AppConstants
from utils.animations import AnimationUtils as Anim

class PacketTable(QWidget):
    packet_selected = Signal(object)
    def __init__(self, details_panel):
        super().__init__()
        self.details_panel = details_panel
        self.packets = []

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["#", "Time", "Source", "Dest", "Proto", "Info"]
        )
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table.itemSelectionChanged.connect(self._on_select)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)

    def add_packet(self, pkt):
        idx = self.table.rowCount()
        self.table.insertRow(idx)

        summary = PacketAnalyzer.summarize(pkt)
        threat, th_det = ThreatDetector.scan(pkt)
        ad, ad_det = AdBlocker.scan(pkt)

        info = summary["info"]
        if threat: info += f" [Threat: {th_det}]"
        if ad:     info += f" [Ad: {ad_det}]"

        values = [
            str(idx + 1), summary["timestamp"],
            summary.get("src", ""), summary.get("dst", ""),
            summary["protocol"], info
       ]
   
        for col, val in enumerate(values):
            item = QTableWidgetItem(val)
            self.table.setItem(idx, col, item)

        self.packets.append(pkt)
        self.table.scrollToBottom()

        if not self.details_panel.details_locked:
               self.table.selectRow(idx)

    def clear(self):
        self.table.setRowCount(0)
        self.packets.clear()

    def _on_select(self):
        if self.details_panel.details_locked:
             print("Selection blocked — panel locked")
             return

        row = self.table.currentRow()
        if 0 <= row < len(self.packets):
             print("Selection allowed — emitting packet")
             self.packet_selected.emit(self.packets[row])