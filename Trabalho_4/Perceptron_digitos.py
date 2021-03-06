"""
@author: João Paulo, João Pedro, Renato, Thiago

Algoritmo de Treinamento Rede Multilayer Perceptron

"""

import numpy as np
import random as rd
import matplotlib.pyplot as plt
import os

os.chdir(r'D:\IFTM\9-SEM\IA\Trabalhos\Trabalho_4\digitostreinamento')


# funcao para criar arquivos txt para matrizes treinadas
def criarTxt(nomeTxt: str, valorTxt: str):
    with open(f'Acerto_taxa_{nomeTxt}.txt', 'a') as arquivo:
        arquivo.write(f'{valorTxt}\n')

# amostras
ampdigitos = 50  # amostras por digitos
vsai = 10
amostras = ampdigitos * vsai  # quantidade de amostras
entradas = 256
neur = 30
limiar = 0.0
alfa = 0.012
errotolerado = 0.05  # taxa de aprendizagem
listaciclo = []
listaerro = []

# montando o arquivo de amostras de treinamento
x = np.zeros((amostras, entradas))
k2 = '_'
k4 = '.txt'
cont = 0
ordem = np.zeros(amostras)

for m in range(vsai):
    k1 = str(m)
    for n in range(ampdigitos):
        k3a = n + 1
        k3 = str(k3a)
        nome = k1 + k2 + k3 + k4
        entrada = np.loadtxt(nome)
        x[cont, :] = entrada[:]
        ordem[cont] = m
        cont += 1
ordem = ordem.astype('int')

# lendo o arquivo de saidas esperadas (target)
t = np.loadtxt('t.txt')

# gerando os pesos sinapticos aleatoriamente
vanterior = np.zeros((entradas, neur))
aleatorio = 0.2

for i in range(entradas):
    for j in range(neur):
        vanterior[i][j] = rd.uniform(-aleatorio, aleatorio)

v0anterior = np.zeros((1, neur))

for j in range(neur):
    v0anterior[0][j] = rd.uniform(-aleatorio, aleatorio)

wanterior = np.zeros((neur, vsai))
for i in range(neur):
    for j in range(vsai):
        wanterior[i][j] = rd.uniform(-aleatorio, aleatorio)

w0anterior = np.zeros((1, vsai))
for j in range(vsai):
    w0anterior[0][j] = rd.uniform(-aleatorio, aleatorio)

# matrizes de atualizacao de pesos e valores de saida da rede
vnovo = np.zeros((entradas, neur))
v0novo = np.zeros((1, neur))
wnovo = np.zeros((neur, vsai))
w0novo = np.zeros((1, vsai))
zin = np.zeros((1, neur))
z = np.zeros((1, neur))
deltinhak = np.zeros((vsai, 1))
deltaw0 = np.zeros((vsai, 1))
deltinha = np.zeros((1, neur))
xaux = np.zeros((1, entradas))
h = np.zeros((vsai, 1))
target = np.zeros((vsai, 1))
deltinha2 = np.zeros((neur, 1))
ciclo = 0
errototal = 100000

while errotolerado < errototal:
    errototal = 0
    for padrao in range(amostras):
        for j in range(neur):
            zin[0][j] = np.dot(x[padrao, :], vanterior[:, j]) + v0anterior[0][j]
        z = np.tanh(zin)
        yin = np.dot(z, wanterior) + w0anterior
        y = np.tanh(yin)

        for m in range(vsai):
            h[m][0] = y[0][m]
        for m in range(vsai):
            target[m][0] = t[m][ordem[padrao]]

        errototal = errototal + np.sum(0.5 * ((target - h) ** 2))

        # obter matrizes para a atualizacao dos pesos
        deltinhak = (target - h) * (1 + h) * (1 - h)
        deltaw = alfa * (np.dot(deltinhak, z))
        deltaw0 = alfa * deltinhak
        deltinhain = np.dot(np.transpose(deltinhak), np.transpose(wanterior))
        deltinha = deltinhain * (1 + z) * (1 - z)

        for m in range(neur):
            deltinha2[m][0] = deltinha[0][m]
        for k in range(entradas):
            xaux[0][k] = x[padrao][k]
        deltav = alfa * np.dot(deltinha2, xaux)
        deltav0 = alfa * deltinha

        # realizando as atualizacoes de pesos
        vnovo = vanterior + np.transpose(deltav)
        v0novo = v0anterior + np.transpose(deltav0)
        wnovo = wanterior + np.transpose(deltaw)
        w0novo = w0anterior + np.transpose(deltaw0)
        vanterior = vnovo
        v0anterior = v0novo
        wanterior = wnovo
        w0anterior = w0novo

    ciclo += 1
    listaciclo.append(ciclo)
    listaerro.append(errototal)
    print('Ciclo\t Erro')
    print(ciclo, '\t', errototal)
    criarTxt('v0novo', str(v0novo))
    criarTxt('vnovo', str(vnovo))
    criarTxt('w0novo', str(w0novo))
    criarTxt('wnovo', str(wnovo))

plt.plot(listaciclo, listaerro)
plt.xlabel('Ciclo')
plt.ylabel('Erro')
plt.show()

# Teste manual
# xteste = np.loadtxt('9_72.txt')
# for m2 in range(vsai):
#     for n2 in range(neur):
#         zin[0][n2] = np.dot(xteste, vanterior[:, n2])+v0anterior[0][n2]
#     z = np.tanh(zin)
#     yin = np.dot(z, wanterior)+w0anterior
#     y = np.tanh(yin)
# print(yin)
# for j in range(vsai):
#     if y[0][j] >= limiar:
#         y[0][j] = 1.0
#     else:
#         y[0][j] = -1.0
# print(y[0, :])

# Teste automatico da rede
aminicial = 20
amtestedigitos = 70
yteste = np.zeros((vsai, 1))
cont = 0
contcerto = 0
ordem = np.zeros(amostras)
for m in range(vsai):
    k1 = str(m)
    for n in range(amtestedigitos):
        k3a = n + aminicial
        k3 = str(k3a)
        nome = k1 + k2 + k3 + k4
        xteste = np.loadtxt(nome)
        for m2 in range(vsai):
            for n2 in range(neur):
                zin[0][n2] = np.dot(xteste, vanterior[:, n2]) + v0anterior[0][n2]

            z = np.tanh(zin)
            yin = np.dot(z, wanterior) + w0anterior
            y = np.tanh(yin)

        for j in range(vsai):
            if y[0][j] >= limiar:
                y[0][j] = 1.0
            else:
                y[0][j] = -1.0

        for j in range(vsai):
            yteste[j][0] = y[0][j]
        for j in range(vsai):
            target[j][0] = t[0][j]

        soma = np.sum(y - target)
        if soma == 0:
            contcerto += 1
        cont += 1
taxa = contcerto / cont * 100

print(taxa, '%')