# Desktop Agent - Project Plan

> A smart screenshot tool with AI-powered insights

---

## Overview

Desktop Agent is a productivity application that allows users to capture specific regions of their screen and interact with an LLM to ask questions about the captured content. The application features a transparent overlay frame that acts as a viewfinder for capturing screenshots.

**Key Features:**
- Transparent, movable, resizable overlay frame
- One-click screenshot capture of frame contents
- LLM integration for image analysis and Q&A
- Clean, minimal interface

---

## Project Structure

```
Desktop Agent/
├── docs/                          # Documentation and learning materials
│   ├── project-overview.html      # Main project overview
│   └── phases/                    # Phase-specific HTML pages
│       ├── phase-01-intro.html
│       ├── phase-01-summary.html
│       └── ...
├── src/                           # Source code
│   └── desktop_agent/             # Main package
│       ├── __init__.py
│       ├── main.py                # Application entry point
│       ├── window.py              # Main window class
│       ├── capture.py             # Screenshot functionality
│       ├── ui/                    # UI components
│       └── llm/                   # LLM integration
├── screenshots/                   # Captured images
├── tests/                         # Unit tests
├── requirements.txt               # Dependencies
├── PLAN.md                        # This file
└── README.md                      # Project readme
```

---

## Technology Stack

| Technology | Purpose |
|------------|---------|
| Python 3.11+ | Core programming language |
| PyQt6 | Desktop GUI framework |
| Pillow | Image processing |
| Anthropic SDK | Claude API integration |
| Git | Version control |

---

# Iteration 1: Core Application & Screenshot Capture

The first iteration focuses on building the core application with screenshot capture functionality.

---

## Phase 1: Project Setup & Foundations

### App Objective
Set up the complete project structure with all necessary files, virtual environment, and dependencies.

### Learning Objective
Understand professional Python project organization, virtual environments, and dependency management.

### Documentation
- [ ] Create `docs/phases/phase-01-intro.html` - Introduction to project setup
- [ ] Create `docs/phases/phase-01-summary.html` - Summary and key takeaways

### Implementation Tasks
- [ ] Create project folder structure
- [ ] Set up Python virtual environment
- [ ] Create `requirements.txt` with initial dependencies:
  ```
  PyQt6>=6.6.0
  Pillow>=10.0.0
  ```
- [ ] Install dependencies
- [ ] Create `src/desktop_agent/__init__.py`
- [ ] Create basic `src/desktop_agent/main.py` with entry point
- [ ] Initialize Git repository
- [ ] Create `.gitignore` file
- [ ] Make initial commit

### Key Concepts to Learn
- Virtual environments (`venv`)
- `pip` and `requirements.txt`
- Python package structure (`__init__.py`)
- Git basics: init, add, commit

---

## Phase 2: PyQt Fundamentals

### App Objective
Create a basic PyQt6 window that can be launched and closed.

### Learning Objective
Understand the PyQt6 framework basics: QApplication, QWidget, event loop, and the signal/slot mechanism.

### Documentation
- [ ] Create `docs/phases/phase-02-intro.html` - Introduction to PyQt6
- [ ] Create `docs/phases/phase-02-summary.html` - Summary and key takeaways

### Implementation Tasks
- [ ] Update `main.py` to create QApplication
- [ ] Create `src/desktop_agent/window.py` with basic QWidget class
- [ ] Implement window with title "Desktop Agent"
- [ ] Set initial window size (800x600)
- [ ] Add basic window close functionality
- [ ] Test running the application
- [ ] Commit changes to Git

### Key Concepts to Learn
- QApplication and event loop
- QWidget as base class
- Window properties (title, size, position)
- Running Qt applications
- Signals and slots introduction

---

## Phase 3: Transparent Overlay & Frame

### App Objective
Transform the window into a transparent overlay with a visible frame border.

### Learning Objective
Learn about frameless windows, window transparency, and custom painting with QPainter.

### Documentation
- [ ] Create `docs/phases/phase-03-intro.html` - Introduction to window customization
- [ ] Create `docs/phases/phase-03-summary.html` - Summary and key takeaways

### Implementation Tasks
- [ ] Make window frameless using `Qt.WindowType.FramelessWindowHint`
- [ ] Enable transparency with `Qt.WindowType.WA_TranslucentBackground`
- [ ] Set window to stay on top with `Qt.WindowType.WindowStaysOnTopHint`
- [ ] Override `paintEvent` to draw custom frame border
- [ ] Draw frame with visible border (e.g., 3px cyan/blue)
- [ ] Keep center transparent (pass-through visual)
- [ ] Add rounded corners to frame (optional)
- [ ] Test overlay appears correctly over other windows
- [ ] Commit changes to Git

### Key Concepts to Learn
- Qt Window Flags
- Frameless windows
- Transparency and translucent backgrounds
- QPainter basics
- Custom `paintEvent` override
- QPen and QBrush

---

## Phase 4: Drag & Resize Functionality

### App Objective
Enable users to drag the frame around the screen and resize it by dragging edges.

### Learning Objective
Master mouse event handling, window geometry manipulation, and cursor changes.

### Documentation
- [ ] Create `docs/phases/phase-04-intro.html` - Introduction to event handling
- [ ] Create `docs/phases/phase-04-summary.html` - Summary and key takeaways

### Implementation Tasks
- [ ] Override `mousePressEvent` to detect drag/resize start
- [ ] Override `mouseMoveEvent` to handle dragging
- [ ] Override `mouseReleaseEvent` to end drag/resize
- [ ] Implement edge detection for resize (detect which edge is being grabbed)
- [ ] Support resizing from all 4 edges and 4 corners
- [ ] Change cursor based on position (arrows for edges/corners)
- [ ] Set minimum window size (e.g., 200x150)
- [ ] Implement smooth dragging from anywhere in the frame
- [ ] Test drag and resize functionality
- [ ] Commit changes to Git

### Key Concepts to Learn
- Mouse events in Qt
- `QMouseEvent` and its properties
- Window geometry (`geometry()`, `setGeometry()`)
- Cursor types (`Qt.CursorShape`)
- Hit testing and regions

---

## Phase 5: Control Panel UI

### App Objective
Add the bottom control panel with Capture button and chat input field.

### Learning Objective
Learn Qt layouts, widget composition, and styling with QSS (Qt Style Sheets).

### Documentation
- [ ] Create `docs/phases/phase-05-intro.html` - Introduction to Qt layouts and styling
- [ ] Create `docs/phases/phase-05-summary.html` - Summary and key takeaways

### Implementation Tasks
- [ ] Create control panel widget as separate class
- [ ] Use QHBoxLayout for horizontal arrangement
- [ ] Add "Capture" QPushButton
- [ ] Add QLineEdit for chat input (placeholder text)
- [ ] Style the panel with dark background
- [ ] Style the button with gradient (match design)
- [ ] Style the input field
- [ ] Integrate panel into main window (bottom position)
- [ ] Update `paintEvent` to account for panel area (not transparent)
- [ ] Connect Capture button click (placeholder action for now)
- [ ] Test UI appearance and responsiveness
- [ ] Commit changes to Git

### Key Concepts to Learn
- QVBoxLayout and QHBoxLayout
- Widget composition
- QPushButton and QLineEdit
- Qt Style Sheets (QSS)
- Signal connections

---

## Phase 6: Screenshot Capture

### App Objective
Implement the core screenshot functionality that captures the screen region within the frame.

### Learning Objective
Understand screen capture APIs, image formats, and file I/O in Python.

### Documentation
- [ ] Create `docs/phases/phase-06-intro.html` - Introduction to screen capture
- [ ] Create `docs/phases/phase-06-summary.html` - Summary and key takeaways

### Implementation Tasks
- [ ] Create `src/desktop_agent/capture.py` module
- [ ] Create `screenshots/` folder for storing captures
- [ ] Implement capture logic:
  1. Hide the overlay window
  2. Calculate screen region coordinates
  3. Capture that region using `QScreen.grabWindow()`
  4. Show the overlay window again
- [ ] Save captured image as PNG with timestamp filename
- [ ] Add visual/audio feedback on capture (optional)
- [ ] Connect Capture button to capture function
- [ ] Handle multi-monitor setups
- [ ] Test capture on various screen regions
- [ ] Commit changes to Git

### Key Concepts to Learn
- QScreen and screen geometry
- `grabWindow()` method
- QPixmap and image saving
- File naming conventions
- Coordinate systems

---

# Iteration 2: LLM Integration & Polish

The second iteration adds AI capabilities and polishes the application.

---

## Phase 7: Settings & Configuration

### App Objective
Add settings management for save location, API keys, and user preferences.

### Learning Objective
Learn about configuration files, JSON handling, and application persistence.

### Documentation
- [ ] Create `docs/phases/phase-07-intro.html` - Introduction to configuration management
- [ ] Create `docs/phases/phase-07-summary.html` - Summary and key takeaways

### Implementation Tasks
- [ ] Create `src/desktop_agent/config.py` module
- [ ] Define configuration schema:
  - Screenshot save directory
  - API key storage
  - Default window size/position
  - UI preferences
- [ ] Implement config loading from JSON file
- [ ] Implement config saving
- [ ] Create default config if none exists
- [ ] Add settings dialog/menu (optional)
- [ ] Secure API key handling (not in plain text ideally)
- [ ] Test config persistence across app restarts
- [ ] Commit changes to Git

### Key Concepts to Learn
- JSON file handling
- Configuration patterns
- User data directories
- Security considerations for API keys

---

## Phase 8: LLM API Integration

### App Objective
Connect to Claude API for sending images and receiving AI analysis.

### Learning Objective
Understand REST APIs, async programming, and API authentication.

### Documentation
- [ ] Create `docs/phases/phase-08-intro.html` - Introduction to API integration
- [ ] Create `docs/phases/phase-08-summary.html` - Summary and key takeaways

### Implementation Tasks
- [ ] Add `anthropic` to requirements.txt
- [ ] Create `src/desktop_agent/llm/` package
- [ ] Create `src/desktop_agent/llm/client.py` for API client
- [ ] Implement image encoding (base64) for API
- [ ] Create function to send image with prompt to Claude
- [ ] Handle API responses
- [ ] Implement error handling (rate limits, network errors)
- [ ] Add loading state during API calls
- [ ] Test with sample image and prompt
- [ ] Commit changes to Git

### Key Concepts to Learn
- Anthropic/Claude API
- Base64 image encoding
- API authentication (API keys)
- Error handling for network calls
- Async considerations in Qt

---

## Phase 9: Chat Interface

### App Objective
Build a conversation interface for interacting with the AI about captured images.

### Learning Objective
Learn about state management, message handling, and building chat UIs.

### Documentation
- [ ] Create `docs/phases/phase-09-intro.html` - Introduction to chat interfaces
- [ ] Create `docs/phases/phase-09-summary.html` - Summary and key takeaways

### Implementation Tasks
- [ ] Create chat history data model
- [ ] Create expandable chat panel widget
- [ ] Display message bubbles (user and AI)
- [ ] Show captured image thumbnail in chat
- [ ] Connect text input to send messages
- [ ] Display AI responses in chat
- [ ] Add scroll area for message history
- [ ] Implement "new conversation" functionality
- [ ] Add loading indicator while waiting for AI
- [ ] Test full capture-to-chat flow
- [ ] Commit changes to Git

### Key Concepts to Learn
- Data models for chat
- QScrollArea
- Custom widgets for messages
- State management patterns
- Threading for responsiveness

---

## Phase 10: Polish & Packaging

### App Objective
Final refinements, comprehensive error handling, logging, and creating a distributable package.

### Learning Objective
Learn about logging, error handling best practices, and Python application packaging.

### Documentation
- [ ] Create `docs/phases/phase-10-intro.html` - Introduction to polish and packaging
- [ ] Create `docs/phases/phase-10-summary.html` - Summary and key takeaways

### Implementation Tasks
- [ ] Add logging throughout the application
- [ ] Implement comprehensive error handling
- [ ] Add keyboard shortcuts:
  - `Ctrl+Shift+C` for capture
  - `Escape` to close
  - `Enter` to send message
- [ ] Add system tray icon (optional)
- [ ] Create application icon
- [ ] Write README.md with usage instructions
- [ ] Test on clean system
- [ ] Create `setup.py` or `pyproject.toml` for packaging
- [ ] Test package installation
- [ ] Final Git commit and tag release
- [ ] Create `docs/phases/phase-10-final.html` - Project completion summary

### Key Concepts to Learn
- Python `logging` module
- Exception handling patterns
- Keyboard shortcuts in Qt
- Application packaging (setuptools/PyInstaller)
- Documentation best practices

---

## Quick Reference: Commands

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m desktop_agent.main

# Git commands
git init
git add .
git commit -m "message"
git log --oneline
```

---

## Progress Tracking

| Phase | Status | Started | Completed |
|-------|--------|---------|-----------|
| Phase 1: Project Setup | Not Started | - | - |
| Phase 2: PyQt Fundamentals | Not Started | - | - |
| Phase 3: Transparent Overlay | Not Started | - | - |
| Phase 4: Drag & Resize | Not Started | - | - |
| Phase 5: Control Panel UI | Not Started | - | - |
| Phase 6: Screenshot Capture | Not Started | - | - |
| Phase 7: Settings & Config | Not Started | - | - |
| Phase 8: LLM API Integration | Not Started | - | - |
| Phase 9: Chat Interface | Not Started | - | - |
| Phase 10: Polish & Packaging | Not Started | - | - |

---

## Notes

- Each phase builds on the previous one
- Complete all tasks in a phase before moving to the next
- The HTML intro/summary pages help reinforce learning
- Take time to experiment and understand each concept
- Don't hesitate to ask questions!

---

*Last Updated: January 2025*
