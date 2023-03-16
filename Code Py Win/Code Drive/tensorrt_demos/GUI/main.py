# pyside2-uic ui_interface.ui -o ui_interface.py
# pyside2-rcc resource.qrc -o resource_rc.py

from ui_interface import *
import sys

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())