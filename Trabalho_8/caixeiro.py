from dis import dis

import xlrd
import random as rd
import math
import matplotlib.pyplot as plt
import PySimpleGUI as sg


grafico = plt.figure()
gDistancia = grafico.add_subplot()
vetorDist, vetorGeracao = [], []

arquivo = xlrd.open_workbook("Planilha_caixeiro_viajante.xls").sheet_by_index(0)

numGenes = arquivo.ncols - 1
#dis = 0
geracaoAtual = 0

dados = [   
    [sg.Text('Tamanho da População: ', size = (15,0)), sg.InputText(size = (10,1), key='tamanhoPopulacao')],
    [sg.Text('Taxa de Cruzamento: ', size = (15,0)), sg.InputText(size = (10,1), key='taxaCruzamento')],
    [sg.Text('Taxa de Mutação: ', size = (15,0)), sg.InputText(size = (10,1), key='taxaMutacao')],
    [sg.Text('Número de Gerações: ', size = (15,0)), sg.InputText(size = (10,1), key='qtdGeracoes')],
    [sg.Text('Tamanho do Elitismo: ', size = (15,0)), sg.InputText(size = (10,1), key='tamanhoElitismo')],
    [sg.Radio('Torneio', "select",size=(12,0), key='radioButton_Torneio', default=True),
         sg.InputText(key='torneio', size=(10,0))], 
    [sg.Radio('Roleta', "select",size=(15,0), key='radioButton_Roleta', default=False)],
    [sg.Button('Viajar', size=(15,0))],
    [sg.Text('Distância: ', size=(10,0)),sg.Text(f'{dis}', key='barrinha',size = (20,1))],
    [sg.Text('Geração: ', size=(10,0)),sg.Text(f'{geracaoAtual}', key='barrinha2',size = (20,1))]]

rotas = [
    [sg.Text('Rotas',size=(10,0))],
    [sg.Text('', size=(20,40), key='rotas')]]
            
layout = [[sg.Column(dados,size = (250,400)),sg.Column(rotas,size = (200,400))]]

# Realizar a criação da janela 
window = sg.Window('Caixeiro Viajante', layout)

# Função para alterar a posição das cidades no vetor filho
def organizarPopulacao(pop):
    populacaoNova = []
    for vetor in pop:
        populacaoNova.append(ordenarCidade(vetor))
    return populacaoNova

# Função para colocar a cidade de Uberaba na primeira posição
def ordenarCidade(vetor):
    indice = 0
    while indice < len(vetor):
        if(vetor[indice] == 1 and indice != 0):
            temporario = vetor[0]
            vetor[0] = vetor[indice]
            vetor[indice] = temporario
        indice += 1
    indice = 0
    while indice < len(vetor):
        if(vetor[indice] == 21 and indice != 0):
            temporario = vetor[len(vetor)-1]
            vetor[len(vetor)-1] = vetor[indice]
            vetor[indice] = temporario
        indice += 1
    return vetor

# Função para passar o tamanho da população e retornar
def genes(tamanhoPopulacao):
    pop = []
    for aux in range (tamanhoPopulacao):
        # criando individuo randomicamente
        temp = rd.sample(population = range(1, numGenes+1), k = numGenes)
        # reorganizando o vetor
        temp = ordenarCidade(temp)
        # adicionando na população
        pop.append(temp)

    return pop
    
def aptidao_individuos(qtdGeracoes, populacao):
    aptidao = []
    for aux2 in range (len(populacao)):
        aptidao.append(0)
        for aux3 in range(1,numGenes):
            aptidao[aux2] = float(aptidao[aux2]) + float(arquivo.cell_value(populacao[aux2][aux3 - 1], populacao[aux2][aux3]))
        aptidao[aux2] = float(aptidao[aux2]) + float(arquivo.cell_value(populacao[aux2][0], populacao[aux2][numGenes - 1]))
        aptidao[aux2] = 1/aptidao[aux2]
    
    # ordenando a lista de aptidão e populaçao pelo desempenho
    aptidao, populacao = zip(*sorted(zip(aptidao, populacao), reverse = True))
    return aptidao, populacao


def alg_genetico():

    # criando populacao
    populacao = genes(tamanhoPopulacao)
    
    # iniciando gerações
    for geracaoAtual in range(qtdGeracoes):
        # definindo aptidao
        aptidao, populacao = aptidao_individuos(qtdGeracoes, populacao)
                 
        filhos = []

        # verificando se o método escolhido foi o torneio
        if metodo == True:
            # escolhendo os mais aptos
            for indice in range(min(tamanhoElitismo, len(populacao))):
                filhos.append(populacao[indice])
                
            #Fazendo cruzamentos
            for b in range (math.floor(len(populacao)/2)):
                #Escolhendo pais para cruzamento
                progenitores = list(populacao)
                apt = list(aptidao)
                pais = []
                
                pai1 = rd.choices(progenitores, weights=apt, k = 1)[0]
                pai1 = ordenarCidade(pai1)
                pais.append(pai1)
                apt.pop(progenitores.index(pais[0]))
                progenitores.pop(progenitores.index(pais[0]))
                
                pai2 = rd.choices(progenitores, weights=apt, k = 1)[0]
                pai2 = ordenarCidade(pai2)
                pais.append(pai2)

                # crossing over
                if(rd.random() < taxaCruzamento):
                    corte = rd.randrange(numGenes)

                    filho = []
                    filho.append([])
                    filho.append([])

                    for indice in range(corte):
                        filho[0].append(pais[0][indice])
                        filho[1].append(pais[1][indice])
                    indice = 0

                    while(len(filho[0]) < numGenes):
                        if not(pais[1][indice] in filho[0]):
                            filho[0].append(pais[1][indice])
                        indice += 1

                    indice = 0
                    while(len(filho[1]) < numGenes):
                        if not(pais[0][indice] in filho[1]):
                            filho[1].append(pais[0][indice])
                        indice += 1

                    if(rd.random() < taxaMutacao):
                    
                        mutacao = rd.choices(filho[0], k = 2)
                        gene = filho[0].index(mutacao[0])
                        filho[0][filho[0].index(mutacao[1])] = mutacao[0]
                        filho[0][gene] = mutacao[1]

                    if(rd.random() < taxaMutacao):
                    
                        mutacao = rd.choices(filho[1], k = 2)
                        gene = filho[1].index(mutacao[0])
                        filho[1][filho[1].index(mutacao[1])] = mutacao[0]
                        filho[1][gene] = mutacao[1]
                    
                    filhos.append(filho[0])
                    filhos.append(filho[1])
            populacao = filhos
            populacao = organizarPopulacao(populacao)

        # metodo roleta
        else:
            for indice in range(min(tamanhoElitismo, len(populacao))):
                filhos.append(populacao[indice])

            #Fazendo cruzamentos
            for aux in range (math.floor(len(populacao)/2)):
                # gerando números para escolher os pais
                pais = []
                num1 = rd.random()
                num2 = rd.random()

                # pegando os pais
                # pai 1
                ind_pai1 = 0            
                while ind_pai1 < len(aptidao) and aptidao[ind_pai1] > num1:
                    ind_pai1 += 1
                
                if ind_pai1 == len(aptidao):
                    ind_pai1 -= 1
                
                if ind_pai1 != 0:
                    if aptidao[ind_pai1] - num1 > num1 - aptidao[ind_pai1-1]:
                        ind_pai1 = ind_pai1 - 1

                pais.append(populacao[ind_pai1])

                # pai 2
                ind_pai2 = 0            
                while ind_pai2 < len(aptidao) and aptidao[ind_pai2] > num2:
                    ind_pai2 += 1
                
                if ind_pai2 == len(aptidao):
                    ind_pai2 -= 1

                if ind_pai2 != 0:
                    if aptidao[ind_pai2] - num2 > num2 - aptidao[ind_pai2-1]:
                        ind_pai2 = ind_pai2 - 1

                pais.append(populacao[ind_pai2])
                
                # crossing over
                if(rd.random() < taxaCruzamento):
                    corte = rd.randrange(numGenes)

                    filho = []
                    filho.append([])
                    filho.append([])

                    for indice in range(corte):
                        filho[0].append(pais[0][indice])
                        filho[1].append(pais[1][indice])
                    indice = 0

                    while(len(filho[0]) < numGenes):
                        if not(pais[1][indice] in filho[0]):
                            filho[0].append(pais[1][indice])
                        indice += 1

                    indice = 0
                    while(len(filho[1]) < numGenes):
                        if not(pais[0][indice] in filho[1]):
                            filho[1].append(pais[0][indice])
                        indice += 1

                    # mutação
                    # filho 1                    
                    if(rd.random() < taxaMutacao):
                        # aplicando mutação
                        mutacao = rd.choices(filho[0], k = 2)
                        gene = filho[0].index(mutacao[0])
                        filho[0][filho[0].index(mutacao[1])] = mutacao[0]
                        filho[0][gene] = mutacao[1]

                    # filho 2
                    if(rd.random() < taxaMutacao):
                        # aplicando mutação
                        mutacao = rd.choices(filho[1], k = 2)
                        gene = filho[1].index(mutacao[0])
                        filho[1][filho[1].index(mutacao[1])] = mutacao[0]
                        filho[1][gene] = mutacao[1]
                    
                    filhos.append(filho[0])
                    filhos.append(filho[1])
            populacao = filhos
            populacao = organizarPopulacao(populacao)

        
        # Procurar o melhor indivíduo
        aptidao = []
        for b in range(len(populacao)):
            aptidao.append(0)
            for c in range(1, numGenes):
                aptidao[b] = float(aptidao[b]) + float(arquivo.cell_value(populacao[b][c - 1], populacao[b][c]))
            aptidao[b] = float(aptidao[b]) + float(arquivo.cell_value(populacao[b][0], populacao[b][numGenes - 1]))
            aptidao[b] = 1/aptidao[b]

        # Ordenar as cidades
        aptidao, populacao = zip(*sorted(zip(aptidao, populacao), reverse = True))
        vetorDist.append(1/aptidao[0])
        vetorGeracao.append(geracaoAtual)


        if(geracaoAtual == 0):
            plt.plot(vetorGeracao, vetorDist, label='Km')
        else:
            plt.plot(vetorGeracao, vetorDist)
        plt.xlabel('Gerações')
        plt.ylabel('Distância')
        plt.show()
        # plt.pause(0.03)

        texto = ''
        for a2 in populacao[0]:
            texto += arquivo.cell_value(0, a2)+' \n'

        window['barrinha'].Update(f'{1/aptidao[0]}')
        window['barrinha2'].Update(f'{geracaoAtual+1}')
        
        window['rotas'].Update(texto)
        window.refresh()  
        
        
    
    print("Menor caminho: ", 1/aptidao[0])
    
while True:
    event, values = window.read()
    if event == 'Viajar':
        # pegando dados dos inputs
        tamanhoPopulacao = int(values['tamanhoPopulacao'])
        taxaCruzamento = float(values['taxaCruzamento'])
        taxaMutacao = float(values['taxaMutacao'])
        qtdGeracoes = int(values['qtdGeracoes'])
        tamanhoElitismo = int(values['tamanhoElitismo'])
        if (values['radioButton_Torneio'] == True):
            metodo = True
        else:
            metodo = False
        vetorDist, vetorGeracao = [], []
        alg_genetico()
        
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

window.close()