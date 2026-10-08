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