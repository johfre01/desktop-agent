"""
Desktop Agent - Main Window

This module contains the MainWindow class that serves as the primary
application window - a transparent overlay with a visible frame border.
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen, QColor


class MainWindow(QWidget):
    """
    Main application window for Desktop Agent.

    This is a transparent overlay window with:
    - No default window frame (frameless)
    - Transparent background (see-through)
    - Custom-drawn border (cyan frame)
    - Stays on top of other windows

    Note: Without a title bar, you cannot drag or close this window normally.
    Use Alt+F4 or Ctrl+C in terminal to close. Dragging will be added in Phase 4.
    """

    # Frame border settings
    BORDER_COLOR = QColor(0, 217, 255)  # Cyan
    BORDER_WIDTH = 2

    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Set up the user interface."""
        # Window title (still useful for taskbar/alt-tab)
        self.setWindowTitle("Desktop Agent")

        # Remove default window frame and keep on top
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )

        # Make the background transparent
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Window size and position
        self.setGeometry(100, 100, 800, 600)

        # Minimum size to prevent window from becoming too small
        self.setMinimumSize(400, 300)

    def paintEvent(self, event):
        """
        Custom paint event to draw the frame border.

        This is called automatically by Qt whenever the window needs
        to be redrawn (on show, resize, etc.)
        """
        painter = QPainter(self)

        # Enable anti-aliasing for smoother edges
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Set up the pen for drawing the border
        pen = QPen(self.BORDER_COLOR)
        pen.setWidth(self.BORDER_WIDTH)
        painter.setPen(pen)

        # Don't fill the rectangle (keep it transparent inside)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        # Draw the frame border
        # adjusted() shrinks the rect so the border draws fully inside
        rect = self.rect().adjusted(
            self.BORDER_WIDTH // 2,
            self.BORDER_WIDTH // 2,
            -self.BORDER_WIDTH // 2 - 1,
            -self.BORDER_WIDTH // 2 - 1
        )

        # Draw rectangle with sharp corners
        painter.drawRect(rect)

        painter.end()
