from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
from core.analyzer import PacketAnalyzer

class DetailsPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.title = QLabel("Packet Details")
        layout.addWidget(self.title)


        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.text.setPlainText("Select a packet to view details...")
        layout.addWidget(self.text)

        self.details_locked = False
        self.locked_packet = None

    def clear(self):
        self.title.setText("Packet Details")
        self.text.setPlainText("Select a packet to view details...")

    def display(self, pkt):
        if self.details_locked:
            return  # Ignore updates if locked

        detail = PacketAnalyzer.details(pkt)

        formatted = f"""
Source: {getattr(pkt, 'src', 'N/A')}
Destination: {getattr(pkt, 'dst', 'N/A')}
Protocol: {getattr(pkt, 'highest_layer', 'N/A')}

Details:
{detail}
"""

        self.title.setText(f"Details — {pkt.highest_layer}")
        self.text.setPlainText(formatted)
        self.locked_packet = pkt

    def lock(self):
        self.details_locked = True
        self.text.setToolTip("Details are locked. Press Esc or Backspace to unlock.")
    def unlock(self):
        self.details_locked = False
        self.locked_packet = None
        self.clear()
        self.text.setToolTip("")  # Clear the tooltip