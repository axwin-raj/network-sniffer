from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem
from PySide6.QtGui import QPen, QColor
from PySide6.QtCore import Qt, QPointF

class TrafficMapWidget(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.nodes = {}

    def add_flow(self, src_ip: str, dst_ip: str, protocol: str):
        src_node = self._get_or_create_node(src_ip, x=50, y=200)
        dst_node = self._get_or_create_node(dst_ip, x=300, y=200)

        # Draw flow line
        line = QGraphicsLineItem(
        src_node.x() + 6, src_node.y() + 6,
        dst_node.x() + 6, dst_node.y() + 6
)
        line.setPen(QPen(self._protocol_color(protocol), 2))
        self.scene.addItem(line)

    def _get_or_create_node(self, ip, x, y):
        if ip in self.nodes:
            return self.nodes[ip]

        node = QGraphicsEllipseItem(x, y, 12, 12)
        node.setBrush(QColor("lightblue"))
        node.setToolTip(ip)
        self.scene.addItem(node)
        self.nodes[ip] = node
        return node

    def _protocol_color(self, proto):
        return {
            "TCP": Qt.red,
            "UDP": Qt.green,
            "ICMP": Qt.yellow,
        }.get(proto.upper(), Qt.white)