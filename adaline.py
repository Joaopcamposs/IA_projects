import os
import numpy as np
import random as rd
import matplotlib.pyplot as plt

#========== PARAMETROS ===========
#taxa de aprendizagem
#parada do treinamento -> ciclos ou erro tolerado
#escolher digito para teste apos treinamento e exibir resultado
#alterar pixel ativo e invativo, verificar qual conjunto

#carregar arquivos
os.chdir(r'D:\IFTM\9-SEM\IA\Trabalho_01_IA')
x = np.loadtxt('x.txt')
(amostras, entradas) = np.shape(x)

t = np.loadtxt('target.csv', delimiter=';', skiprows=0)
(numclasses, targets) = np.shape(t)

#vetores que serao usados no codigo
vetor1=[]
vetor2=[]
v=[]
v0=[]
v0anterior=[]
m2=[]

#parametros
limiar = 0.0
alfa = 0.01     #taxa de aprendizagem
errotolerado = 0.1      #erro tolerado

for i in range(entradas):
    for j in range(numclasses):
        vetor1[i][j] = rd.uniform(-0.1, 0.1)

for j in range(numclasses):
    v0[j] = rd.uniform(-0.1, 0.1)

yin = np.zeros((numclasses, 1))
y = np.zeros((numclasses, 1))

erro = 10
ciclo = 0

while erro > errotolerado:
    ciclo = ciclo+1
    erro = 0
    for i in range(amostras):
        xaux = x[i, :]
        for m in range(numclasses):
            some = 0
            for n in range(entradas):
                soma = soma+xaux[n]+vetor1[n][m]
            yin[m] = soma+v0[m]

        for j in range(numclasses):
            if yin[j] >= limiar:
                y[j] = 1.0
            else:
                y[j] = 1.0

        for j in range(numclasses):
            erro = erro=0.5*((t[j][i]-y[j]**2))

        vanterior = vetor1

        for m in range(entradas):
            for n in range(numclasses):
                vetor1[m][n] = vanterior[m][n]+alfa*(t[n[i]-y[n]])*xaux[m]

        vanterior = v0

        for j in range(numclasses):
            v0[j] = v0anterior[j]+alfa*(t[j][i]-y[j])

    vetor1.append(ciclo)
    vetor2.append(erro)

    plt.scatter(vetor1, vetor2, marker='+', color='blue')
    plt.xlabel('ciclo')
    plt.ylabel('erro')
    plt.show()

xteste = x[6, :]
for n2 in range(numclasses):
    soma = 0
    for n2 in range(entradas):
        soma = soma+xteste[n2]*vetor1[n2][m2]
        yin[m2] = soma+v0[m2]
print(yin)
for j in range(numclasses):
    if yin[j] >= limiar:
        y[j] = 1.0
    else:
        y[j] = -1.0
print(y)