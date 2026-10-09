import random
import math
import pretty_midi


gramatica_pop = {
    # macro
    'MUSICA': {
        'producoes': [
            ['INTRO', 'VERSO', 'REFRAO', 'VERSO', 'REFRAO', 'PONTE', 'REFRAO'], 
            ['VERSO', 'REFRAO', 'VERSO', 'REFRAO'],                             
            ['REFRAO', 'VERSO', 'REFRAO', 'PONTE', 'REFRAO']                    
        ],
        'pesos': [0.60, 0.25, 0.15]
    },
    
    # meso
    'VERSO': {
        'producoes': [
            ['ACORDES_LONGOS', 'MELODIA_ESPARSA'],
            ['ACORDES_PULSANTES', 'MELODIA_SINCOPADA']
        ],
        'pesos': [0.70, 0.30]
    },
    'REFRAO': {
        'producoes': [
            ['ACORDES_COMPASSADOS', 'MELODIA_ENERGICA'], 
            ['ACORDES_ARPEJADOS', 'MELODIA_ENERGICA']
        ],
        'pesos': [0.50, 0.50]
    }
    
    # micro
}

# mudança de hiperparâmetro
def aplicar_temperatura(pesos_originais, temperatura):
    if temperatura == 0:
        novos_pesos = [0.0] * len(pesos_originais)
        indice_maximo = pesos_originais.index(max(pesos_originais))
        novos_pesos[indice_maximo] = 1.0
        return novos_pesos
        
    return [peso ** (1.0 / temperatura) for peso in pesos_originais]

def sortear_producao(simbolo, regras, temperatura):
    if simbolo in regras:
        opcoes = regras[simbolo]['producoes']
        probabilidades = regras[simbolo]['pesos']
        
        pesos_ajustados = aplicar_temperatura(probabilidades, temperatura)
        escolha = random.choices(opcoes, weights=pesos_ajustados, k=1)[0]
        return escolha
    
    return [simbolo]

def expandir(simbolo, regras, temperatura):
    # se o símbolo for um terminal
    if simbolo not in regras:
        return [simbolo]
    
    # se for não-terminal, sorteia a produção usando a temperatura
    producao = sortear_producao(simbolo, regras, temperatura)
    
    # loop recursivo
    resultado_final = []
    for s in producao:
        resultado_final.extend(expandir(s, regras, temperatura))
        
    return resultado_final

# print(expandir('MUSICA', gramatica_pop, temperatura=1.0))