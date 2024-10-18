import numpy as np
import pandas as pd
import yfinance as yf
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# Coleta de dados
ativos = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
dados = yf.download(ativos, start='2020-01-01', end='2023-01-01')['Adj Close']
retornos = dados.pct_change().mean() * 252  # Retorno anualizado
risco = dados.pct_change().std() * np.sqrt(252)  # Volatilidade anualizada

# Função objetivo
def objetivo(x):
    return -np.dot(retornos, x)

# Restrições
def restricao_risco(x):
    return capacidade_risco - np.dot(risco, x)

def restricao_soma(x):
    return np.sum(x) - 1

# Parâmetros
capacidade_risco = 0.2
num_ativos = len(ativos)

# Restrições e limites
restricoes = [{'type': 'eq', 'fun': restricao_soma},
              {'type': 'ineq', 'fun': restricao_risco}]
limites = tuple((0, 1) for _ in range(num_ativos))

# Solução
x0 = np.ones(num_ativos) / num_ativos
resultado = minimize(objetivo, x0, method='SLSQP', bounds=limites, constraints=restricoes)

# Calcular retorno diário da carteira
alocacao = resultado.x
retorno_diario = dados.pct_change()
retorno_carteira = (retorno_diario * alocacao).sum(axis=1)
retorno_acumulado = (1 + retorno_carteira).cumprod()

# Funções de visualização
def plot_fronteira():
    riscos = []
    retornos_esperados = []

    for _ in range(1000):
        x0 = np.random.dirichlet(np.ones(num_ativos))  # Alocação aleatória
        risco_portfolio = np.dot(risco, x0)
        retorno_portfolio = np.dot(retornos, x0)

        riscos.append(risco_portfolio)
        retornos_esperados.append(retorno_portfolio)

    plt.figure(figsize=(10, 6))
    plt.scatter(riscos, retornos_esperados, c='blue', marker='o', alpha=0.3)
    plt.title('Fronteira Eficiente')
    plt.xlabel('Risco (Volatilidade)')
    plt.ylabel('Retorno Esperado')
    plt.grid()
    plt.show()

def plot_alocacao_ativos(alocacao, ativos):
    plt.figure(figsize=(8, 6))
    plt.pie(alocacao, labels=ativos, autopct='%1.1f%%', startangle=140)
    plt.title('Alocação de Ativos na Carteira')
    plt.axis('equal')
    plt.show()

def plot_historico_desempenho(retorno_acumulado):
    plt.figure(figsize=(10, 6))
    plt.plot(retorno_acumulado, label='Retorno Acumulado da Carteira', color='blue')
    plt.title('Histórico de Desempenho da Carteira')
    plt.xlabel('Data')
    plt.ylabel('Retorno Acumulado')
    plt.legend()
    plt.grid()
    plt.show()

# Exibir resultados
print("Alocação ótima:", alocacao)
print("Retorno esperado:", -resultado.fun)
print("Risco da carteira:", np.dot(risco, alocacao))

# Plotar gráficos
plot_fronteira()  # Gráfico da Fronteira Eficiente
plot_alocacao_ativos(alocacao, ativos)  # Gráfico de Alocação de Ativos
plot_historico_desempenho(retorno_acumulado)  # Gráfico de Histórico de Desempenho
