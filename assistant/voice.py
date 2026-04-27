"""Voice recognition and text-to-speech module."""

import threading

import pyttsx3
import speech_recognition as sr


class VoiceEngine:
    """Handles voice recognition and text-to-speech."""

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        self._configure_tts()
        self._listening = False
        self._lock = threading.Lock()

    def _configure_tts(self):
        """Configure TTS engine settings."""
        voices = self.tts_engine.getProperty("voices")
        if voices:
            self.tts_engine.setProperty("voice", voices[0].id)
        self.tts_engine.setProperty("rate", 175)
        self.tts_engine.setProperty("volume", 0.9)

    def set_voice(self, index: int):
        """Set TTS voice by index."""
        voices = self.tts_engine.getProperty("voices")
        if 0 <= index < len(voices):
            self.tts_engine.setProperty("voice", voices[index].id)

    def set_rate(self, rate: int):
        """Set TTS speech rate."""
        self.tts_engine.setProperty("rate", rate)

    def set_volume(self, volume: float):
        """Set TTS volume (0.0 to 1.0)."""
        self.tts_engine.setProperty("volume", max(0.0, min(1.0, volume)))

    def speak(self, text: str):
        """Convert text to speech."""
        with self._lock:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()

    def speak_async(self, text: str, callback=None):
        """Speak text asynchronously."""

        def _speak():
            self.speak(text)
            if callback:
                callback()

        thread = threading.Thread(target=_speak, daemon=True)
        thread.start()

    def listen(self, timeout: int = 5, phrase_time_limit: int = 10) -> str:
        """Listen for voice input and return recognized text."""
        self._listening = True
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit,
                )
                text = self.recognizer.recognize_google(audio)
                return text.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return "[error] Speech recognition service unavailable"
        finally:
            self._listening = False

    def is_listening(self) -> bool:
        """Check if currently listening."""
        return self._listening

    def get_available_voices(self) -> list:
        """Return list of available TTS voices."""
        return self.tts_engine.getProperty("voices")
