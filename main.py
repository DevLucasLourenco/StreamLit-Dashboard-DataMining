import streamlit as st
import pandas as pd
import plotly.express as px


class DataMining():
    def __init__(self):
        self.dataframe = None
        self.ler_tratar_dataframe()
        
        self.mes_sidebar = st.sidebar.selectbox('Mês', self.dataframe['Month'].unique())
        self.dataframe_filtrado = self.dataframe[self.dataframe['Month'] == self.mes_sidebar]


    def ler_tratar_dataframe(self):
        self.dataframe = pd.read_csv('supermarket_sales.csv', sep=';', decimal=',')
        self.dataframe['Date'] = pd.to_datetime(self.dataframe['Date'])
        self.dataframe['Month'] = self.dataframe['Date'].apply(lambda x: f'{str(x.year)} - {str(x.month)}')
        self.dataframe = self.dataframe.sort_values('Date')
        


class Dashboard(DataMining):
    st.set_page_config(layout='wide')

    def __init__(self):
        self.dados = DataMining()
        self.definicao_colunas()

        self.data_sharp:dict = {
        'total_cidade' : self.dados.dataframe_filtrado.groupby('City')[['Total']].sum().reset_index(),
        'fitro_avaliacao' : self.dados.dataframe_filtrado.groupby('City')[['Rating']].mean().reset_index()
        }


    def definicao_colunas(self):
        self.col1, self.col2 = st.columns(2)
        self.col3, self.col4, self.col5 = st.columns(3)


    def dashboard(self):
        fig_data = px.bar(self.dados.dataframe_filtrado, x='Date', y='Total',
                            color='City', title='Faturamento por dia')
        self.col1.plotly_chart(fig_data, use_container_width=True)

        
        fig_produto = px.bar(self.dados.dataframe_filtrado, x='Date', y='Product line', 
                     color='City', title='Faturamento por tipo de produto',
                     orientation='h')
        self.col2.plotly_chart(fig_produto, use_container_width=True)


        fig_cidade = px.bar(self.data_sharp['total_cidade'], x='City', y='Total', 
                        title='Faturamento por filial')
        self.col3.plotly_chart(fig_cidade, use_container_width=True)


        fig_tipo_pagamento = px.pie(self.dados.dataframe_filtrado, values='Total', names='Payment', 
                            title='Faturamento por tipo de pagamento')
        self.col4.plotly_chart(fig_tipo_pagamento, use_container_width=True)


        fig_avaliacao = px.bar(self.data_sharp['fitro_avaliacao'], y='Rating', x='City',
                               title='Avaliação')
        self.col5.plotly_chart(fig_avaliacao, use_container_width=True)



if __name__ =='__main__':
    Dashboard().dashboard()
    