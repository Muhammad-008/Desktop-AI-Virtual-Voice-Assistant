"""Application launcher module for opening system and web apps."""

import platform
import subprocess
import webbrowser

SYSTEM = platform.system().lower()

WEB_APPS = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "gmail": "https://mail.google.com",
    "github": "https://github.com",
    "stackoverflow": "https://stackoverflow.com",
    "stack overflow": "https://stackoverflow.com",
    "wikipedia": "https://www.wikipedia.org",
    "twitter": "https://twitter.com",
    "x": "https://x.com",
    "facebook": "https://www.facebook.com",
    "instagram": "https://www.instagram.com",
    "linkedin": "https://www.linkedin.com",
    "reddit": "https://www.reddit.com",
    "spotify": "https://open.spotify.com",
    "netflix": "https://www.netflix.com",
    "amazon": "https://www.amazon.com",
    "chatgpt": "https://chat.openai.com",
    "maps": "https://maps.google.com",
    "google maps": "https://maps.google.com",
    "translate": "https://translate.google.com",
    "drive": "https://drive.google.com",
    "google drive": "https://drive.google.com",
    "docs": "https://docs.google.com",
    "google docs": "https://docs.google.com",
}

LINUX_APPS = {
    "notepad": ["gedit"],
    "text editor": ["gedit"],
    "terminal": ["gnome-terminal"],
    "file manager": ["nautilus"],
    "files": ["nautilus"],
    "calculator": ["gnome-calculator"],
    "settings": ["gnome-control-center"],
    "browser": ["xdg-open", "https://www.google.com"],
    "firefox": ["firefox"],
    "chrome": ["google-chrome"],
}

WINDOWS_APPS = {
    "notepad": ["notepad.exe"],
    "calculator": ["calc.exe"],
    "paint": ["mspaint.exe"],
    "file manager": ["explorer.exe"],
    "explorer": ["explorer.exe"],
    "cmd": ["cmd.exe"],
    "command prompt": ["cmd.exe"],
    "powershell": ["powershell.exe"],
    "task manager": ["taskmgr.exe"],
    "control panel": ["control.exe"],
    "settings": ["start", "ms-settings:"],
    "word": ["start", "winword"],
    "excel": ["start", "excel"],
    "powerpoint": ["start", "powerpnt"],
    "browser": ["start", "https://www.google.com"],
    "chrome": ["start", "chrome"],
    "edge": ["start", "msedge"],
}

MACOS_APPS = {
    "notepad": ["open", "-a", "TextEdit"],
    "text editor": ["open", "-a", "TextEdit"],
    "terminal": ["open", "-a", "Terminal"],
    "finder": ["open", "-a", "Finder"],
    "file manager": ["open", "-a", "Finder"],
    "calculator": ["open", "-a", "Calculator"],
    "settings": ["open", "-a", "System Preferences"],
    "safari": ["open", "-a", "Safari"],
    "browser": ["open", "-a", "Safari"],
    "chrome": ["open", "-a", "Google Chrome"],
    "music": ["open", "-a", "Music"],
    "notes": ["open", "-a", "Notes"],
}


def get_desktop_apps() -> dict:
    """Return app commands for the current platform."""
    if SYSTEM == "windows":
        return WINDOWS_APPS
    elif SYSTEM == "darwin":
        return MACOS_APPS
    return LINUX_APPS


def open_app(app_name: str) -> str:
    """Open an application by name. Returns status message."""
    app_name_lower = app_name.lower().strip()

    if app_name_lower in WEB_APPS:
        url = WEB_APPS[app_name_lower]
        webbrowser.open(url)
        return f"Opening {app_name} in your browser."

    desktop_apps = get_desktop_apps()
    if app_name_lower in desktop_apps:
        try:
            cmd = desktop_apps[app_name_lower]
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return f"Opening {app_name}."
        except FileNotFoundError:
            return f"Could not find {app_name} on your system."
        except Exception as e:
            return f"Error opening {app_name}: {e}"

    webbrowser.open(f"https://www.google.com/search?q={app_name}")
    return f"Searching for '{app_name}' on Google."


def get_available_apps() -> list:
    """Return list of all available app names."""
    apps = list(WEB_APPS.keys()) + list(get_desktop_apps().keys())
    return sorted(set(apps))
