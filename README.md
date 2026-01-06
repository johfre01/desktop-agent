# Desktop Agent

A smart screenshot tool with AI-powered insights.

## Overview

Desktop Agent is a productivity application that allows you to:
- Capture specific regions of your screen using a transparent overlay frame
- Ask questions about captured images using an LLM (Claude)
- Get instant AI-powered analysis and insights

## Features

- **Transparent Overlay**: A movable, resizable frame that acts as a viewfinder
- **One-Click Capture**: Capture exactly what you see in the frame
- **AI Integration**: Ask questions about your screenshots (coming in Phase 8)
- **Minimal Interface**: Clean, distraction-free design

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/desktop-agent.git
   cd desktop-agent
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
cd src
python -m desktop_agent.main
```

## Project Structure

```
Desktop Agent/
├── docs/                    # Documentation
├── src/desktop_agent/       # Source code
├── screenshots/             # Captured images
├── requirements.txt         # Dependencies
└── PLAN.md                  # Development plan
```

## Development

This project is being developed as a learning exercise. See `PLAN.md` for the detailed development plan and `docs/` for phase-by-phase documentation.

## Requirements

- Python 3.11+
- PyQt6
- Pillow

## License

MIT License
