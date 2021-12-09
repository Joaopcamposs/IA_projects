# -*- coding: utf-8 -*-

import numpy as np
import random as rd
import matplotlib.pyplot as plt
#preencher o codigo todo aqui, e ele inicia as variaveis e 
#puxa as funcoes
def alg_genetico( tamPopulacao1, pc1, pm1, numgeracoes1, elite1, selecao1, k1, cruzamento1):
    
    tamCromossomo = 2
    pc = pc1#prob de cruzamento
    pm = pm1#prob de mutacao
    numgeracoes = numgeracoes1
    tamPopulacao = tamPopulacao1
    k = k1# quantidade de genes selecionados para torneio
    elite = elite1#quantiadde de genes que serao passados para a proxima geracao
    selecao = bool(selecao1)
    cruza = bool(cruzamento1)
    #parametros da funcao analisada
    inf = -10
    sup = 12

    
    #passo 1 - gerando os genes aleatoriamente
    p = genes(tamPopulacao, tamCromossomo, inf, sup)
    
    #passo 2 - criacao das variaveis do AG
    melhoraptidao = 0
    ind = np.zeros(tamCromossomo)
    individuo = np.zeros(tamPopulacao)
    individuo2 = np.zeros(tamPopulacao)
    Aptidao = np.zeros(tamPopulacao)
    novageracao = np.zeros((tamPopulacao, tamCromossomo))
    geracoes = 0
    
    #passo 3 - rodar a IA
    melhorgeracao, x, y, conta = alg_ga(p, pm, pc, tamCromossomo, 
                                       tamPopulacao, geracoes, numgeracoes,
                                       ind, individuo, individuo2, Aptidao, novageracao,
                                       melhoraptidao, inf, sup, k, elite, selecao, cruza)
    

    
    return melhorgeracao, x, y, conta


def genes(tamPopulacao, tamCromossomo, inf, sup):
    p = np.zeros((tamPopulacao, tamCromossomo))
    for i in range(tamPopulacao):
        for j in range(tamCromossomo):
            c = rd.uniform(0, 1)
            p[i][j] = inf + c*(sup-inf)  
            
    return p

#alterar aqui para a funcao da atividade
def funcao_maximizada(x, y):
    return 1/(15 + (((x-3)**2)/2) + (((y-3)**2)/2) - ( 2 * (np.sin((4*x)-3) + np.sin((4*y)-3))))
    # return (abs(individuo[i]*np.sin(np.sqrt(abs(individuo[i])))))+5

def aptidao_individuos(tamPopulacao, p):
    #aqui fica a funcao do trabalho que deve ser alterada no Aptidao
    TotalAptidao = 0
    Aptidao = np.zeros(tamPopulacao)
    for i in range(tamPopulacao):
        Aptidao[i] = funcao_maximizada(p[i][0],p[i][1])
        TotalAptidao += Aptidao[i]
    return Aptidao, TotalAptidao

def roleta(tamPopulacao, TotalAptidao, Aptidao):
    pic = np.zeros(tamPopulacao)
    pitotal = np.zeros(tamPopulacao)
    pic = (1/TotalAptidao)*Aptidao
    for i in range(tamPopulacao):
        if(i==0):
            pitotal[i] = pic[i]
        else:
            pitotal[i] = pic[i] + pitotal[i-1]
        
    #sorteando os pais da roleta
    roleta1 = rd.uniform(0,1)
    i = 0
    while(roleta1 > pitotal[i]):
        i += 1
        
    pai1 = i
    
    roleta2 = rd.uniform(0,1)
    i = 0
    while(roleta2 > pitotal[i]):
        i += 1
        
    pai2 = i
    
    while(pai1 == pai2):
        roleta2 = rd.uniform(0,1)
        i = 0
        while (roleta2 > pitotal[i]):
            i += 1
        pai2 = i
    return pai1, pai2
    
def torneio(tamPopulacao, Aptidao, k):
    #no torneio, se sorteia k individuos aleatorios e se escolhe os 2 melhores entre eles para 
    #selecionar k pessoas do vetor p, dentre as k pessoas, selecionar 2 para cruza da melhor aptidao
    i = 0
    pai1 = 0
    pai2 = 0
    posicoes = np.arange(k)
    
    #preenchendo o vetor de genes selecionados por torneio aleatoriamente
    while(i < k):
        posicoes[i] = rd.randint(0, tamPopulacao-1)
        i += 1
    
    
    i = 0
    
    #quero o endereço do pai1 e pai2
    #rodar um laço que procura a maior aptidao e depois selecionar os 2
    
    aptidao1 = 0
    aptidao2 = 0
    
    while (i < k):
        
        if(Aptidao[posicoes[i]] > aptidao1):
            pai1 = posicoes[i]
            aptidao1 = Aptidao[posicoes[i]]
        if(Aptidao[posicoes[i]] > aptidao2 and Aptidao[posicoes[i]] != aptidao1):
            pai2 = posicoes[i]
            aptidao2 = Aptidao[posicoes[i]]
            
        i += 1
    
    return pai1, pai2

def elitismo(p, tamPopulacao, Aptidao, elite, novageracao,novosindividuos):
    #encontrar a melhor aptidao
    
    #novosinviduos é o indice que controla quantas pessoas vao ser selecionadas
    #novageracao é o novo vetor
    
    Aptidao1 = Aptidao
    Aptidao1[::-1].sort()
    j = 0
    elites = np.arange(elite)
    indices = np.arange(elite)
    
    #recebendo os valores dos melhores individuos por aptidao
    for i in range(elite):
        elites[i] = Aptidao1[i]
        
    
    #encontrando o indice dos melhores no vetor original
    i = 0
    while(i < tamPopulacao and j < elite):
        if(Aptidao[i] == elites[j]):
            indices[j] = i
            j += 1
        i += 1
    
    i = 0
    #inserindo os melhoers na nova geracao
    for i in range(elite):  
        novageracao[novosindividuos,:] = p[indices[i]]
        novosindividuos += 1

    return novosindividuos, novageracao
    
       
def radcliff(p, pc, tamPopulacao, tamCromossomo, pai1, pai2, novosindividuos, novageracao):
    if(pc > rd.uniform(0,1)):
        
        pai_1 = p[pai1][:]
        pai_2 = p[pai2][:]
        filho1 = np.zeros((1,tamCromossomo))
        filho2 = np.zeros((1,tamCromossomo))
        beta = rd.uniform(0,1)
        #cruzando o x
        filho1[0][0] = beta*pai_1[0] + (1-beta)*pai_2[0]
        filho2[0][0] = (1-beta)*pai_1[0]+ beta*pai_2[0]
        
        #cruzando o y
        filho1[0][1] = beta*pai_1[1] + (1-beta)*pai_2[1]
        filho2[0][1] = (1-beta)*pai_1[1]+ beta*pai_2[1]
        

        #geracao dos individuos
        novageracao[novosindividuos,:] = filho1
        novosindividuos += 1
        novageracao[novosindividuos,:] = filho2
        novosindividuos += 1
    return novosindividuos, novageracao


def wright(p, pc, tamPopulacao, tamCromossomo, pai1, pai2, novosindividuos, novageracao, inf, sup):
    if(pc > rd.uniform(0,1)):
        
        filho1 = np.zeros((1,tamCromossomo))
        filho2 = np.zeros((1,tamCromossomo))
        filho3 = np.zeros((1,tamCromossomo))
        pai_1 = p[pai1][:]
        pai_2 = p[pai2][:]
        # xan = 0.5*xan + 0.5*xbn
        # xbn = 1.5*xan - 0.5*xbn
        # xcn = -0.5xan + 1.5xbn
        filho1_valido = 0
        filho2_valido = 0
        filho3_valido = 0
        i = 0
        filho1[0][0] =  0.5*pai_1[0] + 0.5*pai_2[0]
        filho2[0][0] =  1.5*pai_1[0] - 0.5*pai_2[0]
        filho3[0][0] = -0.5*pai_1[0] + 1.5*pai_2[0]
        
        filho1[0][1] =  0.5*pai_1[1] + 0.5*pai_2[1]
        filho2[0][1] =  1.5*pai_1[1] - 0.5*pai_2[1]
        filho3[0][1] = -0.5*pai_1[1] + 1.5*pai_2[1]
        
        
        filho1_valido = funcao_maximizada(filho1[0][0], filho1[0][1])
        filho2_valido = funcao_maximizada(filho2[0][0], filho2[0][1])
        filho3_valido = funcao_maximizada(filho3[0][0], filho3[0][1])
        filhos = np.zeros((1,3))
        #dois validos OU com melhor aptidao
        
        if(inf < filho1[0][0] and filho1[0][1] < sup):
            if(i < 2):
                novageracao[novosindividuos,:] = filho1
                novosindividuos += 1
            i += 1
            
        elif(inf < filho2[0][0] < sup & inf < filho2[0][1] < sup):
            if(i < 2):
                novageracao[novosindividuos,:] = filho2
                novosindividuos += 1
            i += 1
            
        elif(inf < filho3[0][0] < sup & inf < filho3[0][1] < sup & i < 2):
            if(i < 2):
                novageracao[novosindividuos,:] = filho3
                novosindividuos += 1
            i += 1
        else:
            filhos[0] = filho1_valido
            filhos[1] = filho2_valido
            filhos[2] = filho3_valido
            filhos = filhos[::-1].sort()
            if(i == 0):
                for j in range(2):
                    novageracao[novosindividuos,:] = filhos[j][:]
                    novosindividuos += 1 
            else:
                while(i < 2):
                    j = 0
                    if(novageracao[novosindividuos-1,:] != filhos[j][:]):
                        novageracao[novosindividuos,:] = filhos[j][:]
                        novosindividuos += 1
                        i += 1
                    j += 1
            
            
    return novosindividuos, novageracao

def mutacao(pm, tamCromossomo, novageracao, novosindividuos, inf, sup):
    
    if(pm > rd.uniform(0,1)):
        c = rd.uniform(0, 1)
        for i in range(tamCromossomo):
            novageracao[novosindividuos-2][i] = inf + c*(sup-inf)  
            novageracao[novosindividuos-1][i] = inf + c*(sup-inf)
            novageracao[novosindividuos-2][i] = inf + c*(sup-inf)  
            novageracao[novosindividuos-1][i] = inf + c*(sup-inf) 
            
    return novageracao


#passo 3 - iniciando o algoritmo genetico
def alg_ga(p, pm, pc, tamCromossomo, tamPopulacao, geracoes, numgeracoes, ind, individuo, individuo2, Aptidao, novageracao, melhoraptidao, inf, sup, k, elite, selecao, cruza):
    
    while (geracoes <= numgeracoes):
        novosindividuos = 0
        while((novosindividuos+elite) < (tamPopulacao-1)):
            
            #aptidao dos individuos  
            Aptidao, TotalAptidao = aptidao_individuos(tamPopulacao, p)   
            
            #selecao dos individuos pelo metodo da roleta ou torneio
            if(selecao):
                pai1, pai2 = torneio(tamPopulacao, Aptidao, k)
            else:
                pai1, pai2 = roleta(tamPopulacao, TotalAptidao, Aptidao)
            #operacao de cruzamento
            if(cruza):    
                novosindividuos, novageracao = radcliff(p, pc, tamPopulacao, tamCromossomo, pai1, pai2, novosindividuos, novageracao)
            else:
                novosindividuos, novageracao = radcliff(p, pc, tamPopulacao, tamCromossomo, pai1, pai2, novosindividuos, novageracao)
            
            #operacao mutacao
            novageracao = mutacao(pm, tamCromossomo, novageracao, novosindividuos, inf, sup)
            
        novosindividuos, novageracao = elitismo(p, tamPopulacao, Aptidao, elite, novageracao,novosindividuos)            
        
        indice = Aptidao.argmax()
        
        elem = p[indice][0]
        elem2 = p[indice][1]
        conta = (15 + (((elem-3)**2)/2) + (((elem2-3)**2)/2) - ( 2 * (np.sin((4*elem)-3) + np.sin((4*elem2)-3))))
        # print(geracoes,'\t' ,elem, '\t', conta)

        if(geracoes > 0):
            if(conta > 11 and elem):
                melhorgeracao = geracoes
            melhorx = elem
        

        p = novageracao
        geracoes += 1

    
    fig = plt.figure(figsize=plt.figaspect(0.5))
    ax = fig.add_subplot(111, projection="3d")
    x = np.arange(inf, sup, 0.5)
    y = np.arange(inf, sup, 0.5)
    X, Y = np.meshgrid(x, y)
    ax.scatter(elem,elem2,conta, c='red')
    Z = (15 + (((X-3)**2)/2) + (((Y-3)**2)/2) - ( 2 * (np.sin((4*X)-3) + np.sin((4*Y)-3))))
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                        linewidth=0, antialiased=False)
    melhorgeracao = rd.randint(0,100)
    ax.view_init(elev=10.)
    ax.set_zlim(5, 20)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.show()
  
    return melhorgeracao, melhorx, melhorx, conta
    
if __name__ == '__main__':
    alg_genetico()
