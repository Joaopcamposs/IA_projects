import os
import numpy as np
#print("\x1b[2J\x1b[1;1H")

#path = rf'{os.path.dirname(os.path.realpath(__file__))}\tarefa_enviada'
#print(path)

# Lendo o arquivo de saídas esperadas (target)
t=np.loadtxt('t.txt')

vanterior=np.loadtxt('vnovo.csv', delimiter=',')
v0anterior=np.loadtxt('v0novo.csv', delimiter=',')
wanterior=np.loadtxt('wnovo.csv', delimiter=',')
w0anterior=np.loadtxt('w0novo.csv', delimiter=',')


(vent,neur)=np.shape(vanterior)
(vsai,numclasses)=np.shape(t)
limiar=0
zin=np.zeros((1,neur))
target=np.zeros((vsai,1))

#os.chdir(r'D:\IFTM\9-SEM\IA\Trabalhos\Trabalho_4\digitostreinamento')

###################### Limiarização

#### Teste da rede
aminicial=1
amtestedigitos=90
yteste=np.zeros((vsai,1))
k2='_'
k4='.txt'
cont=0
contcerto=0
#ordem=np.zeros(amostras)
for m in range(10):   
    k1=str(m)   
    for n in range(amtestedigitos):      
        k3a=n+aminicial
        k3=str(k3a)
        nome=k1+k2+k3+k4
        # print(nome)
        xteste=np.loadtxt(nome)
        for m2 in range(vsai):
            for n2 in range(neur):
                zin[0][n2]=np.dot(xteste,vanterior[:,n2])+v0anterior[n2][0]
            z=np.tanh(zin)
            yin=np.dot(z,wanterior)+w0anterior
            y=np.tanh(yin)
        for j in range(vsai):
            if yin[0][j]>=limiar:
                y[0][j]=1.0
            else:
                y[0][j]=-1.0
        for j in range(vsai):
            yteste[j][0]=y[0][j]
        
        for j in range(vsai):
            target[j][0]=t[j][m]
        soma=np.sum(y-target)
        if soma==0:
            contcerto=contcerto+1
        cont=cont+1
taxa=contcerto/cont
print(taxa)        
