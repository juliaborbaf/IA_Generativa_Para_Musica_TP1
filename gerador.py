import random
import math
import pretty_midi
from parser_midi import gerar_midi

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
        'producoes': [
            # I-V-vi-IV
            ['!CHORD_C_4.0', '!CHORD_G_4.0', '!CHORD_Am_4.0', '!CHORD_F_4.0'],
            # vi-IV-I-V
            ['!CHORD_Am_4.0', '!CHORD_F_4.0', '!CHORD_C_4.0', '!CHORD_G_4.0'],
            # I-IV-vi-V
            ['!CHORD_C_4.0', '!CHORD_F_4.0', '!CHORD_Am_4.0', '!CHORD_G_4.0']
        ], 
        'pesos': [0.4, 0.3, 0.3]
    },
    
    'ACORDES_PULSANTES': {
        'producoes': [
            # clássica pulsante
            ['!CHORD_C_2.0', '!CHORD_C_2.0', '!CHORD_G_2.0', '!CHORD_G_2.0', '!CHORD_Am_2.0', '!CHORD_Am_2.0', '!CHORD_F_2.0', '!CHORD_F_2.0'],
            # melancólica pulsante
            ['!CHORD_Am_2.0', '!CHORD_Am_2.0', '!CHORD_F_2.0', '!CHORD_F_2.0', '!CHORD_C_2.0', '!CHORD_C_2.0', '!CHORD_G_2.0', '!CHORD_G_2.0'],
            # animada pulsante
            ['!CHORD_C_2.0', '!CHORD_C_2.0', '!CHORD_F_2.0', '!CHORD_F_2.0', '!CHORD_Am_2.0', '!CHORD_Am_2.0', '!CHORD_G_2.0', '!CHORD_G_2.0']
        ], 
        'pesos': [0.4, 0.3, 0.3]
    },
    
    'ACORDES_COMPASSADOS': {
        'producoes': [
            # IV-I-V-vi
            ['!CHORD_F_4.0', '!CHORD_C_4.0', '!CHORD_G_4.0', '!CHORD_Am_4.0'],
            # clássica
            ['!CHORD_C_4.0', '!CHORD_G_4.0', '!CHORD_Am_4.0', '!CHORD_F_4.0'],
            # tensão
            ['!CHORD_Am_4.0', '!CHORD_G_4.0', '!CHORD_F_4.0', '!CHORD_F_4.0']
        ], 
        'pesos': [0.4, 0.3, 0.3]
    },
    
    'MELODIA_PAUSA': {
        'producoes': [['!NOTE_0_16.0']], 'pesos': [1.0] # silêncio 16 tempos
    },

    'MELODIA_ESPARSA': {
        'producoes': [
            # 1. Original: Subida gradual
            ['!NOTE_60_2.0', '!NOTE_0_2.0', '!NOTE_62_2.0', '!NOTE_0_2.0', '!NOTE_64_2.0', '!NOTE_0_2.0', '!NOTE_65_2.0', '!NOTE_0_2.0'],
            # 2. Focada nas notas fundamentais de cada acorde (Sol, Ré, Dó, Lá)
            ['!NOTE_67_2.0', '!NOTE_0_2.0', '!NOTE_62_2.0', '!NOTE_0_2.0', '!NOTE_60_2.0', '!NOTE_0_2.0', '!NOTE_69_2.0', '!NOTE_0_2.0'],
            # 3. Resposta invertida: a pausa vem antes da nota
            ['!NOTE_0_2.0', '!NOTE_64_2.0', '!NOTE_0_2.0', '!NOTE_67_2.0', '!NOTE_0_2.0', '!NOTE_69_2.0', '!NOTE_0_2.0', '!NOTE_60_2.0']
        ], 
        'pesos': [0.4, 0.3, 0.3]
    },
    
    'MELODIA_SINCOPADA': {
        'producoes': [
            # 1. Original: Contratempo clássico (pausa, curta, longa)
            ['!NOTE_0_1.0', '!NOTE_60_1.0', '!NOTE_60_2.0', '!NOTE_0_1.0', '!NOTE_62_1.0', '!NOTE_62_2.0', '!NOTE_0_1.0', '!NOTE_64_1.0', '!NOTE_64_2.0', '!NOTE_0_1.0', '!NOTE_65_1.0', '!NOTE_65_2.0'],
            # 2. Saltos curtos no contratempo apoiados na pentatônica
            ['!NOTE_0_1.0', '!NOTE_64_1.0', '!NOTE_67_2.0', '!NOTE_0_1.0', '!NOTE_67_1.0', '!NOTE_62_2.0', '!NOTE_0_1.0', '!NOTE_69_1.0', '!NOTE_64_2.0', '!NOTE_0_1.0', '!NOTE_60_1.0', '!NOTE_69_2.0'],
            # 3. Síncope invertida (longa, pausa, curta)
            ['!NOTE_67_2.0', '!NOTE_0_1.0', '!NOTE_64_1.0', '!NOTE_62_2.0', '!NOTE_0_1.0', '!NOTE_67_1.0', '!NOTE_64_2.0', '!NOTE_0_1.0', '!NOTE_69_1.0', '!NOTE_60_2.0', '!NOTE_0_1.0', '!NOTE_60_1.0']
        ], 
        'pesos': [0.4, 0.3, 0.3]
    },
    
    'MELODIA_ENERGICA': {
        'producoes': [
            # 1. Original: Motivo denso
            ['!NOTE_67_1.0', '!NOTE_67_1.0', '!NOTE_64_2.0', '!NOTE_62_1.0', '!NOTE_62_1.0', '!NOTE_59_2.0', '!NOTE_69_1.0', '!NOTE_69_1.0', '!NOTE_64_2.0', '!NOTE_65_1.0', '!NOTE_65_1.0', '!NOTE_60_2.0'],
            # 2. Movimento contínuo em semínimas (sem pausas e sem notas longas)
            ['!NOTE_60_1.0', '!NOTE_64_1.0', '!NOTE_67_1.0', '!NOTE_64_1.0', '!NOTE_62_1.0', '!NOTE_67_1.0', '!NOTE_69_1.0', '!NOTE_67_1.0', '!NOTE_69_1.0', '!NOTE_64_1.0', '!NOTE_60_1.0', '!NOTE_64_1.0', '!NOTE_69_1.0', '!NOTE_60_1.0', '!NOTE_64_1.0', '!NOTE_60_1.0'],
            # 3. Repetição pop (curta, curta, longa com intervalos limpos)
            ['!NOTE_64_1.0', '!NOTE_64_1.0', '!NOTE_60_2.0', '!NOTE_62_1.0', '!NOTE_62_1.0', '!NOTE_67_2.0', '!NOTE_69_1.0', '!NOTE_69_1.0', '!NOTE_64_2.0', '!NOTE_60_1.0', '!NOTE_60_1.0', '!NOTE_69_2.0']
        ], 
        'pesos': [0.4, 0.3, 0.3]
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


if __name__ == "__main__":
    configuracoes = {
        "musica_1_generica.mid": 0.1,  
        "musica_2_padrao.mid": 1.0,    
        "musica_3_experimental.mid": 2.5 
    }

    for nome_arquivo, temp in configuracoes.items():
        print(f"Gerando {nome_arquivo} com Temperatura {temp}")
        # gera lista de terminais
        lista_final = expandir('MUSICA', gramatica_pop, temperatura=temp)

        # print(lista_final[:30])
        
        # envia a lista de terminais pro parser
        gerar_midi(lista_final, nome_arquivo)