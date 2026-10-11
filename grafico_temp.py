import numpy as np
import matplotlib.pyplot as plt

# Intervalo de temperatura (de perto de 0 até 3.0)
T = np.linspace(0.05, 3.0, 200)

# Pesos originais da regra MUSICA
w = np.array([0.60, 0.25, 0.15])

# Listas para armazenar as probabilidades calculadas
p1, p2, p3 = [], [], []

for t in T:
    # Aplica a fórmula do hiperparâmetro
    w_adj = w ** (1/t)
    # Normaliza para obter a probabilidade (soma = 1)
    p = w_adj / np.sum(w_adj)
    
    p1.append(p[0])
    p2.append(p[1])
    p3.append(p[2])

# Configuração do gráfico
plt.figure(figsize=(8, 5))
plt.plot(T, p1, label='Produção A (Peso = 0.60)', linewidth=2, color='#1f77b4')
plt.plot(T, p2, label='Produção B (Peso = 0.25)', linewidth=2, color='#ff7f0e')
plt.plot(T, p3, label='Produção C (Peso = 0.15)', linewidth=2, color='#2ca02c')

# Linha de referência para o estado original
plt.axvline(x=1.0, color='black', linestyle='--', alpha=0.5, label='T = 1.0 (Distribuição Original)')

plt.xlabel('Temperatura (T)', fontsize=12)
plt.ylabel('Probabilidade de Seleção', fontsize=12)
plt.title('Impacto do Hiperparâmetro de Temperatura', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Salva a imagem em alta resolução
plt.savefig('grafico_temperatura.png', dpi=300)
plt.show()