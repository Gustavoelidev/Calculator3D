import json
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QComboBox
)
from PyQt6.QtCore import pyqtSignal

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
CAMINHO_EMBALAGENS = "embalagens.json"



class PresetsTab(QWidget):
    presets_atualizados = pyqtSignal()  # sinal personalizado

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

        layout.addWidget(QLabel("Remover Impressora"))
        self.combo_remover_impressora = QComboBox()
        layout.addWidget(self.combo_remover_impressora)
        btn_remover_impressora = QPushButton("Remover Impressora Selecionada")
        btn_remover_impressora.clicked.connect(self.remover_impressora)
        layout.addWidget(btn_remover_impressora)

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

        layout.addWidget(QLabel("Remover Empresa de Energia"))
        self.combo_remover_energia = QComboBox()
        layout.addWidget(self.combo_remover_energia)
        btn_remover_energia = QPushButton("Remover Empresa Selecionada")
        btn_remover_energia.clicked.connect(self.remover_energia)
        layout.addWidget(btn_remover_energia)

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

        layout.addWidget(QLabel("Remover Filamento"))
        self.combo_remover_filamento = QComboBox()
        layout.addWidget(self.combo_remover_filamento)
        btn_remover_filamento = QPushButton("Remover Filamento Selecionado")
        btn_remover_filamento.clicked.connect(self.remover_filamento)
        layout.addWidget(btn_remover_filamento)

        # --- Embalagens ---
        layout.addWidget(QLabel("Adicionar Embalagem"))
        self.input_embalagem_nome = QLineEdit()
        self.input_embalagem_nome.setPlaceholderText("Nome da embalagem")
        layout.addWidget(self.input_embalagem_nome)

        self.input_embalagem_preco = QLineEdit()
        self.input_embalagem_preco.setPlaceholderText("Preço da embalagem")
        layout.addWidget(self.input_embalagem_preco)

        btn_add_embalagem = QPushButton("Adicionar Embalagem")
        btn_add_embalagem.clicked.connect(self.adicionar_embalagem)
        layout.addWidget(btn_add_embalagem)

        layout.addWidget(QLabel("Remover Embalagem"))
        self.combo_remover_embalagem = QComboBox()
        layout.addWidget(self.combo_remover_embalagem)

        btn_remover_embalagem = QPushButton("Remover Embalagem Selecionada")
        btn_remover_embalagem.clicked.connect(self.remover_embalagem)
        layout.addWidget(btn_remover_embalagem)


        self.setLayout(layout)
        self.atualizar_combos()

    def atualizar_combos(self):
        # Impressoras
        self.combo_remover_impressora.clear()
        self.impressoras = carregar_presets(CAMINHO_IMPRESSORAS)
        for item in self.impressoras:
            self.combo_remover_impressora.addItem(item["nome"])

        # Energia
        self.combo_remover_energia.clear()
        self.energias = carregar_presets(CAMINHO_ENERGIA)
        for item in self.energias:
            self.combo_remover_energia.addItem(item["nome"])

        # Filamentos
        self.combo_remover_filamento.clear()
        self.filamentos = carregar_presets(CAMINHO_FILAMENTOS)
        for item in self.filamentos:
            self.combo_remover_filamento.addItem(item["marca"])
        # Embalagens
        self.combo_remover_embalagem.clear()
        self.embalagens = carregar_presets(CAMINHO_EMBALAGENS)
        for item in self.embalagens:
            self.combo_remover_embalagem.addItem(item["nome"])

    def adicionar_impressora(self):
        nome = self.input_impressora_nome.text().strip()
        potencia = self.input_impressora_potencia.text().strip()
        if nome and potencia:
            try:
                potencia = float(potencia)
                lista = carregar_presets(CAMINHO_IMPRESSORAS)
                lista.append({"nome": nome, "potencia": potencia})
                salvar_presets(lista, CAMINHO_IMPRESSORAS)
                self.input_impressora_nome.clear()
                self.input_impressora_potencia.clear()
                self.atualizar_combos()
                self.presets_atualizados.emit()
                QMessageBox.information(self, "Sucesso", f"Impressora '{nome}' adicionada!")
            except ValueError:
                QMessageBox.warning(self, "Erro", "Potência deve ser um número válido.")
        else:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos da impressora.")

    def remover_impressora(self):
        index = self.combo_remover_impressora.currentIndex()
        if index >= 0:
            nome = self.combo_remover_impressora.currentText()
            confirm = QMessageBox.question(self, "Remover", f"Remover '{nome}'?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:
                del self.impressoras[index]
                salvar_presets(self.impressoras, CAMINHO_IMPRESSORAS)
                self.atualizar_combos()
                self.presets_atualizados.emit()

    def adicionar_energia(self):
        nome = self.input_energia_nome.text().strip()
        preco = self.input_energia_preco.text().strip()
        if nome and preco:
            try:
                preco = float(preco)
                lista = carregar_presets(CAMINHO_ENERGIA)
                lista.append({"nome": nome, "preco_kwh": preco})
                salvar_presets(lista, CAMINHO_ENERGIA)
                self.input_energia_nome.clear()
                self.input_energia_preco.clear()
                self.atualizar_combos()
                self.presets_atualizados.emit()
                QMessageBox.information(self, "Sucesso", f"Empresa '{nome}' adicionada!")
            except ValueError:
                QMessageBox.warning(self, "Erro", "Preço deve ser um número.")
        else:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos da empresa.")

    def remover_energia(self):
        index = self.combo_remover_energia.currentIndex()
        if index >= 0:
            nome = self.combo_remover_energia.currentText()
            confirm = QMessageBox.question(self, "Remover", f"Remover '{nome}'?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:
                del self.energias[index]
                salvar_presets(self.energias, CAMINHO_ENERGIA)
                self.atualizar_combos()
                self.presets_atualizados.emit()

    def adicionar_filamento(self):
        marca = self.input_filamento_marca.text().strip()
        preco = self.input_filamento_preco.text().strip()
        if marca and preco:
            try:
                preco = float(preco)
                lista = carregar_presets(CAMINHO_FILAMENTOS)
                lista.append({"marca": marca, "preco_kg": preco})
                salvar_presets(lista, CAMINHO_FILAMENTOS)
                self.input_filamento_marca.clear()
                self.input_filamento_preco.clear()
                self.atualizar_combos()
                self.presets_atualizados.emit()
                QMessageBox.information(self, "Sucesso", f"Filamento '{marca}' adicionado!")
            except ValueError:
                QMessageBox.warning(self, "Erro", "Preço deve ser um número.")
        else:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos do filamento.")

    def remover_filamento(self):
        index = self.combo_remover_filamento.currentIndex()
        if index >= 0:
            marca = self.combo_remover_filamento.currentText()
            confirm = QMessageBox.question(self, "Remover", f"Remover '{marca}'?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:
                del self.filamentos[index]
                salvar_presets(self.filamentos, CAMINHO_FILAMENTOS)
                self.atualizar_combos()
                self.presets_atualizados.emit()

    def adicionar_embalagem(self):
        nome = self.input_embalagem_nome.text().strip()
        preco = self.input_embalagem_preco.text().strip()
        if nome and preco:
            try:
                preco = float(preco)
                lista = carregar_presets(CAMINHO_EMBALAGENS)
                lista.append({"nome": nome, "preco": preco})
                salvar_presets(lista, CAMINHO_EMBALAGENS)
                self.input_embalagem_nome.clear()
                self.input_embalagem_preco.clear()
                self.atualizar_combos()
                self.presets_atualizados.emit()
                QMessageBox.information(self, "Sucesso", f"Embalagem '{nome}' adicionada!")
            except ValueError:
                QMessageBox.warning(self, "Erro", "Preço deve ser um número válido.")
        else:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos da embalagem.")

    def remover_embalagem(self):
        index = self.combo_remover_embalagem.currentIndex()
        if index >= 0:
            nome = self.combo_remover_embalagem.currentText()
            confirm = QMessageBox.question(self, "Remover", f"Remover '{nome}'?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:
                lista = carregar_presets(CAMINHO_EMBALAGENS)
                del lista[index]
                salvar_presets(lista, CAMINHO_EMBALAGENS)
                self.atualizar_combos()
                self.presets_atualizados.emit()

                    # Embalagens
        self.combo_remover_embalagem.clear()
        self.embalagens = carregar_presets(CAMINHO_EMBALAGENS)
        for item in self.embalagens:
            self.combo_remover_embalagem.addItem(item["nome"])


