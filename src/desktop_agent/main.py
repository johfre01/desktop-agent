"""
Desktop Agent - Main Entry Point

This module serves as the entry point for the Desktop Agent application.
Run with: python -m desktop_agent.main
"""

import sys
from PyQt6.QtWidgets import QApplication

from desktop_agent.window import MainWindow


def main():
    """Main entry point for the Desktop Agent application."""
    print("Desktop Agent v0.1.0")
    print("Starting application...")

    # Create the Qt application
    # QApplication manages the GUI application's control flow and main settings
    app = QApplication(sys.argv)

    # Create and show the main window
    window = MainWindow()
    window.show()

    print("Window created. Close the window to exit.")

    # Start the event loop
    # exec() starts the main event loop and waits until exit() is called
    # sys.exit() ensures proper cleanup when the application closes
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
