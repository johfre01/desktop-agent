"""
Desktop Agent - Main Window

This module contains the MainWindow class that serves as the primary
application window - a transparent overlay with a visible frame border,
control panel, and drag/resize functionality.
"""

from PyQt6.QtWidgets import (
    QWidget, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QApplication
)
from PyQt6.QtCore import Qt, QPoint, QTimer
from datetime import datetime
from pathlib import Path
from PyQt6.QtGui import QPainter, QPen, QColor


class ControlPanel(QWidget):
    """
    Control panel widget containing the Capture button and chat input.

    This panel sits at the bottom of the main window and provides
    the user interface for capturing screenshots and (later) chatting
    with the LLM.
    """

    # Panel settings
    PANEL_HEIGHT = 50
    PANEL_COLOR = "#1a1a2e"

    def __init__(self, parent=None):
        """Initialize the control panel."""
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """Set up the control panel UI."""
        # Set fixed height
        self.setFixedHeight(self.PANEL_HEIGHT)

        # Make panel opaque with dark background
        self.setAutoFillBackground(True)
        self.setStyleSheet(f"background-color: {self.PANEL_COLOR};")

        # Create horizontal layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(10)

        # Create Capture button
        self.capture_button = QPushButton("Capture")
        self.capture_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.capture_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d9ff, stop:1 #00ff88);
                color: black;
                border: none;
                padding: 8px 24px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00ff88, stop:1 #00d9ff);
            }
            QPushButton:pressed {
                background: #00b8d4;
            }
        """)

        # Create chat input
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Ask about this screenshot...")
        self.chat_input.setStyleSheet("""
            QLineEdit {
                background-color: #0a0a15;
                color: #e4e4e4;
                border: 1px solid #333;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #00d9ff;
            }
            QLineEdit::placeholder {
                color: #666;
            }
        """)

        # Add widgets to layout
        layout.addWidget(self.capture_button)
        layout.addWidget(self.chat_input, 1)  # stretch factor 1 to take remaining space


class MainWindow(QWidget):
    """
    Main application window for Desktop Agent.

    This is a transparent overlay window with:
    - No default window frame (frameless)
    - Transparent background (see-through)
    - Custom-drawn border (cyan frame)
    - Stays on top of other windows
    - Draggable from center area
    - Resizable from edges and corners
    - Control panel at the bottom
    """

    # Frame border settings
    BORDER_COLOR = QColor(0, 217, 255)  # Cyan
    BORDER_WIDTH = 2

    # Edge detection margin (pixels from edge to trigger resize)
    EDGE_MARGIN = 16

    def __init__(self):
        """Initialize the main window."""
        super().__init__()

        # Drag/resize state
        self._drag_start_pos = None
        self._drag_start_geometry = None
        self._resize_edge = None

        # Screenshot capture state
        self._capture_region = None
        self._is_capturing = False

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

        # Enable mouse tracking for cursor updates while hovering
        self.setMouseTracking(True)

        # Window size and position
        self.setGeometry(100, 100, 800, 600)

        # Minimum size to prevent window from becoming too small
        self.setMinimumSize(300, 200)

        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Add spacer to push panel to bottom
        main_layout.addStretch(1)

        # Create and add control panel
        self.control_panel = ControlPanel(self)
        main_layout.addWidget(self.control_panel)

        # Connect signals
        self.control_panel.capture_button.clicked.connect(self.on_capture_clicked)
        self.control_panel.chat_input.returnPressed.connect(self.on_chat_submit)

    def on_capture_clicked(self):
        """Handle Capture button click - start screenshot capture."""
        # Calculate the capture region (inside the frame border, excluding panel)
        geo = self.geometry()
        panel_height = self.get_panel_height()

        # Border drawn with pen width BORDER_WIDTH, centered on line position
        # This covers BORDER_WIDTH + 1 pixels from each edge (pen extends half-width each side)
        # Right/bottom need extra margin due to asymmetric border_rect adjustment + anti-aliasing
        left_margin = self.BORDER_WIDTH + 1
        top_margin = self.BORDER_WIDTH + 1
        right_margin = self.BORDER_WIDTH + 3   # Extra for asymmetry + AA
        bottom_margin = self.BORDER_WIDTH + 2  # Extra for AA at small sizes

        # Store the region to capture (in screen coordinates)
        self._capture_region = (
            geo.x() + left_margin,
            geo.y() + top_margin,
            geo.width() - left_margin - right_margin,
            geo.height() - panel_height - top_margin - bottom_margin
        )

        # Make interior fully transparent (skip the nearly-invisible fill)
        self._is_capturing = True
        self.repaint()
        QApplication.processEvents()

        # Short delay for compositor to update, then capture
        QTimer.singleShot(50, self._do_capture)

    def _do_capture(self):
        """Perform the actual screen capture."""
        if self._capture_region is None:
            self._is_capturing = False
            self.repaint()
            return

        x, y, width, height = self._capture_region

        # Capture the screen region
        screen = QApplication.primaryScreen()
        pixmap = screen.grabWindow(0, x, y, width, height)

        # Restore the nearly-invisible fill for mouse event handling
        self._is_capturing = False
        self.repaint()

        # Create save directory
        save_dir = Path("C:/Projects/Desktop Agent/screenshots")
        save_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = save_dir / f"Context_{timestamp}.png"

        # Save the screenshot
        pixmap.save(str(filepath))
        print(f"Screenshot saved: {filepath}")

        # Clear capture region
        self._capture_region = None

    def on_chat_submit(self):
        """Handle chat input submission."""
        text = self.control_panel.chat_input.text()
        if text.strip():
            print(f"Chat submitted: {text}")
            # LLM integration will be implemented in Phase 8
            self.control_panel.chat_input.clear()

    def get_panel_height(self):
        """Get the height of the control panel."""
        return self.control_panel.height() if hasattr(self, 'control_panel') else 0

    def get_edge_at_position(self, pos):
        """
        Determine which edge/corner the given position is in.

        Args:
            pos: QPoint position relative to the widget

        Returns:
            String indicating the edge ('top', 'bottom', 'left', 'right'),
            corner ('top-left', 'top-right', 'bottom-left', 'bottom-right'),
            or None if in the center (drag area).
        """
        x, y = pos.x(), pos.y()
        width, height = self.width(), self.height()
        margin = self.EDGE_MARGIN
        panel_height = self.get_panel_height()

        # If clicking in the panel area, don't handle as edge/drag
        if y > height - panel_height:
            return 'panel'  # Special value to indicate panel area

        # Determine which edges we're near
        near_left = x < margin
        near_right = x > width - margin
        near_top = y < margin
        near_bottom = y > height - panel_height - margin

        # Check corners first (they take priority)
        if near_top and near_left:
            return 'top-left'
        if near_top and near_right:
            return 'top-right'
        if near_bottom and near_left:
            return 'bottom-left'
        if near_bottom and near_right:
            return 'bottom-right'

        # Check edges
        if near_top:
            return 'top'
        if near_bottom:
            return 'bottom'
        if near_left:
            return 'left'
        if near_right:
            return 'right'

        # Center area (for dragging)
        return None

    def get_cursor_for_edge(self, edge):
        """
        Get the appropriate cursor for a given edge/corner.

        Args:
            edge: String from get_edge_at_position() or None

        Returns:
            Qt.CursorShape for the edge
        """
        if edge == 'panel':
            return Qt.CursorShape.ArrowCursor
        elif edge is None:
            return Qt.CursorShape.SizeAllCursor  # Move cursor for drag
        elif edge in ('left', 'right'):
            return Qt.CursorShape.SizeHorCursor
        elif edge in ('top', 'bottom'):
            return Qt.CursorShape.SizeVerCursor
        elif edge in ('top-left', 'bottom-right'):
            return Qt.CursorShape.SizeFDiagCursor
        elif edge in ('top-right', 'bottom-left'):
            return Qt.CursorShape.SizeBDiagCursor
        else:
            return Qt.CursorShape.ArrowCursor

    def mousePressEvent(self, event):
        """Handle mouse button press to start drag or resize."""
        if event.button() == Qt.MouseButton.LeftButton:
            edge = self.get_edge_at_position(event.position().toPoint())

            # Don't handle drag/resize if clicking in panel
            if edge == 'panel':
                return

            # Store starting position and geometry
            self._drag_start_pos = event.globalPosition().toPoint()
            self._drag_start_geometry = self.geometry()

            # Determine if we're resizing (edge) or dragging (center)
            self._resize_edge = edge

    def mouseMoveEvent(self, event):
        """Handle mouse movement for cursor updates and drag/resize."""
        if event.buttons() & Qt.MouseButton.LeftButton:
            # We're dragging or resizing
            if self._drag_start_pos is not None:
                self._handle_drag_or_resize(event)
        else:
            # Just hovering - update cursor based on position
            edge = self.get_edge_at_position(event.position().toPoint())
            self.setCursor(self.get_cursor_for_edge(edge))

    def mouseReleaseEvent(self, event):
        """Handle mouse button release to end drag or resize."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start_pos = None
            self._drag_start_geometry = None
            self._resize_edge = None

    def _handle_drag_or_resize(self, event):
        """
        Execute the drag or resize operation based on current state.

        Args:
            event: The mouse move event
        """
        if self._drag_start_pos is None or self._drag_start_geometry is None:
            return

        # Calculate how far the mouse has moved from the start
        current_pos = event.globalPosition().toPoint()
        delta = current_pos - self._drag_start_pos

        if self._resize_edge is None:
            # Dragging - move the window
            new_pos = self._drag_start_geometry.topLeft() + delta

            # Constrain to screen boundaries
            screen = QApplication.primaryScreen().availableGeometry()
            new_x = max(screen.left(), min(new_pos.x(), screen.right() - self.width()))
            new_y = max(screen.top(), min(new_pos.y(), screen.bottom() - self.height()))

            self.move(new_x, new_y)
        else:
            # Resizing - adjust geometry based on which edge
            self._do_resize(delta)

    def _do_resize(self, delta):
        """
        Resize the window based on the drag delta and active edge.

        Args:
            delta: QPoint representing mouse movement from start
        """
        geo = self._drag_start_geometry
        new_x = geo.x()
        new_y = geo.y()
        new_width = geo.width()
        new_height = geo.height()

        edge = self._resize_edge

        # Adjust dimensions based on which edge is being dragged
        if 'left' in edge:
            new_x = geo.x() + delta.x()
            new_width = geo.width() - delta.x()
        if 'right' in edge:
            new_width = geo.width() + delta.x()
        if 'top' in edge:
            new_y = geo.y() + delta.y()
            new_height = geo.height() - delta.y()
        if 'bottom' in edge:
            new_height = geo.height() + delta.y()

        # Enforce minimum size
        min_w = self.minimumWidth()
        min_h = self.minimumHeight()

        # If resizing from left and would go below minimum, adjust
        if new_width < min_w:
            if 'left' in edge:
                new_x = geo.x() + geo.width() - min_w
            new_width = min_w

        if new_height < min_h:
            if 'top' in edge:
                new_y = geo.y() + geo.height() - min_h
            new_height = min_h

        # Apply the new geometry
        self.setGeometry(new_x, new_y, new_width, new_height)

    def paintEvent(self, event):
        """
        Custom paint event to draw the frame border.

        This is called automatically by Qt whenever the window needs
        to be redrawn (on show, resize, etc.)
        """
        painter = QPainter(self)

        # Enable anti-aliasing for smoother edges
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Get panel height to know where frame ends
        panel_height = self.get_panel_height()
        frame_rect = self.rect().adjusted(0, 0, 0, -panel_height)

        # Fill with nearly-invisible color for mouse event handling
        # Skip during capture so screen shows through
        if not self._is_capturing:
            painter.fillRect(frame_rect, QColor(0, 0, 0, 1))

        # Set up the pen for drawing the border
        pen = QPen(self.BORDER_COLOR)
        pen.setWidth(self.BORDER_WIDTH)
        painter.setPen(pen)

        # Don't fill the rectangle (keep it transparent inside)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        # Draw the frame border (excluding panel area)
        border_rect = frame_rect.adjusted(
            self.BORDER_WIDTH // 2,
            self.BORDER_WIDTH // 2,
            -self.BORDER_WIDTH // 2 - 1,
            -self.BORDER_WIDTH // 2
        )

        # Draw all four sides of the frame border
        painter.drawLine(border_rect.topLeft(), border_rect.topRight())  # Top
        painter.drawLine(border_rect.topLeft(), border_rect.bottomLeft())  # Left
        painter.drawLine(border_rect.topRight(), border_rect.bottomRight())  # Right
        painter.drawLine(border_rect.bottomLeft(), border_rect.bottomRight())  # Bottom

        painter.end()
