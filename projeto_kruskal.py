import tkinter as tk
from tkinter import filedialog
import networkx as nx
import matplotlib.pyplot as plt
import csv
import sys

class Kruskal:
    def __init__(self):
        self.pai = {}
        self.nivel = {}

    def fazerConjunto(self, vertice):
        self.pai[vertice] = vertice
        self.nivel[vertice] = 0

    def encontrar(self, vertice):
        if self.pai[vertice] != vertice:
            self.pai[vertice] = self.encontrar(self.pai[vertice])
        return self.pai[vertice]

    def uniao(self, vertice1, vertice2):
        raiz1 = self.encontrar(vertice1)
        raiz2 = self.encontrar(vertice2)

        if raiz1 != raiz2:
            if self.nivel[raiz1] > self.nivel[raiz2]:
                self.pai[raiz2] = raiz1
            else:
                self.pai[raiz1] = raiz2
                if self.nivel[raiz1] == self.nivel[raiz2]:
                    self.nivel[raiz2] += 1

    def kruskal(self, arestas):
        arvore_minima = []

        for aresta in sorted(arestas, key=lambda x: x[2]):
            vertice1, vertice2, peso = aresta
            if self.encontrar(vertice1) != self.encontrar(vertice2):
                arvore_minima.append((vertice1, vertice2, peso))
                self.uniao(vertice1, vertice2)

        return arvore_minima

def lerArquivoCsv():
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])
    if caminho_arquivo:
        dados = []
        cont = 1
        with open(caminho_arquivo, newline='', encoding='utf-8') as csvfile:
            leitor = csv.reader(csvfile)
            next(leitor)  
            for linha in leitor:
                if len(linha) >= 2: 
                    dados.append((linha[-2], linha[-1], cont))
                    cont += 1
        return dados
    else:
        return None

def visualizarGrafo(arvore_minima):
    if arvore_minima:
        G = nx.Graph()
        for vertice1, vertice2, peso in arvore_minima:
            G.add_edge(vertice1, vertice2, weight=peso)

        posicao = nx.spring_layout(G)
        rotulos_arestas = nx.get_edge_attributes(G, 'weight')

        plt.figure(figsize=(10, 10))

        nx.draw_networkx_nodes(G, posicao, node_color='w')
        nx.draw_networkx_edges(G, posicao)
        nx.draw_networkx_labels(G, posicao)
        nx.draw_networkx_edge_labels(G, posicao, edge_labels=rotulos_arestas)

        plt.show()

def executarAlgoritmo():
    dados = lerArquivoCsv()
    if dados:
        algoritmo_kruskal = Kruskal()
        for aresta in dados:
            for vertice in aresta[:2]:
                if vertice not in algoritmo_kruskal.pai:
                    algoritmo_kruskal.fazerConjunto(vertice)
        arvore_minima = algoritmo_kruskal.kruskal(dados)
        print("Arestas da árvore geradora mínima:")
        for vertice1, vertice2, peso in arvore_minima:
            print(f"{vertice1} - {vertice2}: {peso}")
        visualizarGrafo(arvore_minima)

def fecharPrograma():
    sys.exit()

# Interface gráfica
raiz = tk.Tk()
raiz.title("Algoritmo de Kruskal")
raiz.geometry("600x200")

rotulo = tk.Label(raiz, text="Selecione um arquivo CSV para executar o algoritmo de Kruskal", font=("Arial", 12))
rotulo.pack(pady=10)

botao = tk.Button(raiz, text="Selecionar Arquivo CSV", command=executarAlgoritmo)
botao.pack(pady=5)

botao_sair = tk.Button(raiz, text="Sair", command=fecharPrograma)
botao_sair.pack(pady=5)

raiz.mainloop()