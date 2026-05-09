# Pomodoro Timer

A simple Pomodoro Timer application with both CLI and GUI versions for Windows.

## Features

- **25-minute work sessions** followed by **5-minute breaks**
- **Automatic cycling** between work and break
- **Terminal countdown** in MM:SS format (CLI version)
- **Graphical interface** with progress bar and controls (GUI version)
- **Beep sound** when sessions end
- **Session counter** (GUI version)
- **Stop with Ctrl+C** (CLI) or buttons (GUI)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/soragit-commits/pomodoro-timer.git
   cd pomodoro-timer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### CLI Version
Run the terminal-based timer:
```bash
python pomodoro.py
```
Or use the standalone executable:
```
dist\pomodoro.exe
```

### GUI Version
Run the graphical interface:
```bash
python pomodoro_gui.py
```
Or use the standalone executable:
```
dist\pomodoro_gui.exe
```

### Building Executables
To create standalone .exe files:
```bash
# CLI version
pyinstaller --onefile pomodoro.py

# GUI version
pyinstaller --onefile --windowed pomodoro_gui.py
```

Executables will be created in the `dist/` folder.

## Requirements

- Python 3.6+
- PyInstaller (for building executables)

## License

This project is open source. Feel free to use and modify.