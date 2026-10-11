import matplotlib.pyplot as plt
import numpy as np

# Ativa o estilo de cores recomendado pelo ISMIR
plt.style.use('tableau-colorblind10')

# Simulando uma regra com 3 opções (pesos originais: 60%, 30%, 10%)
pesos_originais = np.array([0.6, 0.3, 0.1])
temperaturas = np.linspace(0.1, 3.0, 100)

probabilidades_hist = []

for t in temperaturas:
    # Aplica a equação da temperatura: w'_i = w_i^(1/T)
    pesos_ajustados = pesos_originais ** (1.0 / t)
    # Normaliza para que a soma dê 100%
    probabilidades = pesos_ajustados / np.sum(pesos_ajustados)
    probabilidades_hist.append(probabilidades)

probabilidades_hist = np.array(probabilidades_hist)

# Criando a figura
plt.figure(figsize=(7, 4))
plt.plot(temperaturas, probabilidades_hist[:, 0], label='Opção A (Original: 60%)', linewidth=2.5)
plt.plot(temperaturas, probabilidades_hist[:, 1], label='Opção B (Original: 30%)', linewidth=2.5)
plt.plot(temperaturas, probabilidades_hist[:, 2], label='Opção C (Original: 10%)', linewidth=2.5)

# Linha vertical marcando a Temperatura 1.0 (Comportamento normal)
plt.axvline(x=1.0, color='gray', linestyle='--', alpha=0.7, label='T = 1.0 (Padrão)')

plt.title('Efeito da Temperatura na Probabilidade das Regras', fontsize=12, pad=10)
plt.xlabel('Temperatura (T)', fontsize=10)
plt.ylabel('Probabilidade de Seleção', fontsize=10)
plt.legend(loc='upper right')
plt.grid(True, alpha=0.3)
plt.xlim(0.1, 3.0)
plt.ylim(0, 1.05)

# Salva a imagem em alta resolução
plt.tight_layout()
plt.savefig('grafico_temperatura.png', dpi=300)
print("Gráfico salvo como grafico_temperatura.png")