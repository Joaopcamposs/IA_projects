import numpy as np
import random as rd
import matplotlib.pyplot as plt

entradas = 1
neur = 200
alfa = 0.005
errotolerado = 0.05
listaciclo = []
listaerro = []
xmin = -1
xmax = 1
npontos = 50

# Gerando o arquivo de entradas
x1 = np.linspace(xmin, xmax, npontos)
x = np.zeros((npontos, 1))
for i in range(npontos):
    x[i][0] = x1[i]
(amostras, vsai) = np.shape(x)

t1 = (np.cos(x)) * (np.cos(2 * x))
t = np.zeros((1, amostras))
for i in range(amostras):
    t[0][i] = t1[i]
(vsai, amostras) = np.shape(t)

# Gerando os pesos sinapticos aleatoriamente
vanterior = np.zeros((entradas, neur))
aleatorio = 1
for i in range(entradas):
    for j in range(neur):
        vanterior[i][j] = rd.uniform(-aleatorio, aleatorio)
v0anterior = np.zeros((1, neur))
for j in range(neur):
    v0anterior[0][j] = rd.uniform(-aleatorio, aleatorio)

wanterior = np.zeros((neur, vsai))
aleatorio = 0.2
for i in range(neur):
    for j in range(vsai):
        wanterior[i][j] = rd.uniform(-aleatorio, aleatorio)
w0anterior = np.zeros((1, vsai))
for j in range(vsai):
    w0anterior[0][j] = rd.uniform(-aleatorio, aleatorio)

# Matrizes de atualizacao de pesos e valores de saida da rede
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
            target[m][0] = t[0][padrao]

        errototal = errototal + np.sum(0.5 * ((target - h) ** 2))

        # Obter matrizes para atualizacao dos pesos
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

        # Realizando as atualizacoes de pesos
        vnovo = vanterior + np.transpose(deltav)
        v0novo = v0anterior + np.transpose(deltav0)
        wnovo = wanterior + np.transpose(deltaw)
        w0novo = w0anterior + np.transpose(deltaw0)
        vanterior = vnovo
        v0anterior = v0novo
        wanterior = wnovo
        w0anterior = w0novo
    ciclo = ciclo + 1
    listaciclo.append(ciclo)
    listaerro.append(errototal)
    print('Ciclo\t Erro')
    print(ciclo, '\t', errototal)

    zin2 = np.zeros((1, neur))
    z2 = np.zeros((1, neur))
    t2 = np.zeros((amostras, 1))
    for i in range(amostras):
        for j in range(neur):
            zin2[0][j] = np.dot(x[i, :], vanterior[:, j]) + v0anterior[0][j]
            z2 = np.tanh(zin2)
        yin2 = np.dot(z2, wanterior) + w0anterior
        y2 = np.tanh(yin2)
        t2[i][0] = y2

    plt.plot(x, t1, color='red')
    plt.plot(x, t2, color='blue')
    plt.show()