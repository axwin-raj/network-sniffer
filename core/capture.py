import sys
import subprocess
import asyncio
import threading
import logging
import os
import pyshark

from PySide6.QtCore import QThread, Signal

DETACHED_PROCESS = 0x00000008
CREATE_NO_WINDOW = subprocess.CREATE_NO_WINDOW
CREATE_NEW_PROCESS_GROUP = subprocess.CREATE_NEW_PROCESS_GROUP

print("Loaded LiveCaptureEngine from core/capture.py")
logger = logging.getLogger("Capture")


def _hidden_windows_env() -> dict:
    env = os.environ.copy()
    if sys.platform.startswith("win"):
        env["PYTHONNOUSERSITE"] = "1"
        env["WIRESHARK_AUX_DIR"] = r"C:\Program Files\Wireshark"
        env["PYTHONEXECUTABLE"] = os.path.join(sys.base_prefix, "pythonw.exe")
    return env


def _resolve_interface(label: str) -> str:
    # If already a device path, keep as-is
    if label.startswith(r"\\Device\\NPF_"):
        return label
    # Try to map friendly names to actual devices
    try:
        from pyshark.tshark.tshark import get_tshark_interfaces
        devs = get_tshark_interfaces() or []
        low = label.strip().lower()
        if low in {"wi-fi", "wifi", "wlan"}:
            for d in devs:
                dl = d.lower()
                if "wi-fi" in dl or "wifi" in dl or "wlan" in dl or "wireless" in dl:
                    return d
        # Fallback to first device if nothing matched
        return devs[0] if devs else label
    except Exception:
        return label


class LiveCaptureEngine(QThread):
    """Threaded live packet capture via pyshark."""

    packet_captured = Signal(object)
    capture_started = Signal(str)
    capture_stopped = Signal()
    error_occurred = Signal(str)

    def __init__(self, interface: str, display_filter: str = "") -> None:
        super().__init__()
        self.interface = interface
        self.display_filter = "" if display_filter == "All" else display_filter
        self._stop_event = threading.Event()
        self._capture = None
        self._running = False

    def run(self) -> None:
        if self._running:
            return
        self._running = True
        try:
            # Ensure an event loop exists for any async ops beneath pyshark
            try:
                asyncio.get_running_loop()
            except RuntimeError:
                asyncio.set_event_loop(asyncio.new_event_loop())

            child_env = _hidden_windows_env()

            # Normalize interface label -> actual device name
            self.interface = _resolve_interface(self.interface)

            # Supported kwargs only
            kwargs = {
                "interface": self.interface,
                "override_prefs": {"gui.console_open": "NEVER"},
                "custom_parameters": ["-l"],  # line-buffered output
            }

            # Point to tshark.exe or a wrapper via env or default install path
            tshark_path = (
                os.getenv("TSHARK_PATH")
                or r"C:\Program Files\Wireshark\tshark.exe"
            )
            if os.path.exists(tshark_path):
                kwargs["tshark_path"] = tshark_path

            if self.display_filter:
                kwargs["display_filter"] = self.display_filter

            logger.debug("LiveCapture kwargs: %r", kwargs)
            self._capture = pyshark.LiveCapture(**kwargs)

            # Optional preference for speed; can be toggled off if issues arise
            try:
                self._capture.use_json = True
            except Exception:
                pass

            self.capture_started.emit(self.interface)

            for pkt in self._capture.sniff_continuously():
                if self._stop_event.is_set():
                    break
                try:
                    self.packet_captured.emit(pkt)
                except Exception as per_pkt_err:
                    logger.debug("Packet emit skipped: %s", per_pkt_err)

        except Exception as e:
            logger.exception("Capture error")
            self.error_occurred.emit(str(e))
        finally:
            try:
                if self._capture:
                    self._capture.close()
            except Exception:
                pass
            self._running = False
            self.capture_stopped.emit()

    def stop(self) -> None:
        self._stop_event.set()
        try:
            if self._capture:
                self._capture.close_timeout = 1
                self._capture.close()
        except Exception:
            pass
