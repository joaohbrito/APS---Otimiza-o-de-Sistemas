import numpy as np
import pandas as pd
import yfinance as yf
from scipy.optimize import minimize
import plotly.graph_objects as go

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

# Funções de visualização com Plotly
def plot_fronteira():
    riscos = []
    retornos_esperados = []

    for _ in range(1000):
        x0 = np.random.dirichlet(np.ones(num_ativos))  # Alocação aleatória
        risco_portfolio = np.dot(risco, x0)
        retorno_portfolio = np.dot(retornos, x0)

        riscos.append(risco_portfolio)
        retornos_esperados.append(retorno_portfolio)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=riscos,
        y=retornos_esperados,
        mode='markers',
        marker=dict(size=5, color='blue', opacity=0.5),
        name='Fronteira Eficiente'
    ))

    fig.update_layout(
        title='Fronteira Eficiente',
        xaxis_title='Risco (Volatilidade)',
        yaxis_title='Retorno Esperado',
        showlegend=True
    )
    fig.show()

def plot_alocacao_ativos(alocacao, ativos):
    fig = go.Figure(data=[go.Pie(labels=ativos, values=alocacao, hole=.3)])

    fig.update_layout(
        title='Alocação de Ativos na Carteira',
    )
    fig.show()

def plot_historico_desempenho(retorno_acumulado):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=retorno_acumulado.index,
        y=retorno_acumulado,
        mode='lines',
        name='Retorno Acumulado',
        line=dict(color='blue')
    ))

    fig.update_layout(
        title='Histórico de Desempenho da Carteira',
        xaxis_title='Data',
        yaxis_title='Retorno Acumulado',
        showlegend=True
    )
    fig.show()

# Exibir resultados
print("Alocação ótima:", alocacao)
print("Retorno esperado:", -resultado.fun)
print("Risco da carteira:", np.dot(risco, alocacao))

# Plotar gráficos
plot_fronteira()  # Gráfico da Fronteira Eficiente
plot_alocacao_ativos(alocacao, ativos)  # Gráfico de Alocação de Ativos
plot_historico_desempenho(retorno_acumulado)  # Gráfico de Histórico de Desempenho
