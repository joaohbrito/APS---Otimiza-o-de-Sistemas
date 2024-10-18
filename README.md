Objetivo do Trabalho

O objetivo deste trabalho é desenvolver um modelo de otimização para a alocação de ativos em uma carteira de investimentos, com o intuito de maximizar o retorno esperado, respeitando um limite de risco aceitável. A otimização é fundamental para investidores que buscam equilibrar suas carteiras de modo a alcançar o melhor desempenho possível, dado o nível de risco que estão dispostos a aceitar.
Objetivos Específicos:

Coletar dados históricos de preços de ativos financeiros.
Calcular o retorno esperado e a volatilidade (risco) dos ativos.
Aplicar técnicas de otimização para determinar a alocação ideal dos ativos.
Visualizar os resultados por meio de gráficos que demonstrem a fronteira eficiente, a alocação de ativos e o histórico de desempenho da carteira.

Abordagem Utilizada para a Otimização

A abordagem utilizada no projeto é baseada em um modelo de otimização conhecido como "Problema da Mochila", adaptado para a alocação de ativos. A implementação se dá nas seguintes etapas:

Coleta de Dados: Utilização da biblioteca yfinance para baixar dados de preços históricos dos ativos selecionados. A partir dos preços, são calculados:
O retorno esperado (média dos retornos diários multiplicada por 252 para anualização).
A volatilidade (desvio padrão dos retornos diários multiplicado pela raiz quadrada de 252).

Definição da Função Objetivo: A função que será maximizada (ou minimizada, neste caso, seu negativo) é o retorno esperado da carteira, dado pela soma ponderada dos retornos dos ativos com suas respectivas alocações.

Estabelecimento de Restrições:
Uma restrição para garantir que o risco total da carteira não exceda um limite predefinido.
Uma restrição que assegura que a soma das alocações dos ativos seja igual a 1.

Otimização: O método de otimização SLSQP (Sequential Least Squares Programming) é utilizado para encontrar a alocação ótima de ativos que maximiza o retorno esperado sob as restrições definidas.

Visualização dos Resultados: Gráficos são gerados para ilustrar a fronteira eficiente, a alocação de ativos e o histórico de desempenho da carteira.

Instruções de Instalação e Execução
1. Instalação de Dependências

Antes de executar o código, é necessário instalar as bibliotecas necessárias. Isso pode ser feito utilizando o gerenciador de pacotes pip. Se você não tiver um arquivo requirements.txt, crie um com as seguintes bibliotecas:

plaintext

numpy
pandas
yfinance
scipy
matplotlib
seaborn

Em seguida, execute o comando:

        

        pip install -r requirements.txt

2. Execução do Código

O código principal deve estar em um arquivo chamado main.py. Para executar o script e realizar a otimização da carteira, use o seguinte comando no terminal:

   

        python main.py

Após a execução, os gráficos correspondentes serão exibidos, mostrando os resultados da otimização.
Exemplo de Execução com Resultados Visualizados

Após executar o código com os ativos selecionados (por exemplo, AAPL, MSFT, GOOGL, AMZN), você deve observar os seguintes resultados:

Gráfico da Fronteira Eficiente:
Um gráfico de dispersão que mostra a relação entre o risco e o retorno esperado para diferentes alocações de ativos.
A linha da fronteira eficiente será visível, destacando as melhores combinações de risco-retorno.

Gráfico de Alocação de Ativos:
Um gráfico de pizza que ilustra como o capital está distribuído entre os ativos.
As porcentagens de alocação em cada ativo ajudam a entender a diversificação da carteira.

Gráfico de Histórico de Desempenho:
Um gráfico de linha que mostra o retorno acumulado da carteira ao longo do tempo.
O eixo X representa as datas e o eixo Y mostra o crescimento do capital investido.

Resultados Exemplo

Suponha que, após a execução, a alocação ótima encontrada foi:

AAPL: 40%
MSFT: 30%
GOOGL: 20%
AMZN: 10%

A fronteira eficiente pode mostrar um retorno esperado de 15% com um risco de 10%. O gráfico de desempenho pode ilustrar que a carteira teve um crescimento constante ao longo do período analisado, subindo de 1 para aproximadamente 1.5 em um ano.



Descrição do Projeto

Este projeto tem como objetivo otimizar a alocação de ativos em uma carteira de investimentos, maximizando o retorno esperado sob um limite de risco aceitável. Utiliza dados históricos de preços de ativos financeiros e implementa um modelo de otimização baseado no método Sequential Least Squares Programming (SLSQP).
Estrutura do Código
Funções Principais

Coleta de Dados
Objetivo: Coletar dados de preços de ativos financeiros e calcular os retornos esperados e a volatilidade (risco) dos ativos.
        
Implementação:


    dados = yf.download(ativos, start='2020-01-01', end='2023-01-01')['Adj Close']
    retornos = dados.pct_change().mean() * 252  # Retorno anualizado
    risco = dados.pct_change().std() * np.sqrt(252)  # Volatilidade anualizada

Função Objetivo

Objetivo: Maximizar o retorno esperado da carteira.
Implementação:



    def objetivo(x):
        return -np.dot(retornos, x)  # Retorno esperado negativo

    Parâmetros:
        x: Vetor que representa a fração do capital investido em cada ativo.

Restrições

Restrição de Risco: Garantir que o risco total da carteira não exceda um limite predefinido.


    def restricao_risco(x):
    return capacidade_risco - np.dot(risco, x)

Restrição de Soma: Garantir que a soma das alocações de todos os ativos seja igual a 1.



    def restricao_soma(x):
        return np.sum(x) - 1

Otimização

Objetivo: Encontrar a alocação ótima de ativos que maximiza o retorno esperado, respeitando as restrições definidas.

Implementação:



        resultado = minimize(objetivo, x0, method='SLSQP', bounds=limites, constraints=restricoes)

        Parâmetros:
            x0: Alocação inicial dos ativos (distribuição igual entre os ativos).
            method: Método de otimização (SLSQP).
            bounds: Limites para as alocações (0 a 1 para cada ativo).
            constraints: Restrições definidas.

Funções de Visualização

 Gráfico da Fronteira Eficiente
 Objetivo: Visualizar a relação entre risco e retorno para diferentes alocações de ativos.
Implementação:



    def plot_fronteira():
        # Gera e plota a fronteira eficiente

Descrição:
A função gera 1000 alocações aleatórias de ativos, calculando o risco e o retorno para cada uma. Os pontos são plotados em um gráfico de dispersão, onde o eixo X representa o risco (volatilidade) e o eixo Y representa o retorno esperado. Isso ajuda a visualizar a "fronteira eficiente", que é a melhor combinação de risco e retorno.

Gráfico de Alocação de Ativos

Objetivo: Mostrar a distribuição do capital entre os ativos da carteira.
Implementação:



    def plot_alocacao_ativos(alocacao, ativos):
        # Plota um gráfico de pizza com a alocação

Descrição:
A função utiliza um gráfico de pizza para ilustrar a porcentagem do capital alocado em cada ativo da carteira. Cada fatia do gráfico representa a proporção de investimento em um ativo específico, facilitando a visualização da diversificação da carteira.

Gráfico de Histórico de Desempenho

Objetivo: Visualizar o retorno acumulado da carteira ao longo do tempo.
Implementação:



        def plot_historico_desempenho(retorno_acumulado):
            # Plota o histórico de desempenho

Descrição:
A função plota o retorno acumulado da carteira ao longo do período analisado. O eixo X representa o tempo (datas), e o eixo Y mostra o retorno acumulado, permitindo que os usuários visualizem a performance da carteira e como ela evoluiu ao longo do tempo.

Como Usar
Instalar Dependências: Utilize o arquivo requirements.txt para instalar as bibliotecas necessárias.


        pip install -r requirements.txt

Executar o Código: Execute o arquivo principal para realizar a otimização e gerar os gráficos.



    python main.py

Visualizar Resultados: Após a execução, os gráficos da fronteira eficiente, alocação de ativos e histórico de desempenho serão exibidos.

Considerações Finais

Este projeto fornece uma base para a otimização de carteiras financeiras e pode ser expandido com novos ativos, diferentes medidas de risco ou abordagens de otimização. Sinta-se à vontade para modificar e adaptar conforme necessário.
