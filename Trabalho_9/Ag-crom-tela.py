# -*- coding: utf-8 -*-

import AGcromreal as ag

import PySimpleGUI as sg

class Tela:
    def __init__(self):
        layout = [

                [sg.Text('Tamanho população:', size=(15,0)), sg.Input(key='tamPop',size=(10,0))],
                [sg.Text('Probabilidade de cruzamento:', size=(15,0)), sg.Input(key='probCr',size=(10,0))],
                [sg.Text('Probabilidade de mutação', size=(15,0)), sg.Input(key='probMut',size=(10,0))],
                [sg.Text('Quantidade de gerações', size=(15,0)), sg.Input(key='tamGer',size=(10,0))],
                [sg.Text('Elitismo', size=(15,0)), sg.Input(key='elite',size=(10,0))],
                [sg.Radio('Torneio', "select",size=(12,0), key='radio_torneio', default=True),
                     sg.InputText(key='torneio', size=(10,0))], 
                [sg.Radio('Roleta', "select",size=(15,0), key='radio_roleta', default=False)],               
                [sg.Radio('Radcliff', "cruza",size=(15,0), key='radio_cruz1', default=True)], 
                [sg.Radio('Wright', "cruza",size=(15,0), key='radio_cruz2',default=False)],
                [sg.Button('Calcular', size=(15,0))],
                [sg.Text('Geração: '), sg.Text(key='geracao', size=(10,0))],
                [sg.Text('X: '), sg.Text(key='melhorx', size=(10,0))],
                [sg.Text('Y: '),sg.Text(key='melhory', size=(10,0))],
                [sg.Text('f(x,y)=  '),sg.Text(key='aptidao', size=(10,0))],
            ]
        self.window = sg.Window("Algoritmo genético").layout(layout)
        
    def display(self):
        while True:
            self.button, self.values= self.window.Read()  
          
            if self.button == sg.WIN_CLOSED:
               break
             
            if self.button == 'Calcular':
                
                tamPopulacao = int(self.values['tamPop'])
                pc = float(self.values['probCr'])
                pm = float(self.values['probMut'])
                numgeracoes = int(self.values['tamGer'])
                elite = int(self.values['elite'])
                if(self.values['radio_torneio'] == True):
                    selecao = 1
                    if(self.values['torneio'] == ''):
                        k = int(0)
                    else: 
                        k = int(self.values['torneio'])
                else:
                    selecao = 0
                    k = int(0)
                    
                if(self.values['radio_cruz1'] == True):
                    cruzamento = 1
                else:
                    cruzamento = 0
                
                geracaofinal, x, y, aptidaofinal = ag.alg_genetico(tamPopulacao, pc, pm, numgeracoes, elite, selecao, k, cruzamento)
                self.window.FindElement("geracao").Update(value=geracaofinal)
                self.window.FindElement("melhorx").Update(value=x)
                self.window.FindElement("melhory").Update(value=y)
                self.window.FindElement("aptidao").Update(value=aptidaofinal)
            
        
if __name__ == '__main__':        
    tela = Tela()
    tela.display()