import base64
import datetime
import io

from click import style

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

from flask import Flask

import plotly.express as px

import pandas as pd

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
            dbc.Col(dcc.Upload(id='upload-data',
                        children=html.Div([
                            'Drag and Drop or ',
                            html.A('Select Files'),
                        ]),                        
                        style={
                            # 'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                            },
                        # Allow multiple files to be uploaded
                        multiple=False
                        ),
                width=4,
                ),
            dbc.Col(dcc.Loading(id='msg_uploading_1',
                                    type="circle",
                                    children=html.Div(id='msg_upload',
                                    style={'textAlign': 'center','color':'#4130a4','margin': '10px'})
                                    ),                
                width=3,
                ),
            dbc.Col(dbc.Button('Update', id='update-val', n_clicks=0, style={'width': '100px','margin': '10px'}),
                width=2,
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


@app.callback(Output('store-data', 'data'),
              Output('msg_upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'),
              prevent_initial_call=True)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        dff = parse_contents(list_of_contents, list_of_names, list_of_dates)
        return [dff.to_dict('records'), u'{} uploaded successfully. Click on Update button.'.format(list_of_names,)]

@app.callback(Output('dd_xaxis', 'options'),
              Output('dd_yaxis', 'options'),
              Output('msg_update', 'children'),
              Input('update-val', 'n_clicks'),
              State('store-data', 'data'),
              prevent_initial_call=True)
              
def update_dropdowns(click,data):
    dff = pd.DataFrame(data)
    lst = dff.columns
    dd = [o for o in lst]
    return [dd, dd, f'Variables Updated. Please select the variables and click on "Plot" Button.']

@app.callback(Output('line_plot', 'figure'),
              Output('msg_plot', 'children'),
              Input('plot-val', 'n_clicks'),
              State('store-data', 'data'),
              State('dd_xaxis', 'value'),
              State('dd_yaxis', 'value'),
              prevent_initial_call=True)
def update_dropdowns(click2,data2,xval,yval):
    dff = pd.DataFrame(data2)
    fig = px.line(dff, x=xval, y=yval, title='Time series plot')
    return [fig, f'Plotted!']

if __name__ == '__main__':
    app.run_server(debug=True,host="0.0.0.0",port=8050)
