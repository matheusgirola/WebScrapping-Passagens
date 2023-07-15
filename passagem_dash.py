import numpy as np
import pandas as pd
import plotly 
import plotly.express as px
import os
import datetime as dt

from dash import Dash, html, dash_table, dcc
from dash.dependencies import Input, Output

def hj(today = dt.datetime.today()):
    hj = today.strftime('%d-%m-%Y')
    
    return hj

test_df = pd.DataFrame(columns = ['Companhia', 
                                  'Data de Coleta', 
                                  'Data da Passagem', 
                                  'Preço Mínimo',
                                  'Média dos Preços'])

for folder in os.listdir('C:/Users/MATHEUS/Desktop/Biblioteca/Python/WebScrapping_Passagens/Azul/' + hj()):
    try:
        date_df = pd.read_pickle('C:/Users/MATHEUS/Desktop/Biblioteca/Python/WebScrapping_Passagens/Azul/' + hj() + '/'+ folder)
        prices = date_df["Preço (R$)"]    
    except:
        prices = np.nan
        
    try:
        min_price = prices.min()
        avg_price = prices.mean()
    except:
        min_price = np.nan
        avg_price = np.nan
            
    new_row = {'Companhia': 'Azul', 
                'Data de Coleta': hj(), 
                'Data da Passagem': folder[0:10], 
                'Preço Mínimo': [min_price],
                'Média dos Preços': round(avg_price, 2)}
    test_df = pd.concat([test_df, pd.DataFrame.from_dict(new_row)])
        
for folder in os.listdir(f'C:/Users/MATHEUS/Desktop/Biblioteca/Python/WebScrapping_Passagens/Latam/' + hj()):
    try:
        date_df = pd.read_pickle('C:/Users/MATHEUS/Desktop/Biblioteca/Python/WebScrapping_Passagens/Latam/' + hj() + '/' + folder)
        prices = date_df["Preço (R$)"]          
    except:
        prices = np.nan
        
    try:
        min_price = prices.min()
        avg_price = prices.mean()
    except:
        min_price = np.nan
        avg_price = np.nan
            
    new_row = {'Companhia': 'Latam', 
                'Data de Coleta': hj(), 
                'Data da Passagem': folder[0:10], 
                'Preço Mínimo': [min_price],
                'Média dos Preços': round(avg_price, 2) }
    test_df = pd.concat([test_df, pd.DataFrame.from_dict(new_row)])
        
for folder in os.listdir(f'C:/Users/MATHEUS/Desktop/Biblioteca/Python/WebScrapping_Passagens/Gol/' + hj()):
    try:
        date_df = pd.read_pickle('C:/Users/MATHEUS/Desktop/Biblioteca/Python/WebScrapping_Passagens/Gol/' + hj() + '/' + folder)
        prices = date_df["Preço (R$)"]          
    except:
        prices = np.nan
        
    try:
        min_price = prices.min()
        avg_price = prices.mean()
    except:
        min_price = np.nan
        avg_price = np.nan
            
    new_row = {'Companhia': 'Gol', 
                'Data de Coleta': hj(), 
                'Data da Passagem': folder[0:10], 
                'Preço Mínimo': [min_price],
                'Média dos Preços': round(avg_price, 2) }
    test_df = pd.concat([test_df, pd.DataFrame.from_dict(new_row)])

test_df['Data de Coleta'] = pd.to_datetime(test_df['Data de Coleta'], format='%d-%m-%Y')
test_df['Data da Passagem'] = pd.to_datetime(test_df['Data da Passagem'], format='%d-%m-%Y')
test_df = test_df.sort_values(by=['Data da Passagem'])
#tmp = df[(df['Data de Coleta'] > '2023-06-30')]
test_df['Data de Coleta'] = test_df['Data de Coleta'].astype(str)
test_df['Data da Passagem'] = test_df['Data da Passagem'].astype(str)
tmp = test_df[(test_df['Data de Coleta'] >= '2023-06-30')]    

df = tmp
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.Div(children='Preços de Passagens de Recife ao Rio de Janeiro nos Próximos Meses'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    
    html.Div(
        dcc.Graph(id='graph',
                  style={'height': 400, 'width': 800}
                  ),
    ),
    html.Div([
                html.Label(['Tipo de preço:'],style={'font-weight': 'bold'}),
                dcc.RadioItems(
                    id='radio',
                    options=[
                             {'label': 'mínimo', 'value': 'graph1'},
                             {'label': 'média', 'value': 'graph2'},
                    ],
                    value='age',
                    style={"width": "60%"}
                ),
        ])

])



# ---------------------------------------------------------------
@app.callback(
    Output('graph', 'figure'),
    [Input(component_id='radio', component_property='value')]
)
def build_graph(value):
    if value == 'graph1':
        return px.line(
            df,
            x="Data da Passagem",
            y="Preço Mínimo",
            color="Companhia"
        )
    else:
        return px.line(
            df,
            x="Data da Passagem",
            y="Média dos Preços",
            color="Companhia"
        )

if __name__ == '__main__':
    app.run_server(debug=True)