#python tp_ia_daniel_reis.py 3 3 [[1,2,3],[4,5,6],[7,8,0]] [[1,2,3],[4,5,6],[7,8,0]] 0 1
#python tp_ia_daniel_reis.py 4 4 [[1,2,3,4],[5,6,7,8],[9,10,11,12],[15,13,14,0]] [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]] 0 1

import time
import random
from copy import copy, deepcopy
import sys

sizeRow = int(sys.argv[1])
sizeColumn = int(sys.argv[2])

fileResult = open('result' + sys.argv[6] + '.txt', 'a')
fileResultCsv = open('resultCSV' + sys.argv[6] + '.csv', 'a')
fileResultCsv.write('algorithm,beginTime,endTime,totalTime,pathCost,totalNodes,totalNodesExplored\n')

def printTextCSV(algorithm, beginTime, endTime, totalTime, pathCost, totalNodes, totalNodesExplored, totalNodesOpenNotExplored):
    #Insere texto no arquivo
    fileResultCsv.write(str(algorithm) + ',' + str(beginTime) + ',' + str(endTime) + ',' + str(totalTime) + ',' + str(pathCost) + ',' + str(totalNodes) + ',' + str(totalNodesExplored) + '\n')
    
def printText(text):
    print(text)                             #Imprime texto
    fileResult.write(str(text) + '\n')      #Insere texto no arquivo

def printTextInline(text):
    print(str(text) + ' ', end='')          #Imprime texto inline
    fileResult.write(str(text) + ' ')       #Insere texto no arquivo
    
def closeFileTXT():
    #fileResult.write('\n\n\n')
    fileResult.close()      #Fecha o arquivo

def closeFileCSV():
    #fileResultCsv.write(',,,,,,,,\n' + ',,,,,,,,\n' + ',,,,,,,,\n')
    fileResultCsv.close()   #Fecha o arquivo

class LoadMatrix:   
    def load(matrixInRow):        
        #Cria matriz somente com zeros
        M = []                                              #Cria matriz
        for i in range(sizeRow):                            #Para cada linha do arquivo
            li = []                                         #Cria uma lista que vai armazenar uma linha da matriz
            for j in range(sizeColumn):                     #Para cada coluna dessa linha
                li.append(0)                                #Preenche cada elemento com zero
            M.append(li)                                    #Adiciona a linha criada a matriz
        
        d = matrixInRow.split(',')                                                  #Separa os dados da matriz lida do arquivo
        for i in range(sizeRow):                                                    #Para cada linha da matriz
            for j in range(sizeColumn):                                             #Para cada coluna da matriz
                M[i][j] = int(d[sizeRow*i+j].replace('[','').replace(']',''))       #Preenche a matriz com os valores lidos do arquivo
        return M                                                                    #Retorna a matriz preenchida

class Node:
    def __init__(self, root, matrix, cost, costH):
        self.root = root
        self.matrix = matrix
        self.cost = cost
        self.costH = costH

    def setCost(self, cost):
        self.cost = cost
        
    def setCostH(self, costH):
        self.costH = costH
    
    def setRoot(self, root):
        self.root = root
    
    def getCost(self):
        return self.cost
    
    def getCostH(self):
        return self.costH
    
    def getRoot(self):
        return self.root
         
    def getMatrix(self):
        return self.matrix

class Result:
    def __init__(self, algorithm, timeBegin, timeEnd, lenFrontier, lenExplored, lenNodes, nodes, index):
        self.algorithm = algorithm
        self.timeBegin = timeBegin
        self.timeEnd = timeEnd
        self.lenFrontier = lenFrontier
        self.lenExplored = lenExplored
        self.lenNodes = lenNodes
        self.nodes = nodes
        self.index = index
    
    #Mostrar os resultados
    def printResultSearch(self):
        printText('Results')
        
        listPath = []
        while (self.index >= 0):
            listPath.append(self.index)
            self.index = self.nodes[self.index].getRoot()   
        listPath.reverse()
        
        if (len(listPath) > 0):
            printTextInline('Path:')
            for element in listPath:
                printTextInline(element)
            print('')
            for element in listPath:
                OperationsMatrix.printMatrix(self.nodes[element].getMatrix())
            printText('Path cost: ' + str(len(listPath)-1))
        else:
            printText('Path cost: 0')
        
        #printText('Begin time: ' + str(self.timeBegin) + ' ms')
        #printText('End time: ' + str(self.timeEnd) + ' ms')
        printText('Total time: ' + str(self.timeEnd-self.timeBegin) + ' s')
        printText('Total nodes: ' + str(self.lenNodes))
        printText('Total nodes explored: ' + str(self.lenExplored))
        printText('--------------------------------------------')
        printTextCSV(self.algorithm, self.timeBegin, self.timeEnd, (self.timeEnd-self.timeBegin), (len(listPath)-1), (len(self.nodes)), self.lenExplored, self.lenFrontier)
        
    #Mostrar os resultados
    def printResultSearch_(self, path, lenNodes):
        printText('Results')
        if (len(path) > 0):
            printText('Path:')
            for r in path:
                OperationsMatrix.printMatrix(r.getMatrix())
            printText('Path cost: ' + str(len(path)-1))
        else:
            printText('Path cost: 0')
        printText('Total time: ' + str(self.timeEnd-self.timeBegin) + ' s')
        printText('Total nodes: ' + str(lenNodes))
        printText('Total nodes explored: ' + str(self.lenExplored))
        printText('--------------------------------------------')
        printTextCSV(self.algorithm, self.timeBegin, self.timeEnd, (self.timeEnd-self.timeBegin), (len(path)-1), lenNodes, self.lenExplored, self.lenFrontier)

class OperationsMatrix:  
    #Gera matriz aleatória
    def generatorRandomMatrix():
        items = [x for x in range(sizeRow*sizeColumn)]      #Gera uma lista com valores de 1 até n
        random.shuffle(items)                               #Embaralha a lista
        
        #Cria matriz somente com zeros
        M = []                                              #Cria matriz
        for i in range(sizeRow):                            #Para cada linha do arquivo
            li = []                                         #Cria uma lista que vai armazenar uma linha da matriz
            for j in range(sizeColumn):                     #Para cada coluna dessa linha
                li.append(0)                                #Preenche cada elemento com zero
            M.append(li)                                    #Adiciona a linha criada a matriz
        
        for i in range(sizeRow):                            #Para cada linha da matriz
            for j in range(sizeColumn):                     #Para cada coluna da matriz
                M[i][j] = int(d[sizeRow*i+j])               #Preenche a matriz com os valores lidos do arquivo
        return M                                            #Retorna a matriz preenchida

    #Imprime a matriz
    def printMatrix(M):
        for i in range(sizeRow):                            #Percorre cada linha da matriz
            #printText(M[i])                                #Imprime o valor da linha
            printTextInline(M[i])                           #Imprime o valor da linha
        printText('')
    
    #Encontra a posição em que se encontra um valor na matriz
    def findPosition(M, value):
        posColumn = -1                                      #Supõe inicialmente que o valor procurado não está na matriz
        posRow = -1                                         #Supõe inicialmente que o valor procurado não está na matriz
        for i in range(sizeRow):                            #Para cada linha da matriz
            for j in range(sizeColumn):                     #Para cada coluna dessa linha
                if (M[i][j] == value):                      #Verifica se o elemento da posição atual na matriz é exatamente o elemento procurado
                    posRow = i                              #Se o elemento procurado foi encontrado, guarda a linha em que ele se encontra
                    posColumn = j                           #Se o elemento procurado foi encontrado, guarda a coluna em que ele se encontra
        return (posRow, posColumn)                          #Retorna a posição do elemento procurado na matriz (linha, coluna)
    
    #Encontra a posição em que se encontra na hash
    def getPosition(M, value):
        pos = 0                                             #Supõe inicialmente que o espaço em branco está na primeira posição da matriz
        for i in range(sizeRow):                            #Para cada linha da matriz
            for j in range(sizeColumn):                     #Para cada coluna dessa linha
                if (M[i][j] == value):                      #Verifica se o elemento da posição atual na matriz é exatamente o elemento procurado
                    return pos                              #Retorna a posição do elemento procurado na matriz
                pos = pos+1                                 #Avança o contador
        return 0                                            #Retorna a posição do elemento procurado na matriz
    
    #Troca elemento de posição na matriz
    def swapElementMatrix(M, posRow1, posColumn1, posRow2, posColumn2):
        aux = M[posRow1][posColumn1]                        #Guarda o valor da matrix[posRow1][posColumn1] em um valor auxiliar
        M[posRow1][posColumn1] = M[posRow2][posColumn2]     #Atualiza a matrix[posRow1][posColumn1] com o valor da matrix[posRow2][posColumn2]
        M[posRow2][posColumn2] = aux                        #Atualiza a matrix[posRow2][posColumn2] com o valor guardado em auxiliar
        return M                                            #Retorna a matriz atualizada
    
    #Encontra todos os posíveis movimentos para cada nó => analisa as possibilidades de mover o espaço em branco pra cima, baixo, direita e/ou esquerda
    #Nota: a ordem explorada interfere diretamente nos resultados finais
    def possibilityMoves(M, indexRoot, nodes):
        (posRow, posColumn) = OperationsMatrix.findPosition(M, 0)           #Procura o elemento '0' na matriz, ou seja, o espaço em branco
        possibility = []                                                    #Move elemento, ou seja, cria cada filho
        if (posColumn-1>=0):                    #Checa se é possível mover para esquerda => retroceder uma posição na coluna
            possibility.append(OperationsMatrix.swapElementMatrix(deepcopy(M), posRow, posColumn, posRow, posColumn-1))       #Move em x--
        if (posColumn+1<sizeColumn):            #Checa se é possível mover para direita => avançar uma posição na coluna
            possibility.append(OperationsMatrix.swapElementMatrix(deepcopy(M), posRow, posColumn, posRow, posColumn+1))       #Move em x++
        if (posRow-1>=0):                       #Checa se é possível mover para cima => retroceder uma posição na linha
            possibility.append(OperationsMatrix.swapElementMatrix(deepcopy(M), posRow, posColumn, posRow-1, posColumn))       #Move em y--
        if (posRow+1<sizeRow):                  #Checa se é possível mover para baixo => avançar uma posição na linha
            possibility.append(OperationsMatrix.swapElementMatrix(deepcopy(M), posRow, posColumn, posRow+1, posColumn))       #Move em y++
        
        #Elimina o que for igual ao avó, para não ter que consultar no vetor
        if (indexRoot > 0):
            for element in possibility:
                if (element == nodes[indexRoot].getMatrix()):
                    possibility.remove(element)
        return possibility
    
    #Checa se o estado atual é o estado objetivo
    def verifyGoal(M, goal):
        return (M == goal)                    #Caso não detectar nenhum elemento diferente, retorna verdadeiro, pois ambos são iguais
    
    #Inicializa a lista de explorados
    def initializeExplored():
        explored = []
        for i in range(sizeRow*sizeColumn):                     #Para o total de possições possíveis de conter a posição vazia
            listA = []                                          #Cria uma lista vazia
            for j in range(sizeRow*sizeColumn):                 #Para o total de possições possíveis de conter a posição vazia
                listB = []                                      #Cria uma lista vazia
                for k in range(sizeRow*sizeColumn):             #Para o total de possições possíveis de conter a posição vazia
                    listC = []                                  #Cria uma lista vazia
                    for m in range(sizeRow*sizeColumn):         #Para o total de possições possíveis de conter a posição vazia
                        listD = []                              #Cria uma lista vazia
                        for n in range(sizeRow*sizeColumn):     #Para o total de possições possíveis de conter a posição vazia
                            listD.append([])                    #Inclui uma lista vazia
                        listC.append(listD)                     #Inclui uma lista de listas vazia
                    listB.append(listC)                         #Inclui uma lista de lista de listas vazia
                listA.append(listB)                             #Inclui uma lista de lista de lista de listas vazias
            explored.append(listA)                              #Inclui uma lista de lista de lista de lista de listas vazias
        return explored                                         #Retorna a lista de listas inicializada
    
    #Calcula o tamanho da lista de explorados com base nas sublistas
    def getSizeExplored(explored):
        lenExplored = 0                                             #Inicializa o tamanho como zero
        for eListA in explored:                                     #Percorre cada sublista
            for eListB in eListA:                                   #Percorre cada sublista
                for eListC in eListB:                               #Percorre cada sublista
                    for eListD in eListC:                           #Percorre cada sublista
                        for e in eListD:                            #Percorre cada sublista
                            lenExplored = lenExplored+len(e)        #Contabiliza o tamanho de cada sublista
        return lenExplored                                          #Retorna o valor total
    
    #Checa se o nó está entre os explorados
    def verifyNodeIsExplored(M, explored, nodes):
        pos1 = OperationsMatrix.getPosition(M, 0)               #Pega a posição da sublista em que o elemento está na lista de explorados
        pos2 = OperationsMatrix.getPosition(M, 2)               #Pega a posição da sublista em que o elemento está na sublista da lista de explorados
        pos3 = OperationsMatrix.getPosition(M, 4)               #Pega a posição da sublista em que o elemento está na sublista da lista de explorados
        pos4 = OperationsMatrix.getPosition(M, 6)               #Pega a posição da sublista em que o elemento está na sublista da lista de explorados
        pos5 = OperationsMatrix.getPosition(M, 8)               #Pega a posição da sublista em que o elemento está na sublista da lista de explorados
        for index in explored[pos1][pos2][pos3][pos4][pos5]:    #Percorre cada elemento dos explorados
            if (M == nodes[index].getMatrix()):                 #Verifica se o elemento observado no momento entre os explorados é igual ao elemento procurado
                return index                                    #Caso seja, retorna o índice desse elemento na lista de explorados
        return -1                                               #Caso não encontre o elemento entre os explorados, retorna -1

    #Checa se o nó está na fronteira
    def verifyNodeIsFrontier(M, frontier, nodes):
        pos = 0
        for index in frontier:                          #Percorre cada elemento da fronteira
            if (M == nodes[index].getMatrix()):         #Verifica se o elemento observado no momento na fronteira é igual ao elemento procurado
                return pos                              #Caso seja, retorna o índice desse elemento na fronteira
            pos = pos+1                                 #Avança uma posição
        return -1                                       #Caso não encontre o elemento na fronteira, retorna -1
    
    #Retorna o índice do nó com menor custo
    def getIndexNodeMinCost(listIndex, listNode):
        if (len(listIndex) > 0):                                                            #Verifica se a lista tem pelo menos algum elemento
            cont = 0                                                                        #Variável que representa a posição atual em que se está na lista
            minIndex = 0                                                                    #Variável que representa o índice do menor elemento da lista
            minCost = listNode[minIndex].getCost() + listNode[minIndex].getCostH()          #Calcula o custo total (custo real + custo heurisitico) da posição inicial
            for element in listIndex:                                                       #Percorre cada elemento da lista
                totalCost = listNode[element].getCost() + listNode[element].getCostH()      #Calcula o custo total (custo real + custo heurisitico) da posição atual
                if (totalCost < minCost):                                                   #Se o custo total da posição atual for menor que o mínimo conhecido
                    minIndex = cont                                                         #Atualiza o índice do menor valor conhecido
                    minCost = totalCost                                                     #Atualiza o valor do menor valor conhecido
                cont = cont+1                                                               #Avança uma posição na lista
            return minIndex                                                                 #Retorna o índice do elemento com menor custo
        return None                                                                         #Lista vazia, ou seja, não existe elemento com menor custo

    #Calcula o custo com base na heurisitica escolhida
    def getHeuristCost(M, goal, heurist):
        if (heurist == 1):
            return OperationsMatrix.getHeuristCost1(M, goal)        #Heuristica 1
        elif (heurist == 2):
            return OperationsMatrix.getHeuristCost2(M, goal)        #Heuristica 2

    #Heurística 1: Número de quadrados em uma posição errada
    def getHeuristCost1(M, goal):
        value = 0                                           #Número de quadrados em uma posição errada
        for i in range(sizeRow):                            #Percorre cada linha da matriz
            for j in range(sizeColumn):                     #Percorre cada coluna da matriz
                element = goal[i][j]
                if (element > 0 and M[i][j] != element):    #Não considera o espaço em branco. Se o valor na mesma posição é diferente nas duas matrizes
                    value = value+1                         #Incrementa o contador
        return value                                        #Retorna o valor
    
    #Heurística 2: Manhattan Distance
    def getHeuristCost2(M, goal):
        value = 0                                                                       #Soma das distâncias que separam os quadrados das posições finais
        for i in range(sizeRow):                                                        #Percorre cada linha da matriz
            for j in range(sizeColumn):                                                 #Percorre cada coluna da matriz
                element = goal[i][j]
                if (element > 0):                                                           #Não considera o espaço em branco
                    (posRow, posColumn) = OperationsMatrix.findPosition(M, element)         #Procura na matriz M, o valor da posição atual observado no objetivo
                    distanceX = abs(i-posRow)                                               #Calcula a distância em X usando o módulo (abs)
                    distanceY = abs(j-posColumn)                                            #Calcula a distância em X usando o módulo (abs)
                    value = value + distanceX + distanceY                                   #Soma as distâncias
                    #printText(str(M) + ' ' + str(goal) + '+' + str(distanceX + distanceY))
        #printText(str(M) + ' ' + str(value))
        return value                                                                    #Retorna o valor total
    
    #Define a posição para inserir o elemento na fronteira, assumindo-se que a fronteira é uma lista em que inserimos os elementos de forma ordenada
    def getPositionInsert(nodes, listElement, cost, costH):
        ctei = (cost + costH)                                           #Custo total do elemento a ser inserido
        lenListElement = len(listElement)                               #Tamanho da lista de elementos
        
        if (lenListElement == 0):                           #Se a fronteira está vazia
            return 0                                        #Insere no início
        
        node_init = nodes[listElement[0]]                               #Elemento initial da fronteira a ser comparado
        ctef_init = (node_init.getCost() + node_init.getCostH())        #Custo total do elemento da fronteira[0]
                    
        node_end = nodes[listElement[lenListElement-1]]                 #Elemento final da fronteira a ser comparado
        ctef_end = (node_end.getCost() + node_end.getCostH())           #Custo total do elemento da fronteira[lenFrontier-1]
        
        if (ctef_init >= ctei):                             #Se o elemento tem custo total menor que o do primeiro
            return 0                                        #Insere no início
        elif (ctef_end <= ctei):                            #Se o elemento tem custo total maior que o do último
            return lenListElement                           #Insere no fim
        else:
            #Busca binária
            l = 0                       #Começa com a esquerda na posição inicial do vetor
            r = lenListElement-1        #Começa com a direita na posição final do vetor

            while (l <= r and l > 0 and r > 0):
                m = int((l + r) / 2)        #Calcula o meio

                node = nodes[listElement[m]]                                    #Elemento atual da fronteira a ser comparado
                ctef = (node.getCost() + node.getCostH())                       #Custo total do elemento da fronteira[m]

                if ((m+1) < lenListElement):                                        #Verifica se o elemento está no intervalo entre listElement[m] e listElement[m+1]
                    node_prox = nodes[listElement[m+1]]                             #Elemento atual da fronteira a ser comparado
                    ctef_prox = (node_prox.getCost() + node_prox.getCostH())        #Custo total do elemento da fronteira[m+1]
                
                    if ((ctei >= ctef) and (ctef_prox >= ctei)):     #Está entre listElement[m] e listElement[m+1]
                        return m+1
                if ((m-1) > 0):                                                     #Verifica se o elemento está no intervalo entre listElement[m-1] e listElement[m]
                    node_ant = nodes[listElement[m-1]]                              #Elemento atual da fronteira a ser comparado
                    ctef_ant = (node_ant.getCost() + node_ant.getCostH())           #Custo total do elemento da fronteira[m-1]
                    
                    if ((ctei >= ctef_ant) and (ctef >= ctei)):      #Está entre listElement[m-1] e listElement[m]
                        return m
                elif ctei > ctef:            #É maior que listElement[m]
                    l = m
                else:                        #É menor que listElement[m]
                    r = m
            return lenListElement            #Insere no fim

class SearchWithoutInformation:       
    def breadthFirstSearch(M, goal):
        timeBegin = time.time()
        
        #Verifica se o nó atual é igual ao objetivo
        if (OperationsMatrix.verifyGoal(M, goal)):
            timeEnd = time.time()
            result = Result("breadthFirstSearch", timeBegin, timeEnd, 0, 0, 0, [], -1)
            result.printResultSearch()
            return
            
        #Inicializa a lista de nós como vazia
        nodes = []
        index = -1
        nodes.append(Node(index, M, 0, 0))
            
        #Inicializa a fronteira
        frontier = []
        #Insere na fronteira o primeiro nó (Nó inicial)
        frontier.append(0)
        #Inicializa a lista de nós explorados como vazia
        explored = OperationsMatrix.initializeExplored()
            
        #Loop => Enquanto a fronteira não estiver vazia
        while(len(frontier) > 0):                    
            #Atualiza nó => Seleciona o primeiro elemento da fronteira
            index = frontier.pop(0)
            M = nodes[index].getMatrix()
                
            #Marca o nó como explorado
            explored[OperationsMatrix.getPosition(M, 0)][OperationsMatrix.getPosition(M, 2)][OperationsMatrix.getPosition(M, 4)][OperationsMatrix.getPosition(M, 6)][OperationsMatrix.getPosition(M, 8)].append(index)
                
            #printTextInline(M)
            #printTextInline(' ==> ')
                
            #Explora cada filho gerado
            for children in OperationsMatrix.possibilityMoves(M, nodes[index].getRoot(), nodes):
                #Verifica se o nó não está entre os explorados e não está na fronteira
                if (OperationsMatrix.verifyNodeIsExplored(children, explored, nodes) < 0 and OperationsMatrix.verifyNodeIsFrontier(children, frontier, nodes) < 0):
                    #Verifica se o nó é igual a solução objetivo
                    if (OperationsMatrix.verifyGoal(children, goal)):
                        timeEnd = time.time()
                        #Insere o resultado na lista de nós
                        nodes.append(Node(index, children, 0, 0))
                        #Insere o resultado na fronteira
                        frontier.append(len(nodes)-1)
                        #Atualiza o índice do último nó
                        index = len(nodes)-1
                        #Mostra o resultado
                        result = Result("breadthFirstSearch", timeBegin, timeEnd, len(frontier), OperationsMatrix.getSizeExplored(explored), len(nodes), nodes, index)
                        result.printResultSearch()
                        return
                        
                    #printTextInline(children)
                    #printTextInline('  ')
                    
                    #Adiciona nó na fronteira
                    nodes.append(Node(index, children, 0, 0))
                    frontier.append(len(nodes)-1)
                    #printMatrix(children)
                
            #printText('')
            #printText(str(len(frontier)) + ' === ' + str(OperationsMatrix.getSizeExplored(explored)))
                
            #Imprime a fronteira
            #countFrontier = 1
            #for index in frontier:
                #printText('Element frontier ' + str(countFrontier))
                #printMatrix(nodes[index].getMatrix())
                #countFrontier = countFrontier+1

    def uniformCostSearch(M, goal):
        timeBegin = time.time()
        
        #Define o custo real do nó inicial como zero
        pathCost = 0
        
        #Inicializa a lista de nós como vazia
        nodes = []
        index = -1
        nodes.append(Node(index, M, pathCost, 0))
        
        #Inicializa a fronteira
        frontier = []
        #Insere na fronteira o primeiro nó (Nó inicial)
        frontier.append(0)
        #Inicializa a lista de nós explorados como vazia
        explored = OperationsMatrix.initializeExplored()
        
        #Loop => Enquanto a fronteira não estiver vazia
        while(len(frontier) != 0):  
            #Atualiza nó => Seleciona o nó de menor custo (Apenas real) da fronteira
            index = frontier.pop(0)
            M = nodes[index].getMatrix()
            
            #Imprime a iteração
            #printText('Iteration => ' + str(pathCost))
            #OperationsMatrix.printMatrix(M)
            
            #Verifica se o nó atual é igual ao objetivo
            if (OperationsMatrix.verifyGoal(M, goal)):
                timeEnd = time.time()
                #Mostra o resultado
                result = Result("uniformCostSearch", timeBegin, timeEnd, len(frontier), OperationsMatrix.getSizeExplored(explored), len(nodes), nodes, index)
                result.printResultSearch()
                return
            
            #Marca o nó como explorado
            explored[OperationsMatrix.getPosition(M, 0)][OperationsMatrix.getPosition(M, 2)][OperationsMatrix.getPosition(M, 4)][OperationsMatrix.getPosition(M, 6)][OperationsMatrix.getPosition(M, 8)].append(index)
            
            #Explora cada filho gerado
            for children in OperationsMatrix.possibilityMoves(M, nodes[index].getRoot(), nodes):
                indexExplored = OperationsMatrix.verifyNodeIsExplored(children, explored, nodes)        #Verifica se o nó está entre os explorados
                indexFrontier = OperationsMatrix.verifyNodeIsFrontier(children, frontier, nodes)        #Verifica se o nó está na fronteira
                pos = OperationsMatrix.getPositionInsert(nodes, frontier, pathCost, 0)                  #Posição em que o nó deve ser inserido para inserir ordenado
                if (indexExplored < 0 and indexFrontier < 0):       #Se o nó não foi explorado e nem está na fronteira
                    #Adiciona nó na lista de nós
                    nodes.append(Node(index, children, pathCost, 0))
                    #Adiciona o índice do nó na fronteira
                    frontier.insert(pos, (len(nodes)-1))
                    #OperationsMatrix.printMatrix(children)
                elif (indexFrontier >= 0):                          #Se o nó não foi explorado mas já está na fronteira
                    #Atualiza aquele nó utilizando o novo pai e o novo custo => Isso porque foi identificado um novo caminho até ele com menor custo
                    idx = frontier[indexFrontier]
                    nodes[idx].setCost(pathCost)          #Atualiza o custo do nó
                    nodes[idx].setRoot(index)             #Atualiza o pai do nó
                    #Remove esse nó da fronteira e insere novamente com o custo atualizado
                    frontier.insert(pos, idx)
                    del frontier[indexFrontier]

            #Imprime a fronteira
            #countFrontier = 1
            #for index in frontier:
                #printText('Element frontier ' + str(countFrontier))
                #OperationsMatrix.printMatrix(nodes[index].getMatrix())
                #countFrontier = countFrontier+1
                
            pathCost = pathCost+1
            
    def depthSearch(M, limit, goal, timeBeginIDS):
        timeBegin = time.time()
        
        #Verifica se o nó atual é igual ao objetivo
        if (OperationsMatrix.verifyGoal(M, goal)):
            timeEnd = time.time()
            result = Result("iterativeDeepeningSearch", timeBegin, timeEnd, 0, 0, 0, [], -1)
            result.printResultSearch()
            return True
            
        #Inicializa a lista de nós como vazia
        nodes = []
        index = -1
        totalNodes = 0
        
        #Inicializa a fronteira
        frontier = []
        
        #Adiciona nó na lista de nós com profundidade zero
        nodes.append(Node(index, M, 0, 0))
        totalNodes = totalNodes+1
        #Insere na fronteira o primeiro nó (Nó inicial)
        frontier.append(0)
        
        #Inicializa a lista de nós explorados como vazia
        explored = OperationsMatrix.initializeExplored()
        
        #print(frontier)
        #countFrontier = 0
        #for index in frontier:
            #print('Element frontier ' + str(countFrontier), end='')
            #OperationsMatrix.printMatrix(nodes[index].getMatrix())
            #countFrontier = countFrontier+1
        
        #Loop => Enquanto a fronteira não estiver vazia
        while(len(frontier) > 0):                    
            #Atualiza nó => Seleciona o último elemento da fronteira
            index = frontier.pop()
            M = nodes[index].getMatrix()
            depth = nodes[index].getCost()
            
            #Marca o nó como explorado
            explored[OperationsMatrix.getPosition(M, 0)][OperationsMatrix.getPosition(M, 2)][OperationsMatrix.getPosition(M, 4)][OperationsMatrix.getPosition(M, 6)][OperationsMatrix.getPosition(M, 8)].append(index)
            
            #Verifica se o nó é igual a solução objetivo
            if (OperationsMatrix.verifyGoal(M, goal)):
                timeEnd = time.time()
                #Mostra o resultado
                printTextInline('Nodes: ' + str(len(nodes)) + ' - ' + str(totalNodes) + ' - ')
                #result = Result("iterativeDeepeningSearch", timeBegin, timeEnd, len(frontier), len(nodes)-len(frontier), totalNodes, nodes, index)
                result = Result("iterativeDeepeningSearch", timeBeginIDS, timeEnd, len(frontier), len(nodes)-len(frontier), totalNodes, nodes, index)
                result.printResultSearch()
                return True
                
            #printTextInline(M)
            #printTextInline(' ==> ')
            
            #Se a profundidade dos filhos for menor que o limite, podemos gerar mais filhos
            if (depth+1 <= limit):
                #Explora cada filho gerado
                for children in OperationsMatrix.possibilityMoves(M, nodes[index].getRoot(), nodes):
                    #Verifica se o nó está entre os explorados
                    indexExplored = OperationsMatrix.verifyNodeIsExplored(children, explored, nodes)
                    #Se já cheguei nesse nó antes e já explorei
                    if (indexExplored >= 0):
                        elementExplored = nodes[indexExplored]
                        #Verifico se já cheguei nesse nó com um custo maior. Se sim, insiro ele na fronteira
                        if ((elementExplored.getCost() + elementExplored.getCostH()) > depth+1):
                            totalNodes = totalNodes+1
                            #Atualizo o custo do nó
                            nodes[indexExplored].setCost(depth+1)
                            #Atualiza o pai do nó
                            nodes[indexExplored].setRoot(index)
                            #Adiciona o índice do nó na fronteira
                            frontier.append(indexExplored)
                            #print(children)   
                    
                    else:
                        #Verifica se o nó está na fronteira
                        indexFrontier = OperationsMatrix.verifyNodeIsFrontier(children, frontier, nodes)
                        #Se já cheguei nesse nó antes mas ele ainda não foi explorado, ou seja, ele está na fronteira
                        if (indexFrontier >= 0):
                            elementFrontier = nodes[indexFrontier]
                            #Verifico se já cheguei nesse nó com um custo maior. Se sim, insiro ele na fronteira
                            if ((elementFrontier.getCost() + elementFrontier.getCostH()) > depth+1):
                                totalNodes = totalNodes+1
                                #Atualizo o custo do nó
                                nodes[indexFrontier].setCost(depth+1)
                                #Atualiza o pai do nó
                                nodes[indexFrontier].setRoot(index)
                                #Adiciona o índice do nó na fronteira
                                frontier.append(indexFrontier)
                                #print(children)
                        
                        #Se esse nó não foi nem explorado e nem está na fronteira
                        else:
                            #Adiciona nó na lista de nós com profundidade = depth+1
                            nodes.append(Node(index, children, depth+1, 0))
                            totalNodes = totalNodes+1
                            #Adiciona o índice do nó na fronteira
                            frontier.append(len(nodes)-1)
                            #print(children)
                
            #printText('')
            #printText(str(len(frontier)) + ' === ' + str(OperationsMatrix.getSizeExplored(explored)))
            
            #Imprime a fronteira
            #print(frontier)
            #countFrontier = 0
            #for index in frontier:
                #print('Element frontier ' + str(countFrontier), end='')
                #OperationsMatrix.printMatrix(nodes[index].getMatrix())
                #countFrontier = countFrontier+1
        
        timeEnd = time.time()
        #Mostra o resultado
        printTextInline('Nodes: ' + str(len(nodes)) + ' - ' + str(totalNodes) + ' - ')
        #result = Result("iterativeDeepeningSearch", timeBegin, timeEnd, len(frontier), len(nodes)-len(frontier), totalNodes, nodes, index)
        #result.printResultSearch()
        
        return False

    def iterativeDeepeningSearch(M, maximum, goal):
        timeBegin = time.time()         #Começa a contar o tempo total da busca em profundidade
        
        printText('-------------------')
        depth = 1                       #Inicializa a profundidade como 1
        while depth <= maximum:         #Enquanto a profundidade for menor ou igual a profundidade máxima
            timeI = time.time()         #Começa a contar o tempo da busca na profundidade depth
            result = SearchWithoutInformation.depthSearch(M, depth, goal, timeBegin)      #Tenta encontrar o nó objetivo numa profundidade máxima 'depth'
            timeE = time.time()         #Termina de contar o tempo da busca na profundidade depth 
            printText('depth: ' + str(depth) + ' - time: ' + str(timeE - timeI))
            printText('-------------------')
            if (result == True):        #Se o resultado for verdadeiro, para
                break
            depth = depth+1             #Avança a profundidade
            
        timeEnd = time.time()           #Termina de contar o tempo total da busca em profundidade
        printText('Total time: ' + str(timeEnd - timeBegin) + ' s')

class SearchWithInformation:    
    def AStarSearch(M, goal, heurist):
        timeBegin = time.time()
        
        #Seta o custo real como zero
        pathCostG = 0
        #Define o custo heurístico com base na heurística selecionada => Heurística 1 ou 2
        pathCostH = OperationsMatrix.getHeuristCost(M, goal, heurist)
        
        #Inicializa a lista de nós como vazia
        nodes = []
        index = -1
        nodes.append(Node(index, M, pathCostG, pathCostH))
        
        #Inicializa a fronteira
        frontier = []
        #Insere na fronteira o primeiro nó (Nó inicial)
        frontier.append(0)
        #Inicializa a lista de nós explorados como vazia
        explored = OperationsMatrix.initializeExplored()
        
        #Loop => Enquanto a fronteira não estiver vazia
        while(len(frontier) != 0):
            #Atualiza nó => Seleciona o nó de menor custo (real + heuristico) da fronteira            
            index = frontier.pop(0)
            M = nodes[index].getMatrix()
            
            #Imprime a iteração
            #printText('G => ' + str(pathCostG) + ' - H => ' + str(pathCostH))
            #OperationsMatrix.printMatrix(M)
            
            #Verifica se o nó é igual a solução objetivo
            if (OperationsMatrix.verifyGoal(M, goal)):
                timeEnd = time.time()
                result = Result("AStarSearchH" + str(heurist), timeBegin, timeEnd, len(frontier), OperationsMatrix.getSizeExplored(explored), len(nodes), nodes, index)
                result.printResultSearch()
                return

            #Marca o nó como explorado (fechados)
            explored[OperationsMatrix.getPosition(M, 0)][OperationsMatrix.getPosition(M, 2)][OperationsMatrix.getPosition(M, 4)][OperationsMatrix.getPosition(M, 6)][OperationsMatrix.getPosition(M, 8)].append(index)
            
            #Explora cada filho gerado
            for children in OperationsMatrix.possibilityMoves(M, nodes[index].getRoot(), nodes):                
                #Se o nó não está entre os fechados
                if (OperationsMatrix.verifyNodeIsExplored(children, explored, nodes) < 0):
                    #Verifica se o nó está entre os abertos (fronteira)
                    indexFrontier = OperationsMatrix.verifyNodeIsFrontier(children, frontier, nodes)        #Verifica se o nó está na fronteira
                    
                    #Calcula o custo heurísitico
                    pathCostH = OperationsMatrix.getHeuristCost(M, goal, heurist)
                    
                    #Posição em que o nó deve ser inserido para inserir ordenado
                    pos = OperationsMatrix.getPositionInsert(nodes, frontier, pathCostG, pathCostH)

                    #Se o nó ainda não foi aberto
                    if (indexFrontier < 0):
                        #Adiciona nó na lista de nós
                        nodes.append(Node(index, children, pathCostG, pathCostH))
                        #Adiciona o índice do nó na fronteira (abertos)
                        frontier.insert(pos, (len(nodes)-1))
                        #OperationsMatrix.printMatrix(children)
                    
                    #Se o nó já foi aberto
                    else:
                        idx = frontier[indexFrontier]
                        #Se o custo real agora é menor que o custo real anterior, encontrei um caminho melhor
                        if (pathCostG < nodes[idx].getCost()):
                            #Atualiza o custo para se chegar nesse nó através do novo pai
                            nodes[idx].setCost(pathCostG)
                            #Atualiza o pai do nó
                            nodes[idx].setRoot(indexpathCostG)
                            #Remove esse nó da fronteira e insere novamente com o custo atualizado
                            frontier.insert(pos, idx)
                            del frontier[indexFrontier]
                        
            #Imprime a fronteira
            #countFrontier = 1
            #for index in frontier:
                #printText('Element frontier ' + str(countFrontier))
                #OperationsMatrix.printMatrix(nodes[index].getMatrix())
                #countFrontier = countFrontier+1
            
            #Toda vez que descer um ramo na árvore, avança o custo real
            pathCostG = pathCostG+1
    
    def greedyBestFirstSearch(M, goal, heurist):
        timeBegin = time.time()
        
        #Calcula o custo heurísitico
        pathCostH = OperationsMatrix.getHeuristCost(M, goal, heurist)
        
        #Inicializa a lista de nós como vazia
        nodes = []
        index = -1
        nodes.append(Node(index, M, 0, pathCostH))
        
        #Inicializa a fronteira
        frontier = []
        #Insere na fronteira o primeiro nó (Nó inicial)
        frontier.append(0)
        #Inicializa a lista de nós explorados como vazia
        explored = OperationsMatrix.initializeExplored()
        
        #Loop => Enquanto a fronteira não estiver vazia
        while(len(frontier) > 0):
            #printText('')
            
            #Atualiza nó => Seleciona o nó de menor custo (Apenas heurístico) da fronteira          
            minNode = OperationsMatrix.getIndexNodeMinCost(frontier, nodes)
            index = frontier[minNode]
            M = nodes[index].getMatrix()
            del frontier[minNode]
            
            #Verifica se o nó é igual a solução objetivo
            if (OperationsMatrix.verifyGoal(M, goal)):
                timeEnd = time.time()
                frontier.append(index)
                result = Result("greedyBestFirstSearchH" + str(heurist), timeBegin, timeEnd, len(frontier), OperationsMatrix.getSizeExplored(explored), len(nodes), nodes, index)
                result.printResultSearch()
                return
            
            #Marca o nó como explorado
            explored[OperationsMatrix.getPosition(M, 0)][OperationsMatrix.getPosition(M, 2)][OperationsMatrix.getPosition(M, 4)][OperationsMatrix.getPosition(M, 6)][OperationsMatrix.getPosition(M, 8)].append(index)
            
            #Fronteira só deve ter em cada iteração os filhos gerados
            frontier = []
            
            #Explora cada filho gerado
            for children in OperationsMatrix.possibilityMoves(M, nodes[index].getRoot(), nodes):
                #Calcula o custo heurísitico
                pathCostH = OperationsMatrix.getHeuristCost(children, goal, heurist)
                
                #Se o nó não foi explorado
                if (OperationsMatrix.verifyNodeIsExplored(children, explored, nodes) < 0):
                    #Adiciona nó na fronteira
                    nodes.append(Node(index, children, 0, pathCostH))
                    frontier.append(len(nodes)-1)
                    #OperationsMatrix.printMatrix(children)

            #Imprime a fronteira
            #printText(frontier)
            #countFrontier = 1
            #for index in frontier:
                #printText('Element frontier ' + str(countFrontier))
                #OperationsMatrix.printMatrix(nodes[index].getMatrix())
                #countFrontier = countFrontier+1
                
        timeEnd = time.time()
        result = Result("greedyBestFirstSearchH" + str(heurist), timeBegin, timeEnd, len(frontier), OperationsMatrix.getSizeExplored(explored), len(nodes), nodes, index)
        result.printResultSearch()

class LocalSearch:
    def hillclimbingSearch(M, goal, heurist):
        timeBegin = time.time()
        
        #Calcula o custo heurísitico
        pathCostH = OperationsMatrix.getHeuristCost(M, goal, heurist)
        
        #Inicializa a lista de nós como vazia
        nodes = []
        index = -1
        nodes.append(Node(index, M, 0, pathCostH))
        
        #Inicializa a fronteira
        frontier = []
        #Insere na fronteira o primeiro nó (Nó inicial)
        frontier.append(0)
        #Inicializa a lista de nós explorados como vazia
        explored = OperationsMatrix.initializeExplored()
        
        #Loop => Enquanto a fronteira não estiver vazia
        while(len(frontier) > 0):
            #printText('')
            
            #Inicializa as variáveis       
            minNode = 0
            index = 0
            M = []
            
            #Movimento lateral
            while(len(frontier) > 0):
                #Atualiza nó => Seleciona o nó de menor custo (Apenas heurístico) da fronteira          
                minNode = OperationsMatrix.getIndexNodeMinCost(frontier, nodes)
                index = frontier[minNode]
                M = nodes[index].getMatrix()
                del frontier[minNode]
                
                #Se o filho for pior que o pai, a busca para, ou seja, realiza um movimento lateral e continua
                indexRootNode = nodes[index].getRoot()                      #Pai do nó
                costNode = nodes[index].getCostH()                          #Custo do nó
                if (indexRootNode > 0):
                    costRootNode = nodes[indexRootNode].getCostH()          #Custo do pai do nó
                    #Se o filho for pior que o pai, a busca para e vai para o movimento lateral. Caso contrário, continua
                    if (costNode <= costRootNode):
                        break
            
            #Verifica se o nó é igual a solução objetivo
            if (OperationsMatrix.verifyGoal(M, goal)):
                timeEnd = time.time()
                frontier.append(index)
                result = Result("hillclimbingSearchH" + str(heurist), timeBegin, timeEnd, len(frontier), OperationsMatrix.getSizeExplored(explored), len(nodes), nodes, index)
                result.printResultSearch()
                return
                
            #Marca o nó como explorado
            explored[OperationsMatrix.getPosition(M, 0)][OperationsMatrix.getPosition(M, 2)][OperationsMatrix.getPosition(M, 4)][OperationsMatrix.getPosition(M, 6)][OperationsMatrix.getPosition(M, 8)].append(index)
                
            #Explora cada filho gerado
            for children in OperationsMatrix.possibilityMoves(M, nodes[index].getRoot(), nodes):
                #Calcula o custo heurísitico
                pathCostH = OperationsMatrix.getHeuristCost(children, goal, heurist)
                    
                #Se o nó não foi explorado
                if (OperationsMatrix.verifyNodeIsExplored(children, explored, nodes) < 0):
                    #Adiciona nó na fronteira
                    nodes.append(Node(index, children, 0, pathCostH))
                    frontier.append(len(nodes)-1)
                    #OperationsMatrix.printMatrix(children)

            #Imprime a fronteira
            #printText(frontier)
            #countFrontier = 1
            #for index in frontier:
                #printText('Element frontier ' + str(countFrontier))
                #OperationsMatrix.printMatrix(nodes[index].getMatrix())
                #countFrontier = countFrontier+1
                
        timeEnd = time.time()
        result = Result("hillclimbingSearchH" + str(heurist), timeBegin, timeEnd, len(frontier), OperationsMatrix.getSizeExplored(explored), len(nodes), nodes, index)
        result.printResultSearch()
    
class Tests:
    def runAllTests(initial, goal, maximum, algorithm):
        if (algorithm == 0 or algorithm == 1):
            printText('Initial matrix')
            OperationsMatrix.printMatrix(initial)
            printText('--------------------------------------------')
            printText('Goal matrix')
            OperationsMatrix.printMatrix(goal)
            printText('--------------------------------------------')
            printText('******* Search Without Information ********')
            printText('--------------------------------------------')
            printText('Breadth First Search:')
            SearchWithoutInformation.breadthFirstSearch(initial, goal)
            
        if (algorithm == 0 or algorithm == 2):
            printText('\n\n\n')
            printText('Initial matrix')
            OperationsMatrix.printMatrix(initial)
            printText('--------------------------------------------')
            printText('Goal matrix')
            OperationsMatrix.printMatrix(goal)
            printText('--------------------------------------------')
            printText('******* Search Without Information ********')
            printText('--------------------------------------------')
            printText('Uniform Cost Search:')
            SearchWithoutInformation.uniformCostSearch(initial, goal)
        
        if (algorithm == 0 or algorithm == 3):
            printText('\n\n\n')
            printText('Initial matrix')
            OperationsMatrix.printMatrix(initial)
            printText('--------------------------------------------')
            printText('Goal matrix')
            OperationsMatrix.printMatrix(goal)
            printText('--------------------------------------------')
            printText('******* Search Without Information ********')
            printText('--------------------------------------------')
            printText('Iterative Deepening Search:')
            SearchWithoutInformation.iterativeDeepeningSearch(initial, maximum, goal)
            
        if (algorithm == 0 or algorithm == 4):
            printText('\n\n\n')
            printText('Initial matrix')
            OperationsMatrix.printMatrix(initial)
            printText('--------------------------------------------')
            printText('Goal matrix')
            OperationsMatrix.printMatrix(goal)
            printText('--------------------------------------------')
            printText('********* Search With Information *********')
            printText('--------------------------------------------')
            printText('A Star Search Heuristic 1:')
            SearchWithInformation.AStarSearch(initial, goal, 1)
            
        if (algorithm == 0 or algorithm == 5):
            printText('\n\n\n')
            printText('Initial matrix')
            OperationsMatrix.printMatrix(initial)
            printText('--------------------------------------------')
            printText('Goal matrix')
            OperationsMatrix.printMatrix(goal)
            printText('--------------------------------------------')
            printText('********* Search With Information *********')
            printText('--------------------------------------------')
            printText('A Star Search Heuristic 2:')
            SearchWithInformation.AStarSearch(initial, goal, 2)
            
        if (algorithm == 0 or algorithm == 6):
            printText('\n\n\n')
            printText('Initial matrix')
            OperationsMatrix.printMatrix(initial)
            printText('--------------------------------------------')
            printText('Goal matrix')
            OperationsMatrix.printMatrix(goal)
            printText('--------------------------------------------')
            printText('********* Search With Information *********')
            printText('--------------------------------------------')
            printText('Greedy Best First Search Heuristic 1:')
            SearchWithInformation.greedyBestFirstSearch(initial, goal, 1)
            
        if (algorithm == 0 or algorithm == 7):
            printText('\n\n\n')
            printText('Initial matrix')
            OperationsMatrix.printMatrix(initial)
            printText('--------------------------------------------')
            printText('Goal matrix')
            OperationsMatrix.printMatrix(goal)
            printText('--------------------------------------------')
            printText('********* Search With Information *********')
            printText('--------------------------------------------')
            printText('Greedy Best First Search Heuristic 2:')
            SearchWithInformation.greedyBestFirstSearch(initial, goal, 2)
            
        if (algorithm == 0 or algorithm == 8):
            printText('\n\n\n')
            printText('Initial matrix')
            OperationsMatrix.printMatrix(initial)
            printText('--------------------------------------------')
            printText('Goal matrix')
            OperationsMatrix.printMatrix(goal)
            printText('--------------------------------------------')
            printText('*************** Local Search ***************')
            printText('--------------------------------------------')
            printText('Hill Climbing Search Heuristic 1:')
            LocalSearch.hillclimbingSearch(initial, goal, 1)
            
        if (algorithm == 0 or algorithm == 9):
            printText('\n\n\n')
            printText('Initial matrix')
            OperationsMatrix.printMatrix(initial)
            printText('--------------------------------------------')
            printText('Goal matrix')
            OperationsMatrix.printMatrix(goal)
            printText('--------------------------------------------')
            printText('*************** Local Search ***************')
            printText('--------------------------------------------')
            printText('Hill Climbing Search Heuristic 2:')
            LocalSearch.hillclimbingSearch(initial, goal, 2)
    
def main():   
    initial = LoadMatrix.load(sys.argv[3])
    goal = LoadMatrix.load(sys.argv[4])
    
    Tests.runAllTests(initial, goal, 1000, int(sys.argv[5]))

    closeFileTXT()
    closeFileCSV()

    
if __name__ == '__main__':
    main()
