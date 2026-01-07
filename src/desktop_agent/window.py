"""
Desktop Agent - Main Window

This module contains the MainWindow class that serves as the primary
application window - a transparent overlay with a visible frame border
that can be dragged and resized.
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QPen, QColor


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
        self.setMinimumSize(200, 150)

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

        # Determine which edges we're near
        near_left = x < margin
        near_right = x > width - margin
        near_top = y < margin
        near_bottom = y > height - margin

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
        if edge is None:
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
            # Store starting position and geometry
            self._drag_start_pos = event.globalPosition().toPoint()
            self._drag_start_geometry = self.geometry()

            # Determine if we're resizing (edge) or dragging (center)
            self._resize_edge = self.get_edge_at_position(event.position().toPoint())

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
            self.move(new_pos)
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

        # Fill with nearly-invisible color to capture mouse events
        # (fully transparent areas don't receive mouse events)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 1))

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
