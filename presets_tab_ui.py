import json
import os

def carregar_presets(caminho):
    if not os.path.exists(caminho):
        return []
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_presets(lista, caminho):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)

CAMINHO_FILAMENTOS = "filamentos.json"
CAMINHO_IMPRESSORAS = "impressoras.json"
CAMINHO_ENERGIA = "tarifas_energia.json"

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)


class PresetsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # --- Impressora ---
        layout.addWidget(QLabel("Adicionar Impressora"))
        self.input_impressora_nome = QLineEdit()
        self.input_impressora_nome.setPlaceholderText("Nome da impressora")
        layout.addWidget(self.input_impressora_nome)

        self.input_impressora_potencia = QLineEdit()
        self.input_impressora_potencia.setPlaceholderText("Potência (W)")
        layout.addWidget(self.input_impressora_potencia)

        btn_add_impressora = QPushButton("Adicionar Impressora")
        btn_add_impressora.clicked.connect(self.adicionar_impressora)
        layout.addWidget(btn_add_impressora)

        # --- Empresa de Energia ---
        layout.addWidget(QLabel("Adicionar Empresa de Energia"))
        self.input_energia_nome = QLineEdit()
        self.input_energia_nome.setPlaceholderText("Nome da empresa de energia")
        layout.addWidget(self.input_energia_nome)

        self.input_energia_preco = QLineEdit()
        self.input_energia_preco.setPlaceholderText("Preço por kWh (ex: 0.89)")
        layout.addWidget(self.input_energia_preco)

        btn_add_energia = QPushButton("Adicionar Empresa de Energia")
        btn_add_energia.clicked.connect(self.adicionar_energia)
        layout.addWidget(btn_add_energia)

        # --- Filamento ---
        layout.addWidget(QLabel("Adicionar Filamento"))
        self.input_filamento_marca = QLineEdit()
        self.input_filamento_marca.setPlaceholderText("Marca do filamento")
        layout.addWidget(self.input_filamento_marca)

        self.input_filamento_preco = QLineEdit()
        self.input_filamento_preco.setPlaceholderText("Preço por kg (ex: 99.90)")
        layout.addWidget(self.input_filamento_preco)

        btn_add_filamento = QPushButton("Adicionar Filamento")
        btn_add_filamento.clicked.connect(self.adicionar_filamento)
        layout.addWidget(btn_add_filamento)

        self.setLayout(layout)

    def adicionar_impressora(self):
        nome = self.input_impressora_nome.text().strip()
        potencia = self.input_impressora_potencia.text().strip()

        if nome and potencia:
            try:
                potencia = float(potencia)
                lista = carregar_presets(CAMINHO_IMPRESSORAS)
                lista.append({"nome": nome, "potencia": potencia})
                salvar_presets(lista, CAMINHO_IMPRESSORAS)
                QMessageBox.information(self, "Sucesso", f"Impressora '{nome}' adicionada!")
                self.input_impressora_nome.clear()
                self.input_impressora_potencia.clear()
            except ValueError:
                QMessageBox.warning(self, "Erro", "Potência deve ser um número.")
        else:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos da impressora.")

    def adicionar_energia(self):
        nome = self.input_energia_nome.text().strip()
        preco = self.input_energia_preco.text().strip()

        if nome and preco:
            try:
                preco = float(preco)
                lista = carregar_presets(CAMINHO_ENERGIA)
                lista.append({"nome": nome, "preco_kwh": preco})
                salvar_presets(lista, CAMINHO_ENERGIA)
                QMessageBox.information(self, "Sucesso", f"Empresa '{nome}' adicionada!")
                self.input_energia_nome.clear()
                self.input_energia_preco.clear()
            except ValueError:
                QMessageBox.warning(self, "Erro", "Preço deve ser um número.")
        else:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos da energia.")

    def adicionar_filamento(self):
        marca = self.input_filamento_marca.text().strip()
        preco = self.input_filamento_preco.text().strip()

        if marca and preco:
            try:
                preco = float(preco)
                lista = carregar_presets(CAMINHO_FILAMENTOS)
                lista.append({"marca": marca, "preco_kg": preco})
                salvar_presets(lista, CAMINHO_FILAMENTOS)
                QMessageBox.information(self, "Sucesso", f"Filamento '{marca}' adicionado!")
                self.input_filamento_marca.clear()
                self.input_filamento_preco.clear()
            except ValueError:
                QMessageBox.warning(self, "Erro", "Preço deve ser um número.")
        else:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos do filamento.")
