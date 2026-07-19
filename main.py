#!/usr/bin/env python3
"""
network_toolkit/main.py

Entry point for the Network Security Toolkit.
Initializes logging, loads config, applies theme, kicks off a smooth fade-in
and background animation, then launches the main window.
"""

import os
import sys
import asyncio
import logging
from utils.logging import setup_logger
from utils.constants import AppConstants
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("[Boot] .env loaded:", bool(os.getenv("VT_API_KEY")))
except Exception:
    pass



def resource_path(*parts):
    base_dir = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, *parts)


from PySide6.QtGui     import QIcon, QColor
from PySide6.QtWidgets import QApplication
from utils.config_loader import ConfigLoader
from gui.windows.MainWindow import MainWindow

# Animation utilities (pure-Python, not QSS)
from utils.animations    import AnimationUtils as Animations


def load_theme(app: QApplication, theme_path: str) -> None:

    """
    Load and apply a QSS stylesheet from file.
    Qt will silently ignore malformed QSS, so we log a preview.
    """
    logger = logging.getLogger("main")

    if not os.path.isfile(theme_path):
        logger.warning("Theme file not found: %s", theme_path)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        theme_path = os.path.join(BASE_DIR, "assets", "dark_theme.qss")
        if not os.path.isfile(theme_path):
            logger.warning("Fallback theme file not found: %s", theme_path)
            return
    if not os.access(theme_path, os.R_OK):
        logger.warning("Cannot read theme file: %s", theme_path)
        return

    with open(theme_path, "r", encoding="utf-8") as f:
        data = f.read()

    if not data.strip():
        logger.warning("Theme file is empty: %s", theme_path)
        return

    # Dump first few lines so you can catch typos or stray characters
    preview = "\n".join(data.splitlines()[:10])
    logger.info("Loading theme, preview:\n%s", preview)

    # Apply stylesheet
    app.setStyleSheet(data)
    logger.info("Stylesheet applied successfully")


def main() -> None:
    # On Windows, use ProactorEventLoop for better subprocess support
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    # Initialize logging
    setup_logger(AppConstants.LOG_FILE)
    logging.getLogger("main").info("Starting Network Security Toolkit")

    # Load application settings
    config = ConfigLoader.load()

    # Enable High-DPI scaling
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    os.environ["QT_ENABLE_HIGHDPI_PIXMAPS"] = "1"

    # Create the application
    app = QApplication(sys.argv)
    app.setApplicationName(AppConstants.APP_NAME)
    app.setApplicationVersion(AppConstants.VERSION)
    app.setOrganizationName(AppConstants.ORGANIZATION_NAME)
    app.setOrganizationDomain(AppConstants.ORGANIZATION_DOMAIN)

    # Theme and icon
    theme_path = resource_path(*AppConstants.THEME_FILE)

    app.setWindowIcon(QIcon(resource_path(*AppConstants.APP_ICON)))

    # Instantiate main window
    window = MainWindow(config)

    # Optional: force black background before theme overrides it
    window.setStyleSheet("background-color: #000000;")

    # Show window and animations
    window.show()
    Animations.fade_window(window, duration=800)
    Animations.animate_bg_color(
        window,
        start=QColor("#000000"),
        end=QColor("#1E1E1E"),
        duration=600
    )

    # Enter the Qt event loop
    sys.exit(app.exec())



if __name__ == "__main__":
    main()