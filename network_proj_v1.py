#Projeto de Grafos - Pontes Sociais
#Grupo: Camila Faleiros (10395818) & Fernanda Aiko (10395952)
#Aplicações com grafos - Projeto Entrega 2

file_path = 'grafo_v3.txt'

import networkx as nx
from networkx.algorithms import tree
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def csv_to_binary_vectors(csv_file):
    df = pd.read_csv(csv_file, sep=';', header=None, names=['nome', 'pos1', 'pos2', 'pos3', 'pos4', 'pos5'])
    binary_vectors = []

    for _, row in df.iterrows():
        binary_vector = np.zeros((17,), dtype=int)
    
        positions = [row['pos1'], row['pos2'], row['pos3'], row['pos4'], row['pos5']]
        for pos in positions:
            binary_vector[pos-1] = 1
        
        binary_vectors.append(binary_vector)
    
    return binary_vectors

def AND_operation_binary(vetor1, vetor2):
    return sum(a & b for a, b in zip(vetor1, vetor2))

def read_forms_and_format():
    '''
    Função para ler os dados da pesquisa e formatar os dados para serem utilizados no grafo.
    args: None
    return: None
    '''
    csv_file = 'pesquisa_grafos.csv'
    binary_vectors = csv_to_binary_vectors(csv_file)

    for i, vec in enumerate(binary_vectors):
        print(f'{i+1}: {vec}')

    todas_comparacoes = []
    num_comparacoes = 0
    for i in range (80):
        comparacoes = []
        # for j in range(i+1, 80):
        for j in range(80):
            if i == j:
                continue
            else:
                vetor1 = binary_vectors[i]
                vetor2 = binary_vectors[j]
                qtd_iguais = AND_operation_binary(vetor1, vetor2)
                comparacoes.append([i+1, j+1, qtd_iguais])
        comparacoes = sorted(comparacoes, key=lambda x: x[2], reverse=True)
        comparacoes = comparacoes[:6]
        num_comparacoes += len(comparacoes)
        todas_comparacoes.append(comparacoes)
        print(f'Vetor {i+1}: {comparacoes}')

    with open('grafo_v2.txt', 'w') as file:
        file.write("2\n")
        file.write(f"{len(binary_vectors)}"+"\n")
        for i in range (1, len(binary_vectors)+1):
            file.write(f"{i}"+"\n")
        file.write(f"{num_comparacoes-1}"+"\n")
        for i in todas_comparacoes:
            for j in i:  
                file.write(f"{j[0]} {j[1]} {j[2]}\n")

    with open('grafo_v3.txt', 'w') as file:
        file.write("2\n")
        file.write(f"{len(binary_vectors)}"+"\n")
        for i in range (1, len(binary_vectors)+1):
            file.write(f"{i}"+"\n")
        file.write(f"{num_comparacoes-1}"+"\n")
        for i in todas_comparacoes:
            for j in i:  
                file.write(f"{j[0]} {j[1]} {5-(j[2])}\n")

def split_vector(vector):
    '''
    Função para dividir um vetor em subvetores de tamanho 3, visto que a leitura do arquivo txt possui esse formato.
    args: vector (list)
    return: subvectors (list)
    '''
    subvectors = []
    for i in range(0, len(vector), 3):
        subvectors.append(vector[i:i+3])
    return subvectors

def insert_node(G):
    '''
    Função para inserir um vértice no grafo.
    args: G
    return: G
    '''
    node = int(input("Inserir vértice: "))
    if node not in G.nodes:
        G.add_node(node)
    return G

def remove_node(G):
    '''
    Função para remover um vértice do grafo.	
    args: G
    return: G
    '''
    node = int(input("Vértice a ser removido: "))
    if node in G.nodes:
        G.remove_node(node)
    return G

def insert_weighted_edge(G):
    '''
    Função para inserir aresta com peso no grafo.	
    args: G
    return: G
    '''
    print("Inserir aresta com peso: ")
    edge_start = int(input("Vértice 1: "))
    edge_end = int(input("Vértice 2: "))
    weight_edge = int(input("Peso: "))
    if edge_start in G.nodes and edge_end in G.nodes:
        G.add_edge(edge_start, edge_end, weight=weight_edge)
    return G

def remove_weighted_edge(G):
    '''
    Função para remover aresta do grafo.	
    args: G
    return: G
    '''
    print("Remover aresta com peso: ")
    while True:
        edge_start = int(input("Vértice 1: "))
        edge_end = int(input("Vértice 2: "))
        if (edge_start, edge_end) in G.edges:
            G.remove_edge(edge_start, edge_end)
            break
        else:
            print("Aresta não encontrada!")
    return G

def print_graph(G, edges):
    '''
    Função para apresentar visualmente o grafo.	
    args: G, edges (arestas)
    '''
    print("Vértices: ", G.nodes)
    print("Arestas: ", G.edges)
    print("Pesos das Arestas: ", nx.get_edge_attributes(G, 'weight'))

    while True:
        print("\nMenu de visualizações: ")
        print("1. FORMATO LISTA: Vértice: {Vértice Adjacente 1: {Peso da Aresta 1}, Vértice Adjacente 2: {Peso da Aresta 2}, ...}")
        print("2. FORMATO LISTA : Vértice -> Vértice Adjacente -> Peso da Aresta")
        print("3. Plotar grafo")
        print("4. Voltar ao menu principal")
        option = int(input("Selecione a opção desejada: "))
        if option == 1:
            network_list = nx.to_dict_of_dicts(G)
            print(f"FORMATO DE LISTA: {network_list}")
        elif option == 2:
            for i in edges:
                print(f"{i[0]} -> {i[1]} -> {i[2]}")
        elif option == 3:
            pos = nx.circular_layout(G)
            nx.draw(G, pos, with_labels=True, node_size=500, font_size=8, node_color='skyblue', edge_color='gray', width=1, alpha=0.7)
            plt.title('Grafo de relacionamentos')
            plt.show()
        elif option == 4:    
            break
        else:
            print("Opção inválida")


def read_file():
    '''
    Função para leitura do arquivo txt e formatar os dados para serem utilizados no grafo.	
    args: None
    return: tipo do grafo, vertices, arestas
    '''
    with open(file_path, 'r') as file:
        data = file.read()

    numbers = [int(num) for num in data.split()]
    tipo = numbers[0]
    len_nodes = numbers[1]
    nodes = numbers[2:len_nodes+2]
    _ = numbers[len_nodes+2]
    edges = numbers[len_nodes+3:]
    edges = split_vector(edges)
    print("Arquivo lido com sucesso!\n")

    return tipo, nodes, edges

def write_file(G):
    '''
    Função para escrever no arquivo .txt a partir do grafo.	
    args: G
    return: None
    '''
    aux = nx.get_edge_attributes(G, 'weight').values()
    weights = list(aux)
    x = 0

    with open(file_path, 'w') as file:
        file.write("2\n")
        file.write(f"{len(G.nodes)-1}"+"\n")
        for i in G.nodes:
            file.write(f"{i}"+"\n")
        file.write(f"{len(G.edges)-1}"+"\n")
        for i in G.edges:
            file.write(f"{i[0]} {i[1]} {weights[x]}"+"\n")
            x += 1
    print("Arquivo salvo com sucesso!\n")

def show_file():
    '''
    Função para mostrar o conteúdo do arquivo txt.
    args: None
    return: arestas formatadas
    '''
    tipo, nodes, edges = read_file()

    print(f"Tipo do grafo: {tipo}")
    print(f"Número de vértices: {len(nodes)}")
    print(f"Vértices: {nodes}")
    print("As arestas são representadas por vetores que seguem o formato: \n---- [vértice 1, vértice 2, peso] ----\n")
    print(f"Número de arestas: {len(edges)}")
    print(f"Arestas: {edges}")

    return edges

def find_connectiviy(G):
    '''
    Função para informar se o grafo é conexo.
    args: G
    return: None
    '''
    print("O grafo é CONEXO (não direcionado)")

def dijkstra(G):
    '''
    Função para encontrar o menor caminho entre dois vértices no grafo utilizando o algoritmo de Dijkstra.
    args: G
    return: None
    '''
    while True:
        print("\nMenu de opções: ")
        print("0. Encontrar menor caminho entre 2 vértices")
        print("1. Voltar ao menu principal")
        option = int(input("Selecione a opção desejada: "))
        if option == 0:
            a = int(input("Inserir vértice 1: "))
            b = int(input("Inserir vértice 2: "))
            print(f"Dijkstra: {nx.dijkstra_path(G, a, b)}")
        elif option == 1:
            break
        else:
            print("Opção inválida")


def bellman_ford(G):
    '''
    Função para encontrar o menor caminho entre dois vértices no grafo utilizando o algoritmo de Bellman-Ford.
    args: G
    return: None
    '''
    while True:
        print("\nMenu de opções: ")
        print("0. Encontrar menor caminho entre 2 vértices")
        print("1. Voltar ao menu principal")
        option = int(input("Selecione a opção desejada: "))
        if option == 0:
            a = int(input("Inserir vértice 1: "))
            b = int(input("Inserir vértice 2: "))
            print(f"Bellman-Ford: {nx.bellman_ford_path(G, a, b)}")
        elif option == 1:
            break
        else:
            print("Opção inválida")

def kruskal(G):
    '''
    Função para encontrar a árvore geradora mínima de um grafo utilizando o algoritmo de Kruskal.
    args: G
    return: None
    '''
    T = nx.minimum_spanning_tree(G, algorithm= 'kruskal')
    print(f"Árvore de Custo Mínimo - Kruskal: \n{T}")
    nx.draw(T, with_labels=True, node_size=500, font_size=8, node_color='skyblue', edge_color='gray', width=1, alpha=0.7)
    plt.show()

def prim(G):
    '''
    Função para encontrar a árvore geradora mínima de um grafo utilizando o algoritmo de Prim.
    args: G
    return: None
    '''
    T = nx.minimum_spanning_tree(G, algorithm= 'prim')
    print(f"Árvore de Custo Mínimo - Prim: \n{T}")
    nx.draw(T, with_labels=True, node_size=500, font_size=8, node_color='skyblue', edge_color='gray', width=1, alpha=0.7)
    plt.show()


def main():
    print("\n-----------Pontes Sociais - Projeto de Grafos-----------\nGrupo: Camlia Faleiros & Fernanda Aiko \nObjetivo: Criar relacionamentos a partir de objetivos similares entre os usuários.\n")
    G = nx.Graph()

    while True:
        print("\nMenu de opções: ")
        print("0. Leitura do Arquivo")
        print("1. Escrita do Arquivo")
        print("2. Inserir vértice")
        print("3. Remover vértice")
        print("4. Inserir aresta (com peso)")
        print("5. Remover aresta (com peso)")
        print("6. Mostrar arquivo")
        print("7. Mostrar grafo")
        print("8. Conexidade")
        print("9. Menor caminho entre 2 vértices (Dijkstra)")
        print("10. Menor caminho entre 2 vértices (Bellman-Ford)")
        print("11. Árvore geradora mínima (Kruskal)")
        print("12. Árvore geradora mínima (Prim)")
        print("13. Inserir novos resultados da pesquisa")
        print("14. Exit")
        option = int(input("\nSelecionar operação: "))
        if option == 0:
            _, nodes, numbers = read_file()
            G.add_nodes_from(nodes)
            G.add_weighted_edges_from(numbers)
        elif option == 1:
            write_file(G)
        elif option == 2:
            G = insert_node(G)
        elif option == 3:
            G = remove_node(G)
        elif option == 4:
            G = insert_weighted_edge(G)
        elif option == 5:
            G = remove_weighted_edge(G)
        elif option == 6:
            show_file()
        elif option == 7:
            print_graph(G, numbers)
        elif option == 8:
            find_connectiviy(G)
        elif option == 9:  
            dijkstra(G)
        elif option == 10:
            bellman_ford(G)
        elif option == 11:
            kruskal(G)
        elif option == 12:
            prim(G)
        elif option == 13:
            read_forms_and_format()
        elif option == 14:
            break
        else:
            print("Opção Inválida!")

main()