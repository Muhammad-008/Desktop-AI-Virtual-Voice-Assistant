"""PyQt5 GUI for the Desktop AI Virtual Voice Assistant."""

import sys
import threading
from datetime import datetime

from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette, QTextCursor
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QLineEdit,
    QLabel,
    QFrame,
    QStatusBar,
    QAction,
    QMenuBar,
    QInputDialog,
    QMessageBox,
    QSplitter,
    QGroupBox,
)

from assistant.voice import VoiceEngine
from assistant.ai_response import AIEngine
from assistant.utils import route_command


DARK_STYLESHEET = """
QMainWindow {
    background-color: #1a1a2e;
}
QWidget {
    background-color: #1a1a2e;
    color: #e0e0e0;
    font-family: 'Segoe UI', 'Arial', sans-serif;
}
QMenuBar {
    background-color: #16213e;
    color: #e0e0e0;
    border-bottom: 1px solid #0f3460;
    padding: 2px;
}
QMenuBar::item:selected {
    background-color: #0f3460;
}
QMenu {
    background-color: #16213e;
    color: #e0e0e0;
    border: 1px solid #0f3460;
}
QMenu::item:selected {
    background-color: #0f3460;
}
QTextEdit {
    background-color: #16213e;
    color: #e0e0e0;
    border: 1px solid #0f3460;
    border-radius: 8px;
    padding: 10px;
    font-size: 13px;
    selection-background-color: #533483;
}
QLineEdit {
    background-color: #16213e;
    color: #e0e0e0;
    border: 1px solid #0f3460;
    border-radius: 6px;
    padding: 10px;
    font-size: 14px;
}
QLineEdit:focus {
    border: 1px solid #533483;
}
QPushButton {
    background-color: #0f3460;
    color: #e0e0e0;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-size: 13px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #533483;
}
QPushButton:pressed {
    background-color: #e94560;
}
QPushButton#micButton {
    background-color: #e94560;
    border-radius: 25px;
    min-width: 50px;
    min-height: 50px;
    max-width: 50px;
    max-height: 50px;
    font-size: 18px;
}
QPushButton#micButton:hover {
    background-color: #ff6b6b;
}
QPushButton#micButton[listening="true"] {
    background-color: #4caf50;
}
QGroupBox {
    border: 1px solid #0f3460;
    border-radius: 8px;
    margin-top: 10px;
    padding-top: 15px;
    font-weight: bold;
    color: #e94560;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}
QStatusBar {
    background-color: #16213e;
    color: #888;
    border-top: 1px solid #0f3460;
}
QLabel#titleLabel {
    color: #e94560;
    font-size: 20px;
    font-weight: bold;
}
QLabel#statusLabel {
    color: #4caf50;
    font-size: 12px;
}
"""


class AssistantGUI(QMainWindow):
    """Main GUI window for the voice assistant."""

    response_signal = pyqtSignal(str, str)
    status_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.voice_engine = VoiceEngine()
        self.ai_engine = AIEngine()
        self._listening = False

        self.response_signal.connect(self._display_message)
        self.status_signal.connect(self._update_status)

        self._init_ui()
        self._init_menu()
        self._init_timer()

    def _init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Desktop AI Virtual Voice Assistant")
        self.setMinimumSize(800, 600)
        self.setStyleSheet(DARK_STYLESHEET)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Header
        header = QHBoxLayout()
        title = QLabel("AI Voice Assistant")
        title.setObjectName("titleLabel")
        header.addWidget(title)
        header.addStretch()

        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("statusLabel")
        header.addWidget(self.status_label)

        self.time_label = QLabel()
        self.time_label.setStyleSheet("color: #888; font-size: 12px;")
        header.addWidget(self.time_label)
        main_layout.addLayout(header)

        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #0f3460;")
        main_layout.addWidget(line)

        # Chat area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Consolas", 11))
        main_layout.addWidget(self.chat_display, stretch=1)

        # Quick action buttons
        actions_group = QGroupBox("Quick Actions")
        actions_layout = QHBoxLayout(actions_group)

        quick_buttons = [
            ("Time", "what is the time"),
            ("Date", "what is the date"),
            ("Weather", "weather in London"),
            ("System Info", "system information"),
            ("YouTube", "open youtube"),
            ("Google", "open google"),
        ]
        for label, cmd in quick_buttons:
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked, c=cmd: self._process_input(c))
            btn.setCursor(Qt.PointingHandCursor)
            actions_layout.addWidget(btn)

        main_layout.addWidget(actions_group)

        # Input area
        input_layout = QHBoxLayout()

        self.mic_button = QPushButton("\U0001F3A4")
        self.mic_button.setObjectName("micButton")
        self.mic_button.clicked.connect(self._toggle_listening)
        self.mic_button.setToolTip("Click to start/stop voice input")
        self.mic_button.setCursor(Qt.PointingHandCursor)
        input_layout.addWidget(self.mic_button)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(
            "Type a command or click the mic button to speak..."
        )
        self.input_field.returnPressed.connect(self._on_text_submit)
        input_layout.addWidget(self.input_field, stretch=1)

        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self._on_text_submit)
        send_btn.setCursor(Qt.PointingHandCursor)
        input_layout.addWidget(send_btn)

        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self._clear_chat)
        clear_btn.setCursor(Qt.PointingHandCursor)
        input_layout.addWidget(clear_btn)

        main_layout.addLayout(input_layout)

        # Status bar
        self.statusBar().showMessage("Desktop AI Virtual Voice Assistant | Ready")

        # Welcome message
        self._display_message(
            "Welcome! I'm your AI Voice Assistant. "
            "Type a command, click a quick action, or press the mic button to speak.",
            "assistant",
        )

    def _init_menu(self):
        """Initialize the menu bar."""
        menubar = self.menuBar()

        # Settings menu
        settings_menu = menubar.addMenu("Settings")

        api_action = QAction("Set OpenAI API Key", self)
        api_action.triggered.connect(self._set_api_key)
        settings_menu.addAction(api_action)

        voice_menu = settings_menu.addMenu("Voice Settings")

        rate_action = QAction("Speech Rate", self)
        rate_action.triggered.connect(self._set_speech_rate)
        voice_menu.addAction(rate_action)

        volume_action = QAction("Speech Volume", self)
        volume_action.triggered.connect(self._set_speech_volume)
        voice_menu.addAction(volume_action)

        # Help menu
        help_menu = menubar.addMenu("Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

        commands_action = QAction("Available Commands", self)
        commands_action.triggered.connect(self._show_commands)
        help_menu.addAction(commands_action)

    def _init_timer(self):
        """Initialize the clock timer."""
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self._update_clock)
        self.clock_timer.start(1000)
        self._update_clock()

    def _update_clock(self):
        """Update the time display."""
        now = datetime.now()
        self.time_label.setText(now.strftime("%I:%M:%S %p"))

    def _display_message(self, text: str, sender: str):
        """Display a message in the chat area."""
        timestamp = datetime.now().strftime("%H:%M:%S")

        if sender == "user":
            color = "#e94560"
            prefix = "You"
        else:
            color = "#4caf50"
            prefix = "Assistant"

        html = (
            f'<div style="margin: 5px 0;">'
            f'<span style="color: #666; font-size: 11px;">[{timestamp}]</span> '
            f'<span style="color: {color}; font-weight: bold;">{prefix}:</span> '
            f'<span style="color: #e0e0e0;">{text}</span>'
            f"</div>"
        )
        self.chat_display.append(html)
        self.chat_display.moveCursor(QTextCursor.End)

    def _update_status(self, status: str):
        """Update status label."""
        self.status_label.setText(status)
        self.statusBar().showMessage(f"Desktop AI Virtual Voice Assistant | {status}")

    def _on_text_submit(self):
        """Handle text input submission."""
        text = self.input_field.text().strip()
        if text:
            self.input_field.clear()
            self._process_input(text)

    def _process_input(self, text: str):
        """Process user input (text or voice)."""
        self._display_message(text, "user")
        self.status_signal.emit("Processing...")

        def _process():
            response, cmd_type = route_command(text)

            if cmd_type == "ai" and not response:
                response = self.ai_engine.get_response(text)

            self.response_signal.emit(response, "assistant")
            self.status_signal.emit("Ready")

            self.voice_engine.speak_async(response)

        thread = threading.Thread(target=_process, daemon=True)
        thread.start()

    def _toggle_listening(self):
        """Toggle voice listening on/off."""
        if self._listening:
            self._listening = False
            self.mic_button.setText("\U0001F3A4")
            self.mic_button.setProperty("listening", "false")
            self.mic_button.setStyle(self.mic_button.style())
            self.status_signal.emit("Ready")
            return

        self._listening = True
        self.mic_button.setText("\U0001F534")
        self.mic_button.setProperty("listening", "true")
        self.mic_button.setStyle(self.mic_button.style())
        self.status_signal.emit("Listening...")

        def _listen():
            text = self.voice_engine.listen(timeout=8, phrase_time_limit=15)
            self._listening = False
            self.mic_button.setText("\U0001F3A4")
            self.mic_button.setProperty("listening", "false")
            self.mic_button.setStyle(self.mic_button.style())

            if text and not text.startswith("[error]"):
                self._process_input(text)
            elif text.startswith("[error]"):
                self.response_signal.emit(text, "assistant")
                self.status_signal.emit("Error")
            else:
                self.status_signal.emit("No speech detected")

        thread = threading.Thread(target=_listen, daemon=True)
        thread.start()

    def _clear_chat(self):
        """Clear the chat display."""
        self.chat_display.clear()
        self.ai_engine.clear_history()
        self._display_message("Chat cleared. How can I help you?", "assistant")

    def _set_api_key(self):
        """Dialog to set OpenAI API key."""
        key, ok = QInputDialog.getText(
            self,
            "OpenAI API Key",
            "Enter your OpenAI API key:\n"
            "(Leave empty to use fallback responses)",
            QLineEdit.Password,
        )
        if ok:
            if key.strip():
                self.ai_engine.set_api_key(key.strip())
                self._display_message(
                    "OpenAI API key set. AI responses are now powered by GPT!",
                    "assistant",
                )
            else:
                self.ai_engine.set_api_key("")
                self._display_message(
                    "API key cleared. Using fallback responses.", "assistant"
                )

    def _set_speech_rate(self):
        """Dialog to set speech rate."""
        rate, ok = QInputDialog.getInt(
            self,
            "Speech Rate",
            "Enter speech rate (50-300):",
            175,
            50,
            300,
        )
        if ok:
            self.voice_engine.set_rate(rate)
            self._display_message(f"Speech rate set to {rate}.", "assistant")

    def _set_speech_volume(self):
        """Dialog to set speech volume."""
        vol, ok = QInputDialog.getInt(
            self,
            "Speech Volume",
            "Enter volume (0-100):",
            90,
            0,
            100,
        )
        if ok:
            self.voice_engine.set_volume(vol / 100.0)
            self._display_message(f"Speech volume set to {vol}%.", "assistant")

    def _show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About",
            "<h2>Desktop AI Virtual Voice Assistant</h2>"
            "<p>A feature-rich voice assistant with AI capabilities.</p>"
            "<p><b>Features:</b></p>"
            "<ul>"
            "<li>Voice Recognition (SpeechRecognition)</li>"
            "<li>Text-to-Speech (pyttsx3)</li>"
            "<li>App Launching</li>"
            "<li>OpenAI GPT Integration</li>"
            "<li>Weather Information</li>"
            "<li>System Control</li>"
            "</ul>"
            "<p>Built with PyQt5 and Python</p>",
        )

    def _show_commands(self):
        """Show available commands dialog."""
        QMessageBox.information(
            self,
            "Available Commands",
            "<h3>Voice & Text Commands</h3>"
            "<p><b>App Launching:</b></p>"
            "<ul>"
            "<li>'Open YouTube' - Opens YouTube</li>"
            "<li>'Open Notepad' - Opens text editor</li>"
            "<li>'Open Google' - Opens Google</li>"
            "<li>'Open [app name]' - Opens any supported app</li>"
            "</ul>"
            "<p><b>Information:</b></p>"
            "<ul>"
            "<li>'What is the time?' - Current time</li>"
            "<li>'What is the date?' - Current date</li>"
            "<li>'Weather in [city]' - Weather info</li>"
            "</ul>"
            "<p><b>System Control:</b></p>"
            "<ul>"
            "<li>'System info' - System information</li>"
            "<li>'Battery' - Battery status</li>"
            "<li>'Volume [0-100]' - Set volume</li>"
            "<li>'Mute' / 'Unmute' - Toggle mute</li>"
            "<li>'Screenshot' - Take screenshot</li>"
            "<li>'Lock screen' - Lock the screen</li>"
            "</ul>"
            "<p><b>AI Chat:</b></p>"
            "<ul>"
            "<li>Any other text triggers AI response</li>"
            "</ul>",
        )
