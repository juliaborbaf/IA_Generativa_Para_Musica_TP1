# TP1 - Composição Musical Algorítmica

Esse repositório contém a implementação de um gerador estocástico de música pop baseado em Gramáticas Generativas Não-Determinísticas, desenvolvido como Trabalho Prático 1 da disciplina de IA Generativa Para Música.

O sistema utiliza uma arquitetura de Pilha de Tempo para garantir o paralelismo entre a base harmônica e a melodia, operando sobre a escala pentatônica de Dó Maior com transposição dinâmica (offset) para as 12 tonalidades ocidentais. A entropia da geração é controlada por um hiperparâmetro de temperatura.

## Dependências

As bibliotecas necessárias para executar o motor de expansão e gerar os gráficos de análise estão listadas no arquivo `requirements.txt`.
* `pretty_midi`: Processamento e geração dos arquivos de áudio MIDI.
* `matplotlib`: Geração dos gráficos de distribuição de probabilidade (Temperatura).

## Instruções de Instalação

1. Clone este repositório para a sua máquina:
```bash
git clone [https://github.com/juliaborbaf/IA_Generativa_Para_Musica_TP1.git](https://github.com/juliaborbaf/IA_Generativa_Para_Musica_TP1.git)
cd IA_Generativa_Para_Musica_TP1
```

2. Crie e ative um ambiente virtual (recomendado):
```bash
python -m venv venv
# No Linux/macOS:
source venv/bin/activate
# No Windows:
venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Reprodução dos Resultados

Para gerar as músicas e reproduzir os resultados, execute o script principal:
```bash
python gerador.py
```
Para gerar e visualizar o gráfico que demonstra o impacto da temperatura nas probabilidades de seleção, execute o script do gráfico:
```bash
python grafico_temperatura.py
```
