"""System control features module."""

import os
import platform
import subprocess
from datetime import datetime

SYSTEM = platform.system().lower()


def get_system_info() -> str:
    """Return basic system information."""
    info = {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Architecture": platform.machine(),
        "Processor": platform.processor() or "N/A",
        "Python Version": platform.python_version(),
        "Hostname": platform.node(),
    }
    lines = [f"{k}: {v}" for k, v in info.items()]
    return "\n".join(lines)


def set_volume(level: int) -> str:
    """Set system volume (0-100)."""
    level = max(0, min(100, level))
    try:
        if SYSTEM == "linux":
            subprocess.run(
                ["amixer", "set", "Master", f"{level}%"],
                capture_output=True,
                check=True,
            )
        elif SYSTEM == "darwin":
            subprocess.run(
                ["osascript", "-e", f"set volume output volume {level}"],
                capture_output=True,
                check=True,
            )
        elif SYSTEM == "windows":
            # Uses nircmd if available on Windows
            subprocess.run(
                ["nircmd.exe", "setsysvolume", str(int(level * 655.35))],
                capture_output=True,
                check=True,
            )
        return f"Volume set to {level}%."
    except FileNotFoundError:
        return "Volume control tool not found on this system."
    except Exception as e:
        return f"Could not set volume: {e}"


def mute_volume() -> str:
    """Mute system volume."""
    try:
        if SYSTEM == "linux":
            subprocess.run(
                ["amixer", "set", "Master", "mute"],
                capture_output=True,
                check=True,
            )
        elif SYSTEM == "darwin":
            subprocess.run(
                ["osascript", "-e", "set volume output muted true"],
                capture_output=True,
                check=True,
            )
        elif SYSTEM == "windows":
            subprocess.run(
                ["nircmd.exe", "mutesysvolume", "1"],
                capture_output=True,
                check=True,
            )
        return "Volume muted."
    except Exception as e:
        return f"Could not mute volume: {e}"


def unmute_volume() -> str:
    """Unmute system volume."""
    try:
        if SYSTEM == "linux":
            subprocess.run(
                ["amixer", "set", "Master", "unmute"],
                capture_output=True,
                check=True,
            )
        elif SYSTEM == "darwin":
            subprocess.run(
                ["osascript", "-e", "set volume output muted false"],
                capture_output=True,
                check=True,
            )
        elif SYSTEM == "windows":
            subprocess.run(
                ["nircmd.exe", "mutesysvolume", "0"],
                capture_output=True,
                check=True,
            )
        return "Volume unmuted."
    except Exception as e:
        return f"Could not unmute volume: {e}"


def shutdown_system() -> str:
    """Shutdown the system."""
    try:
        if SYSTEM == "linux" or SYSTEM == "darwin":
            subprocess.run(["shutdown", "-h", "now"], check=True)
        elif SYSTEM == "windows":
            subprocess.run(["shutdown", "/s", "/t", "0"], check=True)
        return "Shutting down..."
    except Exception as e:
        return f"Could not shutdown: {e}"


def restart_system() -> str:
    """Restart the system."""
    try:
        if SYSTEM == "linux" or SYSTEM == "darwin":
            subprocess.run(["shutdown", "-r", "now"], check=True)
        elif SYSTEM == "windows":
            subprocess.run(["shutdown", "/r", "/t", "0"], check=True)
        return "Restarting..."
    except Exception as e:
        return f"Could not restart: {e}"


def lock_screen() -> str:
    """Lock the screen."""
    try:
        if SYSTEM == "linux":
            subprocess.run(["xdg-screensaver", "lock"], check=True)
        elif SYSTEM == "darwin":
            subprocess.run(
                [
                    "osascript",
                    "-e",
                    'tell application "System Events" to keystroke "q" '
                    'using {command down, control down}',
                ],
                check=True,
            )
        elif SYSTEM == "windows":
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], check=True)
        return "Screen locked."
    except Exception as e:
        return f"Could not lock screen: {e}"


def get_battery_status() -> str:
    """Get battery status if available."""
    try:
        if SYSTEM == "linux":
            result = subprocess.run(
                ["cat", "/sys/class/power_supply/BAT0/capacity"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return f"Battery level: {result.stdout.strip()}%"
            return "Battery information not available."
        elif SYSTEM == "darwin":
            result = subprocess.run(
                ["pmset", "-g", "batt"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return "Battery information not available."
        elif SYSTEM == "windows":
            result = subprocess.run(
                ["WMIC", "PATH", "Win32_Battery", "Get", "EstimatedChargeRemaining"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return f"Battery: {result.stdout.strip()}"
        return "Battery information not available."
    except Exception:
        return "Battery information not available."


def open_url_in_browser(url: str) -> str:
    """Open a URL in the default browser."""
    import webbrowser

    try:
        webbrowser.open(url)
        return f"Opening {url} in your browser."
    except Exception as e:
        return f"Could not open URL: {e}"


def take_screenshot() -> str:
    """Take a screenshot and save to desktop."""
    try:
        home = os.path.expanduser("~")
        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(home, "Desktop", filename)

        if SYSTEM == "linux":
            subprocess.run(
                ["gnome-screenshot", "-f", filepath],
                capture_output=True,
                check=True,
            )
        elif SYSTEM == "darwin":
            subprocess.run(
                ["screencapture", filepath],
                capture_output=True,
                check=True,
            )
        elif SYSTEM == "windows":
            subprocess.run(
                ["snippingtool.exe"],
                capture_output=True,
            )
            return "Snipping tool opened for screenshot."

        return f"Screenshot saved to {filepath}"
    except Exception as e:
        return f"Could not take screenshot: {e}"


def parse_system_command(text: str) -> str:
    """Parse and execute system control commands from text."""
    text_lower = text.lower()

    if "system info" in text_lower or "system information" in text_lower:
        return get_system_info()

    if "battery" in text_lower:
        return get_battery_status()

    if "screenshot" in text_lower:
        return take_screenshot()

    if "lock" in text_lower and "screen" in text_lower:
        return lock_screen()

    if "mute" in text_lower:
        if "unmute" in text_lower:
            return unmute_volume()
        return mute_volume()

    if "volume" in text_lower:
        import re

        numbers = re.findall(r"\d+", text)
        if numbers:
            return set_volume(int(numbers[0]))
        return "Please specify a volume level (0-100)."

    if "confirm shutdown" in text_lower:
        return shutdown_system()

    if "confirm restart" in text_lower:
        return restart_system()

    if "shutdown" in text_lower or "shut down" in text_lower:
        return "Are you sure you want to shutdown? Say 'confirm shutdown' to proceed."

    if "restart" in text_lower or "reboot" in text_lower:
        return "Are you sure you want to restart? Say 'confirm restart' to proceed."

    return ""
