import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
import qdarkstyle
from calculadora import CalculadoraTab
from presets_tab_ui import PresetsTab


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora 3D")

        self.tabs = QTabWidget()
        self.calculadora_tab = CalculadoraTab()
        self.presets_tab = PresetsTab()

        # Conecta o sinal para atualizar dados da aba calculadora
        self.presets_tab.presets_atualizados.connect(self.calculadora_tab.recarregar_presets)
        self.presets_tab.presets_atualizados.connect(self.calculadora_tab.recarregar_embalagens)

        self.tabs.addTab(self.calculadora_tab, "Calculadora")
        self.tabs.addTab(self.presets_tab, "Presets")

        self.setCentralWidget(self.tabs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    window = AppWindow()
    window.show()
    sys.exit(app.exec())
