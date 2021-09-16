# Form implementation generated from reading ui file 'interface2.ui'
# Created by: PyQt5 UI code generator 5.9.2
# WARNING! All changes made in this file will be lost!

#Autores: João Pedro Campos, João Paulo Alves, Renato Júnior

import os
import numpy as np
import random as rd
import matplotlib.pyplot as plt

from PyQt5 import QtCore, QtGui, QtWidgets

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
        v[i][j] = rd.uniform(-0.1, 0.1)

for i in range(numClasses):
    v0[i] = rd.uniform(-0.1, 0.1)

vetor1 = []
vetor2 = []

yin = np.zeros((numClasses, 1))
y = np.zeros((numClasses, 1))

erro = 10
ciclo = 0

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(554, 215)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 141, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(160, 20, 113, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(20, 60, 131, 20))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(20, 100, 121, 20))
        self.radioButton_2.setObjectName("radioButton_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(400, 20, 113, 22))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(290, 20, 101, 16))
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(310, 100, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(420, 100, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(160, 60, 113, 22))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(160, 100, 113, 22))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 180, 491, 16))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 554, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Taxa de aprendizagem:"))
        self.radioButton.setText(_translate("MainWindow", "Numero de ciclos:"))
        self.radioButton_2.setText(_translate("MainWindow", "Erro Tolerado"))
        self.label_2.setText(_translate("MainWindow", "Digito para teste:"))
        self.pushButton.setText(_translate("MainWindow", "Treinar"))
        self.pushButton.clicked.connect(self.treinar)
        self.pushButton_2.clicked.connect(self.verificar)
        self.pushButton_2.setText(_translate("MainWindow", "Testar digito"))
        self.label_3.setText(_translate("MainWindow", ""))

    def treinar(self):
        global erro
        global erroTolerado
        global ciclo
        global v
        global v0
        global vetor1
        global vetor2

        global alfa
        alfa = float(self.lineEdit.text())
        #print(alfa)

        if(self.radioButton.isChecked()):

            erroTolerado = int(self.lineEdit_3.text())
            #print("entrou no if")

            while ciclo <= erroTolerado:
                ciclo = ciclo + 1
                erro = 0
                #print("chegou aqui")
                for i in range(amostras):
                    xaux = x[i, :]
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
                            v[j][k] = vanterior[j][k] + alfa * (t[k][i] - y[k]) * xaux[j]

                    v0anterior = v0
                    for j in range(numClasses):
                        v0[j] = v0anterior[j] + alfa * (t[j][i] - y[j])

                print(f"ciclo: {ciclo}")

                vetor1.append(ciclo)
                vetor2.append(erro)
                plt.scatter(vetor1, vetor2, marker='*', color='blue')
                plt.xlabel('ciclo')
                plt.ylabel('erro')
                plt.show()

        else:
            erroTolerado = float(self.lineEdit_4.text())

            while erro > erroTolerado:
                ciclo = ciclo + 1
                erro = 0
                for i in range(amostras):
                    xaux = x[i, :]
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
                            v[j][k] = vanterior[j][k] + alfa * (t[k][i] - y[k]) * xaux[j]

                    v0anterior = v0
                    for j in range(numClasses):
                        v0[j] = v0anterior[j] + alfa * (t[j][i] - y[j])

                print(f"ciclo: {ciclo}")

                vetor1.append(ciclo)
                vetor2.append(erro)
                plt.scatter(vetor1, vetor2, marker='*', color='blue')
                plt.xlabel('ciclo')
                plt.ylabel('erro')
                plt.show()

    def verificar(self):
        global xteste
        global yin
        global y

        if(int(self.lineEdit_2.text()) == 0):
            xteste = x[29, :]
        else:
            xteste = x[int(self.lineEdit_2.text())*3-1, :]

        for i in range(numClasses):
            soma = 0
            for j in range(entradas):
                soma = soma + xteste[j] * v[j][i]
                yin[i] = soma + v0[i]
        print(yin)
        for i in range(numClasses):
            if yin[i] >= limiar:
                y[i] = 1.0
            else:
                y[i] = -1.0
        print(y)

        if(y[int(self.lineEdit_2.text())-1] == 1):
            self.label_3.setText("Numero reconhecido!")
        else:
            self.label_3.setText("Numero não reconhecido!")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

