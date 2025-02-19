from math import log

#Sistema de progrssão de faixa com base no número de aulas feitas na faix atual
ordem_faixas = {'Branca':0, 'Azul':1, 'Roxa':2, 'Marrom':3, 'Preta':4}

#Cálculo do número mínimo de aulas necessárias para progredir em uma faixa
def calc_min_aulas_por_faixa(n:int):
    d = 1.47
    k = 30 / log(d)
    return (round(k * log(n + d)))