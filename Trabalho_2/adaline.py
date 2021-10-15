import os
import numpy as np
import random as rd
import matplotlib.pyplot as plt

os.chdir(r'D:\IFTM\9-SEM\IA\Trabalhos\Trabalho_1')
x = np.loadtxt('x.txt')
(amostras, entradas) = np.shape(x)

t = np.loadtxt('t.txt')
(numClasses, targets) = np.shape(t)
limiar = 0.0
alfa = 0.01
erroTolerado = 0.01
v = np.zeros((entradas, numClasses))
v0 = np.zeros((numClasses, 1))

for i in range(entradas):
    for j in range(numClasses):
        v[i][j] = rd.uniform(-0.1,0.1)
    
for i in range(numClasses):
    v0[i] = rd.uniform(-0.1,0.1)

vetor1 = []
vetor2 = []

yin = np.zeros((numClasses,1))
y = np.zeros((numClasses, 1))

erro = 10
ciclo = 0

while erro > erroTolerado:
    ciclo = ciclo+1
    erro = 0
    for i in range(amostras):
        xaux = x[i,:]
        for j in range(numClasses):
            soma = 0
            for k in range(entradas):
                soma = soma + xaux[k] * v[k][j]
            yin[j] = soma + v0[j]

        for j in range(numClasses):
            if yin[j] >= limiar:
                y[j] = 1.0
            else:
                y[j] = -1.0
        
        for j in range(numClasses):
            erro = erro + 0.5 * ((t[j][i] - y[j]) ** 2)
        vanterior = v

        for j in range(entradas):
            for k in range(numClasses):
                v[j][k] = vanterior[j][k] + alfa * (t[k][i] - y[k]) *xaux[j]
        
        v0anterior = v0
        for j in range(numClasses):
            v0[j] = v0anterior[j] + alfa * (t[j][i] - y[j])

    print(ciclo)
    
    vetor1.append(ciclo)
    vetor2.append(erro)
    plt.scatter(vetor1, vetor2, marker='*', color='blue')
    plt.xlabel('ciclo')
    plt.ylabel('erro')
    plt.show()

xteste = x[7,:]
for i in range(numClasses):
    soma = 0
    for j in range(entradas):
        soma = soma + xteste[j] *v[j][i]
        yin[i] = soma +v0[i]
print(yin)
for i in range(numClasses):
    if yin[i] >= limiar:
        y[i] = 1.0
    else:
        y[i] = -1.0
print(y)