import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def split_vector(vector):
    subvectors = []
    for i in range(0, len(vector), 3):
        subvectors.append(vector[i:i+3])
    return subvectors

def insert_node(G):
    node = int(input("Inserir vértice: "))
    if node not in G.nodes:
        G.add_node(node)
    return G

def remove_node(G):
    node = int(input("Vértice a ser removido: "))
    if node in G.nodes:
        G.remove_node(node)
    return G

def insert_weighted_edge(G):
    print("Inserir aresta com peso: ")
    edge_start = int(input("Vértice 1: "))
    edge_end = int(input("Vértice 2: "))
    weight_edge = int(input("Peso: "))
    if edge_start in G.nodes and edge_end in G.nodes:
        G.add_edge(edge_start, edge_end, weight=weight_edge)
    return G

def remove_weighted_edge(G):
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
    with open('teste.txt', 'r') as file:
        data = file.read()

    numbers = [int(num) for num in data.split()]
    tipo = numbers[0]
    len_nodes = numbers[1]
    nodes = numbers[2:len_nodes+2]
    edges = numbers[len_nodes+3:]
    edges = split_vector(edges)
    print("Arquivo lido com sucesso!\n")

    return tipo, nodes, edges

def write_file(G):
    aux = nx.get_edge_attributes(G, 'weight').values()
    weights = list(aux)
    x = 0

    with open('teste2.txt', 'w') as file:
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
    tipo, nodes, edges = read_file()

    print(f"Tipo do grafo: {tipo}")
    print(f"Número de vértices: {len(nodes)}")
    print(f"Vértices: {nodes}")
    print("As arestas são representadas por vetores que seguem o formato: \n---- [vértice 1, vértice 2, peso] ----\n")
    print(f"Número de arestas: {len(edges)}")
    print(f"Arestas: {edges}")

    return edges

def find_connectiviy(G):
    print("O grafo é CONEXO (não direcionado)")
    while True:
        print("\nMenu de opções: ")
        print("0. Encontrar a conectividade entre 2 pontos")
        print("1. Voltar ao menu principal")
        option = int(input("Selecione a opção desejada: "))
        if option == 0:
            a = int(input("Inserir vértice 1: "))
            b = int(input("Inserir vértice 2: "))
            con = nx.node_connectivity(G, a, b)
            print(f"Conectividade entre {a} e {b}: ", con)
        elif option == 1:
            break
        else:
            print("Opção inválida")

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
        print("8. Conexidade (& Conectividade)")
        print("9. Exit")
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
            break
        else:
            print("Opção Inválida!")

main()