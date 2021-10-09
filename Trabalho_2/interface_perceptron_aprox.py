# Autores: João Pedro Campos, João Paulo Alves, Renato Júnior, Thiago Lopes
# Created by: PyQt5 UI code generator 5.9.2

import numpy as np
import random as rd
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(576, 228)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineMin = QtWidgets.QLineEdit(self.centralwidget)
        self.lineMin.setGeometry(QtCore.QRect(130, 10, 113, 22))
        self.lineMin.setObjectName("lineMin")
        self.lineMax = QtWidgets.QLineEdit(self.centralwidget)
        self.lineMax.setGeometry(QtCore.QRect(130, 50, 113, 22))
        self.lineMax.setObjectName("lineMax")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 111, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 111, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(330, 10, 101, 16))
        self.label_3.setObjectName("label_3")
        self.lineAmostras = QtWidgets.QLineEdit(self.centralwidget)
        self.lineAmostras.setGeometry(QtCore.QRect(430, 10, 111, 22))
        self.lineAmostras.setObjectName("lineAmostras")
        self.btnTreinar = QtWidgets.QPushButton(self.centralwidget)
        self.btnTreinar.setGeometry(QtCore.QRect(430, 50, 111, 28))
        self.btnTreinar.setObjectName("btnTreinar")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 110, 241, 16))
        self.label_4.setObjectName("label_4")
        self.label_neuronios = QtWidgets.QLabel(self.centralwidget)
        self.label_neuronios.setGeometry(QtCore.QRect(260, 110, 55, 16))
        self.label_neuronios.setObjectName("label_neuronios")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(380, 110, 141, 16))
        self.label_5.setObjectName("label_5")
        self.label_aprendizagem = QtWidgets.QLabel(self.centralwidget)
        self.label_aprendizagem.setGeometry(QtCore.QRect(520, 110, 55, 16))
        self.label_aprendizagem.setObjectName("label_aprendizagem")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 576, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Perceptron Aproximação de Funções"))
        self.label.setText(_translate("MainWindow", "Valor Mínimo de x:"))
        self.label_2.setText(_translate("MainWindow", "Valor Máximo de x:"))
        self.label_3.setText(_translate("MainWindow", "Nº de amostras:"))
        self.btnTreinar.setText(_translate("MainWindow", "Treinar"))
        self.btnTreinar.clicked.connect(self.treinar)
        self.label_4.setText(_translate("MainWindow", "Nº de neurônios da camada intermediária:"))
        self.label_neuronios.setText(_translate("MainWindow", ""))
        self.label_5.setText(_translate("MainWindow", "Taxa de aprendizagem:"))
        self.label_aprendizagem.setText(_translate("MainWindow", ""))

    def treinar(self):
        entradas = 1
        neur = 100
        self.label_neuronios.setText(str(neur))
        alfa = 0.5
        self.label_aprendizagem.setText(str(alfa))
        errotolerado = 0.05
        listaciclo = []
        listaerro = []
        xmin = int(self.lineMin.text())
        xmax = int(self.lineMax.text())
        npontos = int(self.lineAmostras.text())

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
        #print(amostras)

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
        global vnovo, v0novo, wnovo, w0novo, z, deltinhak, deltaw0, deltinha

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

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

