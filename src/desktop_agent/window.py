"""
Desktop Agent - Main Window

This module contains the MainWindow class that serves as the primary
application window. In later phases, this will become our transparent
overlay frame.
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt


class MainWindow(QWidget):
    """
    Main application window for Desktop Agent.

    This window will eventually become a transparent overlay with:
    - A draggable, resizable frame
    - A control panel at the bottom
    - Screenshot capture functionality

    For now, it's a basic window to establish the foundation.
    """

    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Set up the user interface."""
        # Window title
        self.setWindowTitle("Desktop Agent")

        # Window size and position
        # setGeometry(x, y, width, height)
        self.setGeometry(100, 100, 800, 600)

        # Minimum size to prevent window from becoming too small
        self.setMinimumSize(400, 300)

        # Set a background color so we can see the window
        # This will be removed when we make it transparent in Phase 3
        self.setStyleSheet("background-color: #1a1a2e;")
