import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl

# Variaveis do problema
comida = ctrl.Antecedent(np.arange(0, 11, 1),'comida')
servico = ctrl.Antecedent(np.arange(0, 11, 1),'servico')
gorjeta = ctrl.Consequent(np.arange(0, 26, 1),'gorjeta')

# Usando a funcao de pertinencia padrao (triangulo)
comida.automf(names=['pessima', 'razoavel','deliciosa'])

# Funcoes de pertinencia usando tipos variados
servico['ruim'] = fuzzy.trimf(servico.universe, [0, 0 , 5])
servico['aceitavel'] = fuzzy.gaussmf(servico.universe, 5, 2)
servico['excelente'] = fuzzy.gaussmf(servico.universe, 10, 3)

gorjeta['baixa'] = fuzzy.trimf(gorjeta.universe, [0, 0 , 13])
gorjeta['media'] = fuzzy.trapmf(gorjeta.universe, [0, 13, 15, 25])
gorjeta['alta'] = fuzzy.trimf(gorjeta.universe, [15, 25, 25])

comida.view()
servico.view()
gorjeta.view()

# Criando as regras
rule1 = ctrl.Rule(servico['excelente'] | comida['deliciosa'], gorjeta['alta'])
rule2 = ctrl.Rule(servico['aceitavel'], gorjeta['media'])
rule3 = ctrl.Rule(servico['ruim'] & comida['pessima'], gorjeta['baixa'])

gorjeta_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
gorjeta_simulador = ctrl.ControlSystemSimulation(gorjeta_ctrl)

# Entrando com alguns valores para qualidade da comida e do servico
gorjeta_simulador.input['comida'] = 3.5
gorjeta_simulador.input['servico'] = 9.4

# Computando os resultados
gorjeta_simulador.compute()
print(gorjeta_simulador.output['gorjeta'])

comida.view(sin=gorjeta_simulador)
servico.view(sin=gorjeta_simulador)
gorjeta.view(sin=gorjeta_simulador)