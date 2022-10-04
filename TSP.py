import random
import numpy as np
import networkx as nx

#coordenada das cidades
coordenadas = np.array([[1,2], [30,21], [56,23], [8,18], [20,50], [3,4], [11,6], [6,7], 
                       [15,20], [10,9], [12,12], [46,17], [60,55], [100,80], [16,13]])

#criando matriz de adjacência para um gráfico ponderado com base nas coordenadas fornecidas
def gerar_matriz(coordenadas):
    matriz = []
    for i in range(len(coordenadas)):
        for j in range(len(coordenadas)) :       
            p = np.linalg.norm(coordenadas[i] - coordenadas[j])
            matriz.append(p)
    matriz = np.reshape(matriz, (len(coordenadas),len(coordenadas)))
    #print(matriz)
    return matriz

#ache uma solução aleatória  
def solucao(matriz):
    pontos = list(range(0, len(matriz)))
    solucao = []
    for i in range(0, len(matriz)):
        random_point = pontos[random.randint(0, len(pontos) - 1)]
        solucao.append(random_point)
        pontos.remove(random_point)

    return solucao


#calculando o caminho com base na solução aleatória
def tamanho_caminho(matriz, solucao):
    ciclo_tamanho = 0
    for i in range(0, len(solucao)):
        ciclo_tamanho += matriz[solucao[i]][solucao[i - 1]]
    return ciclo_tamanho

#gera vizinhos da solução aleatória trocando cidades e retorna o melhor vizinho
def vizinhos(matriz, solucao):
    vizinhos = []
    for i in range(len(solucao)):
        for j in range(i + 1, len(solucao)):
            vizinho = solucao.copy()
            vizinho[i] = solucao[j]
            vizinho[j] = solucao[i]
            vizinhos.append(vizinho)
            
    #supondo que o primeiro vizinho da lista seja o melhor vizinho      
    melhor_vizinho = vizinhos[0]
    melhor_caminho = tamanho_caminho(matriz, melhor_vizinho)
    
    #verifique se há um vizinho melhor
    for vizinho in vizinhos:
        current_path = tamanho_caminho(matriz, vizinho)
        if current_path < melhor_caminho:
            melhor_caminho = current_path
            melhor_vizinho = vizinho
    return melhor_vizinho, melhor_caminho

#Algoritmo de hill climbing na esperança de achar a melhor solução
def hill_climbing(coordenadas):
    matriz = gerar_matriz(coordenadas)
    
    current_solucao = solucao(matriz)
    current_path = tamanho_caminho(matriz, current_solucao)
    vizinho = vizinhos(matriz,current_solucao)[0]
    melhor_vizinho, melhor_vizinho_path = vizinhos(matriz, vizinho)

    while melhor_vizinho_path < current_path:
        current_solucao = melhor_vizinho
        current_path = melhor_vizinho_path
        vizinho = vizinhos(matriz, current_solucao)[0]
        melhor_vizinho, melhor_vizinho_path = vizinhos(matriz, vizinho)

    return current_path, current_solucao

#Gerando o grafo do caminho
def grafo(coordenadas):
    final_solucao = hill_climbing(coordenadas)
    G = nx.DiGraph()
    temp = final_solucao[1]
    G.add_nodes_from(final_solucao[1])
    
    for i in range(1, len(final_solucao[1])):
        G.add_edge(temp[i - 1], temp[i])
    G.add_edge(temp[len(temp) - 1], temp[0])
    color_map = []
    for node in G:
        if node == final_solucao[1][0]:
            color_map.append('lime')
        else: 
            color_map.append('plum')
    nx.draw(G, with_labels = True, node_color = color_map, node_size = 1000)
    print("A solução é \n", final_solucao[1], "\nO tamanho do caminho é igual a \n", final_solucao[0])
    return

grafo(coordenadas)