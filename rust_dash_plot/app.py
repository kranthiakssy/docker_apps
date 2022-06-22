import base64
import datetime
import time
import io

from click import style
import csv
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

from flask import Flask

import plotly.express as px

import pandas as pd
import numpy as np

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"

server = Flask(__name__)

app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.Row(dbc.Col(html.H1("Data Plotting Application",
                                className="shadow-sm p-3 mb-3 bg-light rounded text-center", 
                                style={'width':'98%','margin': '10px','color':'#3f826d'}
                                ),           
                ),
                justify='center',
        ),
    dbc.Row([
            dbc.Col(dbc.Input(id="ip_in", placeholder="Enter Server IP here..", type="text", style={'margin': '10px'}),
                width=2,
                ),
            dbc.Col(dbc.Input(id="port_in", placeholder="Enter Port no..", type="text", style={'margin': '10px'}),                
                width=1,
                ),
            dbc.Col(dbc.Input(id="reg_add_in", placeholder="Enter Reg Address here..", type="text", style={'margin': '10px'}),                
                width=2,
                ),
            dbc.Col(dbc.Button('Collect_Data', id='collect-data', n_clicks=0, style={'width': '120px','margin': '10px'}),
                width=1,
                ),
            dbc.Col(dbc.Button('Stop_Collect', id='stop-data', n_clicks=0, style={'width': '120px','margin': '10px'}),
                width=1,
                ),
            dbc.Col(dbc.Button('Update', id='update-data', n_clicks=0, style={'width': '100px','margin': '10px'}),
                width=1,
                ),
            dbc.Col(dcc.Loading(id='msg_uploading_1',
                                    type="circle",
                                    children=html.Div(id='msg_upload',
                                    style={'textAlign': 'center','color':'#4130a4','margin': '10px'})
                                    ),                
                width=2,
                ),
            dbc.Col(html.Div(id='stop_msg'),
                width=1,
                ),
            ]),

    dbc.Row(dbc.Col(dcc.Loading(id='msg_updating_1',
                                    type="default",
                                    children=html.Div(id='msg_update',
                                                        style={'textAlign': 'center','color':'#4130a4','margin': '20px'}
                                                        )
                                    ),
                width={'size':4,'offset':1},
                ),
        ),

    dbc.Row([
            dbc.Col(dcc.Dropdown(id='dd_xaxis',
                                    placeholder="Select X-axis Variable",
                                    style={'margin': '10px 5px'},
                                    multi=False
                        ),
                width=2,
                ),
            dbc.Col(dcc.Dropdown(id='dd_yaxis',
                                    placeholder="Select Y-axis Variables",
                                    style={'margin': '10px 5px'},
                                    multi=True
                        ),
                width=7,
                ),
            dbc.Col(dbc.Button('Plot', id='plot-val', n_clicks=0, style={'width': '100px','margin': '10px 5px'}),
                width=1,
                ),
            dbc.Col(dcc.Loading(id='msg_plotiing_1',
                                    type="graph",
                                    fullscreen=False,
                                    children=html.Div(id='msg_plot',
                                                        style={'textAlign': 'left','color':'Green','margin': '10px 5px'}
                                                        )
                                    ),
                width=2,
                ),
        ]),

    dcc.Graph(id='line_plot',
                figure={},
                style={'width':'98%','height':'650px','margin':'20px 10px'},
                className="shadow p-3 mb-5 bg-light rounded"
                ),

    # dcc.Store inside the user's current browser session
    dcc.Store(id='store-data', data=[], storage_type='memory') # 'local' or 'session'
])

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return None
    return df
end_coll = 0

@app.callback(Output('msg_upload', 'children'),
              Input('collect-data', 'n_clicks'),
              State('ip_in', 'value'),
              State('port_in', 'value'),
              State('reg_add_in', 'value'),
              prevent_initial_call=True)
def data_collection(click, ip, port, reg_add):
    global end_coll
    stop_coll = 0
    reg = reg_add.split(' ')
    no_reg = len(reg)
    fd_dict = {}
    fieldnames = ['Time_Index']
    for i in range(no_reg):
        fieldnames.append(reg[i])
    with open('data_rust.csv', 'w') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                csv_writer.writeheader()
    client = ModbusTcpClient(host=ip,
                            port=int(port)
                            )
    while stop_coll == 0:
        fd_dict['Time_Index'] = str(datetime.datetime.now())
        for j in range(no_reg):
            val = client.read_holding_registers(int(reg[j]), 2)
            decoder_val = BinaryPayloadDecoder.fromRegisters(val.registers, 
                                                            byteorder=Endian.Big, 
                                                            wordorder=Endian.Big
                                                            )
            fd_dict[reg[j]] = decoder_val.decode_32bit_float()
        with open('data_rust.csv', 'a') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator = '\n')
                csv_writer.writerow(fd_dict)       
        if end_coll == 1:
            stop_coll = 1
            end_coll = 0
        time.sleep(1)
    
    client.close()
    return u'Data Collected successfully. Click on Update button.'

@app.callback(Output('stop_msg', 'children'),
              Input('stop-data', 'n_clicks'),
              prevent_initial_call=True)              
def end_collectio(click):
    global end_coll
    end_coll = 1
    return u' '

@app.callback(Output('dd_xaxis', 'options'),
              Output('dd_yaxis', 'options'),
              Output('msg_update', 'children'),
              Input('update-data', 'n_clicks'),
              prevent_initial_call=True)
              
def update_dropdowns(click):
    dff = pd.read_csv('data_rust.csv')
    lst = dff.columns
    dd = [o for o in lst]
    return [dd, dd, f'Variables Updated. Please select the variables and click on "Plot" Button.']

@app.callback(Output('line_plot', 'figure'),
              Output('msg_plot', 'children'),
              Input('plot-val', 'n_clicks'),
              State('dd_xaxis', 'value'),
              State('dd_yaxis', 'value'),
              prevent_initial_call=True)
def update_dropdowns(click2,xval,yval):
    dff = pd.read_csv('data_rust.csv')
    fig = px.line(dff, x=xval, y=yval, title='Time series plot')
    return [fig, f'Plotted!']

if __name__ == '__main__':
    app.run_server(debug=True,host="0.0.0.0",port=8050)
