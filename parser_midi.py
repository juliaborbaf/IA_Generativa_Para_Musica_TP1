import pretty_midi

def gerar_midi(lista_eventos, nome_arquivo="musica_gerada.mid", bpm=120):
    midi_obj = pretty_midi.PrettyMIDI()

    # instrumentos
    # program 0 = acoustic grand piano
    # 80 = synth square
    inst_acordes = pretty_midi.Instrument(program=0)
    inst_melodia = pretty_midi.Instrument(program=80)
    
    cursor_tempo = 0.0
    pilha_tempo = []

    fator_tempo = 60.0 / bpm

    # dicionário de acordes
    dicionario_acordes = {
        'C': [48, 52, 55],    # Dó Maior
        'G': [43, 47, 50],    # Sol Maior
        'Am': [45, 48, 52],   # Lá Menor
        'F': [41, 45, 48]     # Fá Maior
    }
    

    for evento in lista_eventos:
        # PUSH_T salva o tempo atual
        if evento == 'PUSH_T':
            pilha_tempo.append(cursor_tempo)
            
        # POP_T volta o tempo pro último valor salvo
        elif evento == 'POP_T':
            cursor_tempo = pilha_tempo.pop()
            
        # !NOTE cria a nota na melodia
        elif evento.startswith('!NOTE'):
            _, pitch_str, duracao_str = evento.split('_')
            pitch = int(pitch_str)
            duracao = float(duracao_str) * fator_tempo
            
            # se não for pausa, adiciona a nota
            if pitch > 0:
                nota = pretty_midi.Note(
                    velocity=100, 
                    pitch=pitch, 
                    start=cursor_tempo, 
                    end=cursor_tempo + duracao
                )
                inst_melodia.notes.append(nota)
                
            # cursor sempre avança mesmo se for pausa
            cursor_tempo += duracao
            
        # !CHORD cria o acorde na base
        elif evento.startswith('!CHORD'):
            _, cifra, duracao_str = evento.split('_')
            duracao = float(duracao_str) * fator_tempo
            
            notas_acorde = dicionario_acordes[cifra]
            
            # adiciona cada nota do acorde separadamente
            for pitch_acorde in notas_acorde:
                nota = pretty_midi.Note(
                    velocity=80, 
                    pitch=pitch_acorde, 
                    start=cursor_tempo, 
                    end=cursor_tempo + duracao
                )
                inst_acordes.notes.append(nota)
                
            # cursor avança só uma vez pela duração do acorde inteiro
            cursor_tempo += duracao

    midi_obj.instruments.append(inst_acordes)
    midi_obj.instruments.append(inst_melodia)
    midi_obj.write(nome_arquivo)
    print(f"Arquivo {nome_arquivo} gerado com sucesso!")