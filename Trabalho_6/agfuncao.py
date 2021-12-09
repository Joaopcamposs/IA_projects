import numpy as np
import random as rd
from matplotlib import cm
import matplotlib.pyplot as plt

def alg_genetico(tamCromossomo1, tamPopulacao1, pc1, pm1, numgeracoes1, elite1, selecao1, k1, cruzamento1):
    
    tamCromossomo = tamCromossomo1
    pc = pc1#prob de cruzamento
    pm = pm1#prob de mutacao
    numgeracoes = numgeracoes1
    tamPopulacao = tamPopulacao1
    k = k1# quantidade de genes selecionados para torneio
    elite = elite1#quantiadde de genes que serao passados para a proxima geracao
    selecao = bool(selecao1)
    cruzamento1pt = bool(cruzamento1)
    
    #parametros da funcao analisada
    infx = -3.1
    supx = 12.1
    infy = 4.1
    supy = 5.8
    
    #passo 1 - gerando os genes aleatoriamente
    p = genes(tamPopulacao, tamCromossomo)
    
    #passo 2 - criacao das variaveis do AG
    melhoraptidao = 0
    ind = np.zeros(tamCromossomo)
    individuo = np.zeros(tamPopulacao)
    individuo2 = np.zeros(tamPopulacao)
    Aptidao = np.zeros(tamPopulacao)
    novageracao = np.zeros((tamPopulacao, tamCromossomo))
    geracoes = 0
    

    
    #passo 3 - rodar a IA
    melhorgeracao, x, y, aptidaofinal = alg_ga(p, pm, pc, tamCromossomo, 
                                       tamPopulacao, geracoes, numgeracoes,
                                       ind, individuo, individuo2, Aptidao, novageracao,
                                       melhoraptidao, infx, infy, supx, supy, k, elite,
                                       selecao, cruzamento1pt)
    
    
    print('Melhor geracao: ', melhorgeracao)
    print('X: ', x)
    print('Y: ', y)
    return melhorgeracao, x, y, aptidaofinal

def genes(tamPopulacao, tamCromossomo):
    p = np.zeros((tamPopulacao, tamCromossomo))
    for i in range(tamPopulacao):
        for j in range(tamCromossomo):
            a = rd.uniform(0,1)
            if(a >= 0.5):
                p[i][j] = 1
            else:
                p[i][j] = 0
    return p

def valor_real(tamPopulacao, tamCromossomo, p, ind, infx, infy, supx, supy):
    individuo = np.zeros(tamPopulacao)
    individuo2 = np.zeros(tamPopulacao)
    tam = round(tamCromossomo/2) - 1
    for i in range(tamPopulacao):
        ind[:] = p[i,:]
        conv = 0
        conv2 = 0
        for j in range(tam):
            conv += ind[j]*(2**(tamCromossomo-(j+1)))
        individuo[i] = funcao_analisada(infx, supx, conv, tamCromossomo)
        
        conv2 = 0
        for j in range(tamCromossomo):
            conv2 += ind[j]*(2**(tamCromossomo-(j+1)))

        individuo2[i] = funcao_analisada(infy, supy, conv2, tamCromossomo)

        
    return individuo, individuo2

def funcao_analisada(inf, sup, ri, k):
    return inf+(((sup-inf)/((2**k)-1))*ri)

def funcao_maximizada(x, y):
    return (15 + (x*np.cos(2*np.pi*x)) + (y*np.cos(14*np.pi*y)))

def aptidao_individuos(tamPopulacao, individuo, individuo2):
    TotalAptidao = 0
    Aptidao = np.zeros(tamPopulacao)
    for i in range(tamPopulacao):
        Aptidao[i] = funcao_maximizada(individuo[i],individuo2[i])
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
    
def torneio(tamPopulacao, TotalAptidao, Aptidao, k):
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
    
def cruzamento(p, pc, tamPopulacao, tamCromossomo, pai1, pai2, novosindividuos, novageracao):
    if(pc > rd.uniform(0,1)):
        c  = round(1+(tamCromossomo-2)*rd.uniform(0,0.5))
        c2 = round(1+(tamCromossomo-2)*rd.uniform(0.5,1))
        
        tam = round(tamCromossomo/2)
        
        #gene 1
        gene11 = p[pai1][0:c]
        gene12 = p[pai1][c:tam]
        gene13 = p[pai1][tam:c2]
        gene14 = p[pai1][c2:tamCromossomo]
        
        #gene 2
        gene21 = p[pai1][0:c]
        gene22 = p[pai1][c:tam]
        gene23 = p[pai1][tam:c2]
        gene24 = p[pai1][c2:tamCromossomo]
        
        #juncao dos cromossomos permutados
        filho1 = np.concatenate((gene11,gene22, gene23, gene14))
        filho2 = np.concatenate((gene21, gene12, gene13, gene24))
        
        #geracao dos individuos
        novageracao[novosindividuos,:] = filho1
        novosindividuos += 1
        novageracao[novosindividuos,:] = filho2
        novosindividuos += 1
    return novosindividuos, novageracao


def cruzamento_2pts(p, pc, tamPopulacao, tamCromossomo, pai1, pai2, novosindividuos, novageracao):
    if(pc > rd.uniform(0,1)):
        
        tam = round(tamCromossomo/2)
        c1 = round((1+(tamCromossomo-2)*rd.uniform(0,0.5))/2)#primeiro corte em x
        c2 = round((1+(tamCromossomo-2)*rd.uniform(0.5,1))/2)#segundo corte em x
        c3 = round((1+(tamCromossomo-2)*rd.uniform(0,0.5))/2) + tam
        c4 = round((1+(tamCromossomo-2)*rd.uniform(0.5,1))/2) + tam

        gene11 = p[pai1][0:c1]#filho1
        gene12 = p[pai1][c1:c2]#filho2
        gene13 = p[pai1][c2:tam]#filho1
        gene14 = p[pai1][tam:c3]#filho2
        gene15 = p[pai1][c3:c4]#filho1
        gene16 = p[pai1][c4:tamCromossomo]#filho2
        
        
        gene21 = p[pai2][0:c1]#filho2
        gene22 = p[pai2][c1:c2]#filho1
        gene23 = p[pai2][c2:tam]#filho2
        gene24 = p[pai2][tam:c3]#filho1
        gene25 = p[pai2][c3:c4]#filho2
        gene26 = p[pai2][c4:tamCromossomo]#filho1
        
        #juncao dos cromossomos permutados
        filho1 = np.concatenate((gene11, gene22, gene13, gene24, gene15, gene26))
        filho2 = np.concatenate((gene21, gene12, gene23, gene14, gene25, gene16))
        
        #geracao dos individuos
        novageracao[novosindividuos,:] = filho1
        novosindividuos += 1
        novageracao[novosindividuos,:] = filho2
        novosindividuos += 1
    
    return novosindividuos, novageracao

def mutacao(pm, tamCromossomo, novageracao, novosindividuos):
    if(pm > rd.uniform(0,1)):
        d = round(1+(tamCromossomo-2)*rd.uniform(0,1))
        if(novageracao[novosindividuos-2][d] == 0):
            novageracao[novosindividuos-2][d] = 1
        else:
            novageracao[novosindividuos-2][d] = 0
        
        if(novageracao[novosindividuos-1][d] == 0):
            novageracao[novosindividuos-1][d] = 1
        else:
            novageracao[novosindividuos-1][d] = 0
    return novageracao

#passo 3 - iniciando o algoritmo genetico
def alg_ga(p, pm, pc, tamCromossomo, tamPopulacao, geracoes, numgeracoes, ind, individuo, individuo2, Aptidao, novageracao, melhoraptidao, infx, infy, supx, supy, k, elite, selecao, cruzamento1pt):
    
    while (geracoes <= numgeracoes):
        novosindividuos = 0
        while((novosindividuos+elite) < (tamPopulacao-1)):
            
            #transformacao de binario para real dos individuos
            #dividir em 2 vetores
            individuo, individuo2 = valor_real(tamPopulacao, tamCromossomo, p, ind, infx, infy, supx, supy)
            
            #aptidao dos individuos  
            Aptidao, TotalAptidao = aptidao_individuos(tamPopulacao, individuo, individuo2)   
            
            #selecao dos individuos
            if(selecao):
                pai1, pai2 = torneio(tamPopulacao, TotalAptidao, Aptidao, k)    
            else:
                pai1, pai2 = roleta(tamPopulacao, TotalAptidao, Aptidao)    

            #operacoes de cruzamento
            if(cruzamento1pt):
                novosindividuos, novageracao = cruzamento(p, pc, tamPopulacao, tamCromossomo, pai1, pai2, novosindividuos, novageracao)    
            else:
                novosindividuos, novageracao = cruzamento_2pts(p, pc, tamPopulacao, tamCromossomo, pai1, pai2, novosindividuos, novageracao)
            
            
            #operacao mutacao
            novageracao = mutacao(pm, tamCromossomo, novageracao, novosindividuos)
            
        novosindividuos, novageracao = elitismo(p, tamPopulacao, Aptidao, elite, novageracao,novosindividuos)            
        
        indice = Aptidao.argmax()
        elem = individuo[indice]
        # elem2 = individuo2[indice]
        aptidao_final = Aptidao[indice]
        # conta = funcao_maximizada(elem, elem2)
        # print(geracoes,'\t' ,elem, '\t', elem2, '\t', conta)
        if(geracoes > 0):
            if(elem > melhoraptidao):
                melhoraptidao = elem
                melhorx = individuo[indice]
                melhory = individuo2[indice]
                melhorgeracao = geracoes
                
        else:
            melhoraptidao = elem
            melhorx = individuo[indice]
            melhory = individuo2[indice]
            melhorgeracao = 0

        p = novageracao
        geracoes += 1

    fig = plt.figure(figsize=plt.figaspect(0.5))
    ax = fig.add_subplot(111, projection="3d")
    x = np.arange(-3.1, 12.1, 0.1)
    y = np.arange(4.1, 5.8, 0.1)
    X, Y = np.meshgrid(x, y)
    ax.scatter(individuo,individuo2,aptidao_final, c='red')
    Z = 15 + X * np.cos(2 * np.pi * X) + Y * np.cos(14 * np.pi * Y)
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                        linewidth=0, antialiased=False)
    ax.view_init(elev=10., azim=35.)
    ax.set_zlim(0, 30)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.show()
        
    return melhorgeracao, melhorx, melhory, aptidao_final
    
if __name__ == '__main__':
    alg_genetico()
