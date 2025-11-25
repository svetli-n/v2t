# Voice-to-Text macOS App

A macOS application that captures microphone input, transcribes speech using a local Whisper model, and automatically types the transcribed text into the currently focused text input field.

## Features

- **Hotkey Control**: Press **Right Command** to toggle recording (Start/Stop)
- **Local Transcription**: Uses `faster-whisper` (base.en model) for offline speech-to-text
- **Automatic Text Injection**: Types transcribed text directly into any focused text field
- **Privacy-First**: All processing happens locally on your Mac

## Installation

### Option 1: Run from Source
```bash
# Clone the repository
git clone <repo-url>
cd v2t

# Install dependencies with uv
uv sync

# Run the app
uv run python main.py
```

### Option 2: Standalone App
```bash
# Build the app
./build_app.sh

# Move to Applications
mv dist/Voice-to-Text.app /Applications/

# Run from Applications folder or Spotlight
```

## Setup

### Required Permissions
The app requires the following macOS permissions:

1. **Microphone Access**: Allow when prompted
2. **Accessibility Access**: Required for keyboard input simulation
   - Go to **System Settings** > **Privacy & Security** > **Accessibility**
   - Add and enable your Terminal app (if running from source) or Voice-to-Text.app

## Usage

1. Launch the app
2. Press **Right Command** once to start recording
3. Speak your text
4. Press **Right Command** again to stop and transcribe
5. The transcribed text will be automatically typed into the focused text field

## Technical Details

- **Language**: Python 3.12
- **Transcription**: faster-whisper (Optimized Whisper implementation)
- **Audio**: sounddevice + numpy
- **Input Control**: pynput
- **Bundling**: PyInstaller

## Development

```bash
# Install dev dependencies
uv add --dev pyinstaller

# Build standalone app
./build_app.sh
```

## License

MIT
