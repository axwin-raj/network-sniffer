import os 
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget,
    QPushButton, QStatusBar, QMessageBox, QSizePolicy, QLabel
)

from utils.constants import AppConstants
from utils.file_handler import resource_path
from utils.packet_analyzer import PacketAnalyzer
from core.capture import LiveCaptureEngine

from gui.widgets.SettingsDialog import SettingsDialog
from gui.widgets.ControlPanel import ControlPanel
from gui.widgets.PacketTable import PacketTable
from gui.widgets.DetailsPanel import DetailsPanel
from gui.widgets.MonitorPanel import MonitorPanel
from gui.widgets.ProcessManagerPanel import ProcessManagerPanel
from gui.widgets.ScannerPanel import ScannerPanel
from gui.widgets.MalwarePanel import MalwarePanel
from gui.widgets.SecurityStatusPanel import SecurityStatusPanel
from gui.widgets.ExportDialog import ExportDialog
from gui.widgets.AboutDialog import AboutDialog
from gui.widgets.TrafficMapWidget import TrafficMapWidget

from utils.animations import AnimationUtils as Animations


class MainWindow(QMainWindow):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.cfg = config

        self.setWindowTitle(f"{AppConstants.APP_NAME} v{AppConstants.VERSION}")
        self.setWindowIcon(QIcon(resource_path(os.path.join(*AppConstants.APP_ICON))))
        self.resize(1200, 800)

        self._init_ui()
        self._init_menu()
        self._init_capture_handling()

    def keyPressEvent(self, event):
        key = event.key()
        if key in [Qt.Key_Escape, Qt.Key_Backspace]:
            if hasattr(self, "details_panel"):
                self.details_panel.unlock()
            if hasattr(self, "packet_table"):
                self.packet_table.clearSelection()
        else:
            if hasattr(self, "details_panel") and getattr(self.details_panel, "locked_packet", None):
                self.details_panel.lock()

    def switch_to_page(self, target_widget):
        if target_widget is not self.stack.currentWidget():
            target_widget.setWindowOpacity(0.0)
            self.stack.setCurrentWidget(target_widget)

            animation = QPropertyAnimation(target_widget, b"windowOpacity")
            animation.setDuration(400)
            animation.setStartValue(0.0)
            animation.setEndValue(1.0)
            animation.setEasingCurve(QEasingCurve.InOutQuad)
            animation.start(QPropertyAnimation.DeleteWhenStopped)

    def _init_ui(self):
        # Central widget & main layout
        container = QWidget()
        main_layout = QHBoxLayout(container)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(12, 12, 12, 12)
        self.setCentralWidget(container)

        # Side navigation panel
        nav_widget = QWidget()
        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setAlignment(Qt.AlignTop)
        nav_layout.setSpacing(10)
        nav_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.addWidget(nav_widget, 1)

        # --- Sniffer page ---
        sniff_page = QWidget()
        sniff_layout = QVBoxLayout(sniff_page)

        self.control_panel = ControlPanel(self.cfg)
        self.details_panel = DetailsPanel()
        self.packet_table = PacketTable(self.details_panel)

        self.packet_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.packet_table.packet_selected.connect(self.details_panel.display)

        sniff_layout.addWidget(self.control_panel)
        sniff_layout.addWidget(self.packet_table)
        sniff_layout.addWidget(self.details_panel)

        self.stack = QStackedWidget()
        self.stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.stack.addWidget(sniff_page)

        # --- Additional panels ---
        self.scanner_panel = ScannerPanel(self.cfg)
        self.monitor_panel = MonitorPanel()
        self.proc_panel = ProcessManagerPanel()
        self.malware_panel = MalwarePanel(self.cfg)
        self.status_panel = SecurityStatusPanel()

        self.stack.addWidget(self.scanner_panel)
        self.stack.addWidget(self.monitor_panel)
        self.stack.addWidget(self.proc_panel)
        self.stack.addWidget(self.malware_panel)
        self.stack.addWidget(self.status_panel)

        main_layout.addWidget(self.stack, 4)

        # Navigation buttons
        pages = [
            ("Sniffer", sniff_page),
            ("Processes", self.proc_panel),
            ("Malware", self.malware_panel),
            ("Status", self.status_panel),
        ]
        for name, widget in pages:
            self._setup_nav_button(name, widget, nav_layout)

        # --- Traffic Map Panel ---
        self.traffic_map = TrafficMapWidget()
        self.traffic_map.setFixedSize(180, 120)
        self.traffic_map.setStyleSheet(
            "border: 1px solid #444; background-color: #202020; border-radius: 6px;"
        )
        map_label = QLabel("Live Traffic Map")
        map_label.setAlignment(Qt.AlignCenter)
        map_label.setStyleSheet(
            "color: #ccc; font-size: 10pt; font-weight: 500; margin-top: -2px; "
            "margin-bottom: 4px; text-transform: uppercase; letter-spacing: 1px;"
        )
        map_container = QWidget()
        map_container_layout = QVBoxLayout(map_container)
        map_container_layout.setContentsMargins(0, 0, 0, 0)
        map_container_layout.setSpacing(4)
        map_container_layout.setAlignment(Qt.AlignHCenter)
        map_container_layout.addWidget(map_label)
        map_container_layout.addWidget(self.traffic_map)

        alignment_spacer = QWidget()
        alignment_spacer.setFixedHeight(270)
        nav_layout.addWidget(alignment_spacer)
        nav_layout.addWidget(map_container)
        nav_layout.addStretch()

        # --- Status bar ---
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def show_animated_page(self, page_widget, nav_button=None):
        if nav_button:
            Animations.bounce_button(nav_button)
        self.stack.setCurrentWidget(page_widget)
        Animations.slide_in(page_widget, offset=(-100, 0), duration=400)
        Animations.fade_in(page_widget, duration=300)

    def _init_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")

        settings_act = QAction("&Settings", self)
        settings_act.triggered.connect(lambda: SettingsDialog().exec_())
        file_menu.addAction(settings_act)

        export_act = QAction("&Export...", self)
        export_act.setShortcut(QKeySequence.Save)
        export_act.triggered.connect(lambda: ExportDialog(self).exec_())
        file_menu.addAction(export_act)
        file_menu.addSeparator()

        exit_act = QAction("E&xit", self)
        exit_act.setShortcut(QKeySequence.Quit)
        exit_act.triggered.connect(self.close)
        file_menu.addAction(exit_act)

        help_menu = menubar.addMenu("&Help")
        about_act = QAction("&About", self)
        about_act.triggered.connect(lambda: AboutDialog(self).exec_())
        help_menu.addAction(about_act)

        about_menu = self.menuBar().addMenu("&About")
        version_act = QAction("Version Info", self)
        version_act.triggered.connect(lambda: AboutDialog(self).exec_())
        about_menu.addAction(version_act)

        credits_act = QAction("Credits", self)
        credits_act.triggered.connect(lambda: QMessageBox.information(
            self,
            "Credits",
            "Network Sniffer Toolkit developed by Fasil.\nPowered by Python, PySide6, and persistence!"
        ))
        about_menu.addAction(credits_act)

    def _init_capture_handling(self):
        self.capture_engine = None
        cp = self.control_panel
        cp.start_capture.connect(self.start_capture)
        cp.stop_capture.connect(self.stop_capture)
        cp.clear_packets.connect(self.packet_table.clear)
        cp.export_data.connect(lambda: ExportDialog(self).exec_())

    def start_capture(self, interface: str, protocol: str):
        if self.capture_engine and self.capture_engine.isRunning():
            QMessageBox.warning(self, "Already Capturing", "Stop the current capture first.")
            return

        self.capture_engine = LiveCaptureEngine(interface, protocol)
        self.capture_engine.packet_captured.connect(self.packet_table.add_packet)
        self.capture_engine.packet_captured.connect(self._conditionally_clear_details)
        self.capture_engine.error_occurred.connect(
            lambda msg: QMessageBox.critical(self, "Error", msg)
        )
        self.capture_engine.capture_started.connect(
            lambda iface: self.status_bar.showMessage(f"Capturing on {iface}…")
        )
        self.capture_engine.capture_stopped.connect(
            lambda: self.status_bar.showMessage("Capture stopped")
        )
        self.capture_engine.packet_captured.connect(self._update_traffic_map)
        self.capture_engine.start()

    def _conditionally_clear_details(self):
        if not getattr(self.details_panel, "details_locked", False):
            self.details_panel.clear()

    def _update_traffic_map(self, pkt):
        # Expect PacketAnalyzer.summarize to return dict with src, dst, protocol
        summary = PacketAnalyzer.summarize(pkt)
        src = summary.get("src")
        dst = summary.get("dst")
        proto = summary.get("protocol", "TCP")
        if src and dst:
            self.traffic_map.add_flow(src, dst, proto)

    def stop_capture(self):
        if self.capture_engine:
            self.capture_engine.stop()

    def _setup_nav_button(self, name: str, page_widget: QWidget, layout: QVBoxLayout):
        btn = QPushButton(name)
        btn.clicked.connect(lambda _, b=btn: Animations.bounce_button(b))
        btn.clicked.connect(lambda _, w=page_widget: self.switch_to_page(w))
        layout.addWidget(btn)
