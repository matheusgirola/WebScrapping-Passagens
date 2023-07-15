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

df = pd.read_pickle(f"https://github.com/matheusgirola/WebScrapping-Passagens/blob/master/1_Dash_Data/{hj()}.pkl?raw=True")


# Dash App Part %---------------------------------------------------------------------------
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