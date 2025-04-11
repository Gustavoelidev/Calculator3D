import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget
)
import qdarkstyle
from calculadora import CalculadoraTab
from embalagens import EmbalagensTab
from presets_tab_ui import PresetsTab

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora 3D - Gustavo")
        self.setGeometry(100, 100, 800, 600)
        tabs = QTabWidget()
        tabs.addTab(CalculadoraTab(), "Calculadora")
        tabs.addTab(EmbalagensTab(), "Embalagens")
        tabs.addTab(PresetsTab(), "Presets")
        self.setCentralWidget(tabs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    window = AppWindow()
    window.show()
    sys.exit(app.exec())
