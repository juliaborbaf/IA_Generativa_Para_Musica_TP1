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
    'INTRO': {
        'producoes': [['PUSH_T', 'ACORDES_LONGOS', 'POP_T', 'MELODIA_PAUSA']],
        'pesos': [1.0]
    },
    'PONTE': {
        'producoes': [['PUSH_T', 'ACORDES_LONGOS', 'POP_T', 'MELODIA_ESPARSA']],
        'pesos': [1.0]
    },
    
    # meso
    'VERSO': {
        'producoes': [
            ['PUSH_T', 'ACORDES_LONGOS', 'POP_T', 'MELODIA_ESPARSA'],
            ['PUSH_T', 'ACORDES_PULSANTES', 'POP_T', 'MELODIA_SINCOPADA']
        ],
        'pesos': [0.70, 0.30]
    },
    'REFRAO': {
        'producoes': [
            ['PUSH_T', 'ACORDES_COMPASSADOS', 'POP_T', 'MELODIA_ENERGICA'], 
            ['PUSH_T', 'ACORDES_LONGOS', 'POP_T', 'MELODIA_ENERGICA']
        ],
        'pesos': [0.50, 0.50]
    },

    # micro
    'ACORDES_LONGOS': {
        'producoes': [['!CHORD_C_4.0', '!CHORD_G_4.0', '!CHORD_Am_4.0', '!CHORD_F_4.0']], 'pesos': [1.0]
    },
    'ACORDES_PULSANTES': {
        'producoes': [['!CHORD_C_2.0', '!CHORD_C_2.0', '!CHORD_G_2.0', '!CHORD_G_2.0', '!CHORD_Am_2.0', '!CHORD_Am_2.0', '!CHORD_F_2.0', '!CHORD_F_2.0']], 'pesos': [1.0]
    },
    'ACORDES_COMPASSADOS': {
        'producoes': [['!CHORD_C_4.0', '!CHORD_G_4.0', '!CHORD_Am_4.0', '!CHORD_F_4.0']], 'pesos': [1.0]
    },
    
    'MELODIA_PAUSA': {
        'producoes': [['!NOTE_0_16.0']], 'pesos': [1.0] # silêncio 16 tempos
    },
    'MELODIA_ESPARSA': {
        'producoes': [['!NOTE_60_2.0', '!NOTE_0_2.0', '!NOTE_62_2.0', '!NOTE_0_2.0', '!NOTE_64_2.0', '!NOTE_0_2.0', '!NOTE_65_2.0', '!NOTE_0_2.0']], 'pesos': [1.0]
    },
    'MELODIA_SINCOPADA': {
        'producoes': [['!NOTE_0_1.0', '!NOTE_60_1.0', '!NOTE_60_2.0', '!NOTE_0_1.0', '!NOTE_62_1.0', '!NOTE_62_2.0', '!NOTE_0_1.0', '!NOTE_64_1.0', '!NOTE_64_2.0', '!NOTE_0_1.0', '!NOTE_65_1.0', '!NOTE_65_2.0']], 'pesos': [1.0]
    },
    'MELODIA_ENERGICA': {
        'producoes': [['!NOTE_67_1.0', '!NOTE_67_1.0', '!NOTE_64_2.0', '!NOTE_62_1.0', '!NOTE_62_1.0', '!NOTE_59_2.0', '!NOTE_69_1.0', '!NOTE_69_1.0', '!NOTE_64_2.0', '!NOTE_65_1.0', '!NOTE_65_1.0', '!NOTE_60_2.0']], 'pesos': [1.0]
    }
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