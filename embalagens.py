from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QListWidget, QHBoxLayout, QMessageBox
)
from utils import carregar_embalagens, salvar_embalagens

class EmbalagensTab(QWidget):
    def __init__(self):
        super().__init__()
        self.embalagens = carregar_embalagens()
        layout = QVBoxLayout()
        nome_layout = QHBoxLayout()
        self.nome_input = QLineEdit()
        nome_layout.addWidget(QLabel("Nome:"))
        nome_layout.addWidget(self.nome_input)

        preco_layout = QHBoxLayout()
        self.preco_input = QLineEdit()
        preco_layout.addWidget(QLabel("Preço:"))
        preco_layout.addWidget(self.preco_input)

        botoes = QHBoxLayout()
        adicionar = QPushButton("Adicionar")
        remover = QPushButton("Remover")
        botoes.addWidget(adicionar)
        botoes.addWidget(remover)

        self.lista = QListWidget()
        self.atualizar_lista()

        adicionar.clicked.connect(self.adicionar)
        remover.clicked.connect(self.remover)

        layout.addLayout(nome_layout)
        layout.addLayout(preco_layout)
        layout.addLayout(botoes)
        layout.addWidget(self.lista)
        self.setLayout(layout)

    def atualizar_lista(self):
        self.lista.clear()
        for emb in self.embalagens:
            self.lista.addItem(f"{emb['nome']} - R$ {emb['preco']:.2f}")

    def adicionar(self):
        nome = self.nome_input.text().strip()
        try:
            preco = float(self.preco_input.text().replace(",", "."))
        except:
            QMessageBox.warning(self, "Erro", "Preço inválido.")
            return
        self.embalagens.append({"nome": nome, "preco": preco})
        salvar_embalagens(self.embalagens)
        self.nome_input.clear()
        self.preco_input.clear()
        self.atualizar_lista()

    def remover(self):
        idx = self.lista.currentRow()
        if idx >= 0:
            self.embalagens.pop(idx)
            salvar_embalagens(self.embalagens)
            self.atualizar_lista()
