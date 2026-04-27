# Desktop AI Virtual Voice Assistant

A feature-rich desktop AI voice assistant built with Python, featuring voice recognition, text-to-speech, OpenAI integration, and a modern PyQt5 GUI.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green)
![OpenAI](https://img.shields.io/badge/AI-OpenAI-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

- **Voice Recognition** - Speak commands using your microphone (powered by SpeechRecognition + Google Speech API)
- **Text-to-Speech** - Assistant speaks responses back to you (powered by pyttsx3)
- **App Launching** - Open desktop apps (Notepad, Calculator, etc.) and web apps (YouTube, Google, GitHub, etc.)
- **AI Responses** - Intelligent conversation powered by OpenAI GPT (with smart fallback responses when no API key is set)
- **Weather Information** - Real-time weather data for any city (no API key required, uses wttr.in)
- **Date & Time** - Get current date and time information
- **System Control** - Volume control, mute/unmute, system info, battery status, screenshots, screen lock
- **Modern Dark GUI** - Beautiful dark-themed interface built with PyQt5

## Screenshots

The application features a sleek dark-themed interface with:
- Chat display area with timestamped messages
- Quick action buttons for common commands
- Microphone button for voice input
- Text input field for typed commands
- Real-time clock display
- Settings menu for API key and voice configuration

## Installation

### Prerequisites

- Python 3.8 or higher
- A working microphone (for voice input)
- Internet connection (for weather data and OpenAI API)

### System Dependencies

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install -y python3-pyaudio portaudio19-dev espeak
```

**macOS:**
```bash
brew install portaudio espeak
```

**Windows:**
PyAudio wheels are included with pip installation.

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Muhammad-008/Desktop-AI-Virtual-Voice-Assistant.git
cd Desktop-AI-Virtual-Voice-Assistant
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the assistant:
```bash
python main.py
```

## Usage

### Voice Commands

Click the microphone button or press it to start listening, then speak:

| Command | Action |
|---------|--------|
| "Open YouTube" | Opens YouTube in browser |
| "Open Notepad" | Opens text editor |
| "Open Google" | Opens Google in browser |
| "What is the time?" | Tells current time |
| "What is the date?" | Tells current date |
| "Weather in London" | Gets weather for London |
| "System info" | Shows system information |
| "Battery" | Shows battery status |
| "Volume 50" | Sets volume to 50% |
| "Mute" / "Unmute" | Toggles mute |
| "Screenshot" | Takes a screenshot |
| "Lock screen" | Locks the screen |

### Text Input

Type any command in the text input field and press Enter or click Send.

### AI Chat

Any input that doesn't match a specific command is processed by the AI engine:
- **With OpenAI API key**: Uses GPT for intelligent responses
- **Without API key**: Uses built-in pattern matching for basic responses

### Settings

- **Settings > Set OpenAI API Key**: Enter your OpenAI API key for GPT-powered responses
- **Settings > Voice Settings > Speech Rate**: Adjust how fast the assistant speaks (50-300)
- **Settings > Voice Settings > Speech Volume**: Adjust voice volume (0-100%)

## OpenAI API Setup (Optional)

To enable GPT-powered responses:

1. Get an API key from [OpenAI](https://platform.openai.com/api-keys)
2. Either:
   - Set it in the app via **Settings > Set OpenAI API Key**
   - Or set the environment variable: `export OPENAI_API_KEY="your-key-here"`

The assistant works without an API key using built-in fallback responses.

## Project Structure

```
Desktop-AI-Virtual-Voice-Assistant/
├── main.py                     # Application entry point
├── assistant/
│   ├── __init__.py
│   ├── gui.py                  # PyQt5 GUI interface
│   ├── voice.py                # Voice recognition & TTS engine
│   ├── ai_response.py          # OpenAI API integration & fallback responses
│   ├── app_launcher.py         # Application launcher (desktop & web apps)
│   ├── weather.py              # Weather, date, time information
│   ├── system_control.py       # System control features
│   └── utils.py                # Command routing utilities
├── requirements.txt            # Python dependencies
├── .gitignore
└── README.md
```

## Supported Platforms

- **Linux** (Ubuntu, Debian, Fedora, etc.)
- **Windows** (10, 11)
- **macOS**

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
