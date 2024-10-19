from PyQt5.QtWidgets import QApplication
import sys
from gui import create_gui

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = create_gui()
    window.show()
    sys.exit(app.exec_())
