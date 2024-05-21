import pandas as pd
import numpy as np

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
    #Pesquisa de usuários
    csv_file = 'pesquisa_grafos.csv'
    binary_vectors = csv_to_binary_vectors(csv_file)

    for i, vec in enumerate(binary_vectors):
        print(f'{i+1}: {vec}')

    todas_comparacoes = []
    num_comparacoes = 0
    for i in range (80):
        comparacoes = []
        for j in range(i+1, 80):
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

main()
