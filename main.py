"""Desktop AI Virtual Voice Assistant - Main Entry Point."""

import sys
import os

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from assistant.gui import AssistantGUI


def main():
    """Launch the Desktop AI Virtual Voice Assistant."""
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    app = QApplication(sys.argv)
    app.setApplicationName("Desktop AI Virtual Voice Assistant")
    app.setStyle("Fusion")

    window = AssistantGUI()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
