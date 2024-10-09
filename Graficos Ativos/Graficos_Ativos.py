import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Função para carregar os dados dos ativos
@st.cache
def load_data(ticker1, ticker2):
    # Baixar dados dos dois ativos
    end_date = pd.Timestamp.today()
    start_date = end_date - pd.DateOffset(years=1)
    
    # Baixar os dados do ativo 1
    stock_data1 = yf.download(ticker1, start=start_date, end=end_date)['Adj Close']
    
    # Baixar os dados do ativo 2
    stock_data2 = yf.download(ticker2, start=start_date, end=end_date)['Adj Close']
    
    # Juntar os dois em um DataFrame
    data = pd.DataFrame({
        ticker1: stock_data1,
        ticker2: stock_data2
    })
    
    # Remover linhas com valores faltantes
    data.dropna(inplace=True)
    
    return data

# Função para calcular a variação percentual em relação ao primeiro preço
def calculate_variation(data):
    return (data / data.iloc[0] - 1) * 100

# Título do aplicativo
st.title('Comparação de Variação Acumulada - Ação vs IBOV')

# Entrada para o usuário digitar o ticker do ativo 1
ticker1 = st.text_input('Digite o código do ativo 1 (ex: PETR4.SA)', 'PETR4.SA')

# Entrada para o usuário digitar o ticker do ativo 2 (padrão ^BVSP)
ticker2 = st.text_input('Digite o código do ativo 2 (ex: ^BVSP para IBOVESPA)', '^BVSP')

# Remover o '.SA' do nome do ativo para exibir no gráfico
ticker1_display = ticker1.replace('.SA', '') if ticker1.endswith('.SA') else ticker1
# Substituir ^BVSP por IBOV
ticker2_display = 'IBOV' if ticker2 == '^BVSP' else ticker2.replace('.SA', '')

# Botão para carregar os dados e gerar o gráfico
if st.button('Gerar gráfico'):
    # Carregar os dados
    data = load_data(ticker1, ticker2)
    
    # Calcular a variação percentual em relação ao primeiro preço
    data_pct = calculate_variation(data)
    
    # Plotar o gráfico de variação percentual
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Aumentar a grossura das linhas e definir o zorder para a ordem de sobreposição
    ax.plot(data_pct.index, data_pct[ticker2], color='lightblue', label=ticker2_display, linewidth=2.5, zorder=1)  # Linha do ativo 2 atrás
    ax.plot(data_pct.index, data_pct[ticker1], color='darkblue', label=ticker1_display, linewidth=2.5, zorder=2)  # Linha do ativo 1 na frente
    
    # Adicionar título e legendas
    ax.set_ylabel('%', fontsize=14)
    
    # Aumentar o tamanho dos números nos eixos
    ax.tick_params(axis='both', which='major', labelsize=14)  # Ajusta o tamanho dos números dos eixos
    
    # Aumentar o tamanho das legendas e colocá-las na parte de baixo
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=2, fontsize=14)
    
    # Ajustar o fundo do gráfico para transparente
    fig.patch.set_alpha(0.0)  # Fundo da imagem transparente
    ax.set_facecolor('none')   # Fundo do gráfico transparente
    
    # Exibir o gráfico no Streamlit
    st.pyplot(fig)
