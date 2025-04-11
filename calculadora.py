from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QHBoxLayout, QGroupBox, QComboBox
)
from utils import carregar_embalagens
from presets_tab_ui import carregar_presets, CAMINHO_FILAMENTOS, CAMINHO_IMPRESSORAS, CAMINHO_ENERGIA

class CalculadoraTab(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()

        grupo_impressao = QGroupBox("🔧 Dados da Impressão")
        layout_impressao = QGridLayout()

        self.campos = {}
        self.combo_filamento = QComboBox()
        self.combo_impressora = QComboBox()
        self.combo_energia = QComboBox()

        self.filamentos = carregar_presets(CAMINHO_FILAMENTOS)
        self.impressoras = carregar_presets(CAMINHO_IMPRESSORAS)
        self.energias = carregar_presets(CAMINHO_ENERGIA)

        for f in self.filamentos:
            self.combo_filamento.addItem(f["nome"], f["valor"])
        for i in self.impressoras:
            self.combo_impressora.addItem(i["nome"], i["valor"])
        for e in self.energias:
            self.combo_energia.addItem(e["nome"], e["valor"])

        self.campos["Filamento usado (g):"] = QLineEdit()
        self.campos["Desgaste por hora (R$):"] = QLineEdit()

        layout_impressao.addWidget(QLabel("Filamento usado (g):"), 0, 0)
        layout_impressao.addWidget(self.campos["Filamento usado (g):"], 0, 1)
        layout_impressao.addWidget(QLabel("Tipo de Filamento:"), 1, 0)
        layout_impressao.addWidget(self.combo_filamento, 1, 1)
        layout_impressao.addWidget(QLabel("Impressora:"), 2, 0)
        layout_impressao.addWidget(self.combo_impressora, 2, 1)
        layout_impressao.addWidget(QLabel("Tarifa de Energia:"), 3, 0)
        layout_impressao.addWidget(self.combo_energia, 3, 1)
        layout_impressao.addWidget(QLabel("Desgaste por hora (R$):"), 4, 0)
        layout_impressao.addWidget(self.campos["Desgaste por hora (R$):"], 4, 1)

        self.tempo_h = QLineEdit(); self.tempo_m = QLineEdit(); self.tempo_s = QLineEdit()
        tempo_layout = QHBoxLayout()
        tempo_layout.addWidget(QLabel("Horas:")); tempo_layout.addWidget(self.tempo_h)
        tempo_layout.addWidget(QLabel("Minutos:")); tempo_layout.addWidget(self.tempo_m)
        tempo_layout.addWidget(QLabel("Segundos:")); tempo_layout.addWidget(self.tempo_s)
        layout_impressao.addWidget(QLabel("Tempo de Impressão:"), 5, 0)
        layout_impressao.addLayout(tempo_layout, 5, 1)

        grupo_impressao.setLayout(layout_impressao)
        main_layout.addWidget(grupo_impressao)

        grupo_embalagens = QGroupBox("📦 Embalagens Utilizadas")
        layout_embalagens = QVBoxLayout()
        self.embalagens = carregar_embalagens()
        self.embalagem_inputs = []
        for embalagem in self.embalagens:
            linha = QHBoxLayout()
            nome_label = QLabel(embalagem["nome"])
            qtd_input = QLineEdit()
            qtd_input.setPlaceholderText("Qtd")
            qtd_input.setMaximumWidth(60)
            linha.addWidget(nome_label)
            linha.addWidget(qtd_input)
            layout_embalagens.addLayout(linha)
            self.embalagem_inputs.append((embalagem, qtd_input))
        grupo_embalagens.setLayout(layout_embalagens)
        main_layout.addWidget(grupo_embalagens)

        grupo_final = QGroupBox("💰 Margem de Lucro")
        layout_final = QHBoxLayout()
        self.margem_input = QLineEdit()
        layout_final.addWidget(QLabel("Margem de Lucro (%):"))
        layout_final.addWidget(self.margem_input)
        self.botao = QPushButton("CALCULAR")
        self.botao.clicked.connect(self.calcular)
        layout_final.addWidget(self.botao)
        grupo_final.setLayout(layout_final)
        main_layout.addWidget(grupo_final)

        self.resultado = QLabel("")
        main_layout.addWidget(self.resultado)
        self.setLayout(main_layout)

    def calcular(self):
        try:
            filamento = float(self.campos["Filamento usado (g):"].text().replace(",", "."))
            preco_filamento = self.combo_filamento.currentData()
            potencia = self.combo_impressora.currentData()
            preco_kwh = self.combo_energia.currentData()
            desgaste = float(self.campos["Desgaste por hora (R$):"].text().replace(",", "."))
            horas = int(self.tempo_h.text() or 0)
            minutos = int(self.tempo_m.text() or 0)
            segundos = int(self.tempo_s.text() or 0)
            tempo_total_horas = horas + (minutos / 60) + (segundos / 3600)

            custo_filamento = (filamento / 1000) * preco_filamento
            consumo_kw = (potencia / 1000) * tempo_total_horas
            custo_energia = consumo_kw * preco_kwh
            custo_desgaste = desgaste * tempo_total_horas
            custo_embalagens = sum(
                embalagem["preco"] * int(input_qtd.text() or 0)
                for embalagem, input_qtd in self.embalagem_inputs if input_qtd.text().isdigit()
            )

            custo_total = custo_filamento + custo_energia + custo_desgaste + custo_embalagens
            margem = float(self.margem_input.text().replace(",", ".")) / 100 if self.margem_input.text() else 0
            lucro = custo_total * margem
            preco_final = custo_total + lucro

            texto = (
                f"📦 Filamento: R$ {custo_filamento:.2f}\n"
                f"⚡ Energia: R$ {custo_energia:.2f}\n"
                f"🛠️ Desgaste: R$ {custo_desgaste:.2f}\n"
                f"📬 Embalagens: R$ {custo_embalagens:.2f}\n"
                f"-----------------------------\n"
                f"💰 Total: R$ {custo_total:.2f}\n"
                f"📈 Lucro: R$ {lucro:.2f} ({margem*100:.0f}%)\n"
                f"🏷️ Preço Final: R$ {preco_final:.2f}"
            )
            self.resultado.setText(texto)
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))
