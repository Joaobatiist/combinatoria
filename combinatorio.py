import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QLineEdit, QWidget, QMessageBox, QInputDialog

class Grafo:
    def __init__(self, vertices):
        self.vertices = vertices
        self.grafo = {i: [] for i in range(vertices)}

    def adicionar_aresta(self, u, v):
        self.grafo[u].append(v)
        self.grafo[v].append(u)  # Se for um grafo não-dirigido

    def dfs_util(self, v, visitado):
        visitado[v] = True
        for vizinho in self.grafo[v]:
            if not visitado[vizinho]:
                self.dfs_util(vizinho, visitado)

    def contar_componentes_conexos(self):
        visitado = [False] * self.vertices
        contagem = 0
        for v in range(self.vertices):
            if not visitado[v]:
                self.dfs_util(v, visitado)
                contagem += 1
        return contagem

def contar_caminhos(grafo, u, v, visitado, caminho_atual, total_caminhos, todos_caminhos):
    visitado[u] = True
    caminho_atual.append(u)

    if u == v:
        total_caminhos[0] += 1
        todos_caminhos.append(list(caminho_atual))  # Adiciona o caminho encontrado à lista
    else:
        for vizinho in grafo[u]:
            if not visitado[vizinho]:
                contar_caminhos(grafo, vizinho, v, visitado, caminho_atual, total_caminhos, todos_caminhos)

    caminho_atual.pop()
    visitado[u] = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Grafo Interface")
        self.setGeometry(100, 100, 400, 300)

        self.vertices_input = QLineEdit()
        self.vertices_input.setPlaceholderText("Número de vértices")

        self.add_edge_button = QPushButton("Adicionar Aresta")
        self.add_edge_button.clicked.connect(self.add_edge)

        self.count_components_button = QPushButton("Contar Componentes Conexos")
        self.count_components_button.clicked.connect(self.count_components)

        self.count_paths_button = QPushButton("Contar Caminhos entre Dois Vértices")
        self.count_paths_button.clicked.connect(self.count_paths)

        self.output_label = QLabel("")

        layout = QVBoxLayout()
        layout.addWidget(self.vertices_input)
        layout.addWidget(self.add_edge_button)
        layout.addWidget(self.count_components_button)
        layout.addWidget(self.count_paths_button)
        layout.addWidget(self.output_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.grafo = None

    def add_edge(self):
        vertices_text = self.vertices_input.text()
        if not vertices_text:
            QMessageBox.warning(self, "Erro", "Por favor, insira o número de vértices.")
            return

        if not self.grafo:
            try:
                vertices = int(vertices_text)
                self.grafo = Grafo(vertices)
            except ValueError:
                QMessageBox.warning(self, "Erro", "Número de vértices inválido.")
                return

        u, ok1 = self.get_vertex("Digite o primeiro vértice")
        v, ok2 = self.get_vertex("Digite o segundo vértice")

        if ok1 and ok2:
            self.grafo.adicionar_aresta(u, v)
            self.output_label.setText(f"Aresta adicionada entre {u} e {v}")

    def count_components(self):
        if self.grafo:
            componentes = self.grafo.contar_componentes_conexos()
            self.output_label.setText(f"O número de componentes conexos é: {componentes}")

    def count_paths(self):
        if self.grafo:
            u, ok1 = self.get_vertex("Digite o vértice de origem")
            v, ok2 = self.get_vertex("Digite o vértice de destino")

            if ok1 and ok2:
                visitado = [False] * self.grafo.vertices
                caminho_atual = []
                total_caminhos = [0]
                todos_caminhos = []
                contar_caminhos(self.grafo.grafo, u, v, visitado, caminho_atual, total_caminhos, todos_caminhos)
                self.output_label.setText(f"Total de caminhos encontrados: {total_caminhos[0]}\n")
                for caminho in todos_caminhos:
                    self.output_label.setText(self.output_label.text() + f"Caminho encontrado: {caminho}\n")

    def get_vertex(self, message):
        text, ok = QInputDialog.getInt(self, "Entrada de Vértice", message)
        return text, ok

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
