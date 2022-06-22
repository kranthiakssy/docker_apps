# ---------------------------------IMPORT STATEMENTS------------------------------

from dash import Dash, dcc, html, Input, Output 
import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
import datetime
import psycopg2
from flask import Flask
import os

# ---------------------------------------IMPORT STATEMENTS END--------------------------------

server = Flask(__name__)
app = Dash(__name__, server=server, suppress_callback_exceptions=True)

# --------------------------------------- APP LAYOUT  ------------------------------------

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
index_page = html.Div([
    dcc.Link('TABLE',  href='/page-1'),
    html.Br(),
    dcc.Link('GRAPH', href='/page-2'),
])

# ------------------------------------------- APP LAYOUT END -------------------------------------

# ------------------------------------------- PAGE LAYOUT 1 ---------------------------------

page_1_layout = html.Div([ 
    html.H1("     DATA LOGGING  ",id="head",),
    html.H1(" AND VISUALIZATION APPLICATION", id="head",),
    dcc.Link('GRAPH', id="graph", href='/page-2'),
    html.Div(id='table-content'),
    html.Br(),
    html.Div(
    [ 
    html.Br(),
    html.Br(),
    html.Br(),
    ],
      style={'height': 20}), 

# -------------------------------------- TABLE CONTENT ------------------------------------   

    dash_table.DataTable(
        id='our-table', 
        columns=[{'name': 'VARIABLE-1', 'id': 'variable1', 'deletable': False, 'renamable': False},
                 {'name': 'VARIABLE-2', 'id': 'variable2', 'deletable': False, 'renamable': False},
                 {'name': 'VARIABLE-3', 'id': 'variable3', 'deletable': False, 'renamable': False},
                 {'name': 'VARIABLE-4', 'id': 'variable4', 'deletable': False, 'renamable': False}],
        data=[
              {'variable1': "", 'variable2': "", 'variable3': "", 'variable4': "" ,}
              ],
        editable=True,                  # allow user to edit data inside tabel          
        sort_mode="single",             # sort across 'multi' or 'single' columns        
        page_action='none',             # render all of the data at once. No paging.
        style_table={'height': '100px', 'overflowY': 'auto',},
        style_cell={'textAlign': 'center', 'minWidth': '100px', 'background-color': 'antiquewhite','border-radius':'17px' ,'width': '100px', 'maxWidth': '100px' , ' font-size': '25px'},
        style_cell_conditional=[
            {
                'if': {'column_id': c},
                'textAlign': 'center'
            } for c in ['variable3', 'variable4']
        ]),

    # -------------------------------------- TABLE CONTENT END  ------------------------------------   

    # ---------------------------------- SUBMIT BUTTON ----save_to_csv------------------

        html.Button('SUBMIT', id='save_to_csv', n_clicks=0 ), 
        html.Button('VIEW DATA ', id='display_csv', n_clicks=0), 
    html.Br(),
    html.Br(),
    html.Div(id='show_table' , style={"width": "40%","height":"10px","margin-left": "29%"}),
    dcc.Store(id="store", data=0),
    dcc.Interval(id='interval', interval=1000),

    # ------------------------------------- SUBMIT BUTTON END -----------------------------

    # ------------------------------------- GRAPH PAGE LINK -------------------------------

    html.Br(),
    html.Br(),
    html.Div(id='placeholder', children=[]),    
])
# Defining environemtn variables for Database connection
db_host = os.environ.get('DB_HOST','0.0.0.0')
db_name = os.environ.get('DB_NAME','exampledb')
db_user = os.environ.get('DB_USER','docker1')
db_pw = os.environ.get('DB_PW','bhel@123')

#  --------------------------------------------CSV FILE COMMANDS------------------------------

fieldnames = ["Time_Index","variable1","variable2","variable3","variable4"]

# ------------------------------------------ PAGE 1 LAYOUT END -------------------------------

# ------------------------------------------ PAGE 1 callback ----------------------------------

@app.callback(Output('page-1-content', 'children'),
              [Input('page-1-dropdown', 'value')])
def page_1_dropdown(value):
    return f'You have selected {value}'

# -------------------------------------------PAGE 1 CALLBACK END--------------------------

# -------------------------------------------- PAGE 2 LAYOUT --------------------------------

page_2_layout = html.Div([
     
    html.H1("     DATA LOGGING ",id="head" ),
    html.H1(" AND VISUALIZATION APPLICATION",id="head" ),
    html.Div(id='Graph-content'),
    html.Br(), 
    dcc.Link('TABLE',id='tab', href='/page-1',),
    html.Button('REFRESH', id='read_plant_data', n_clicks=0 ), 
    html.Br(),
            dcc.Dropdown(id='my_dropdown',
            options=[
                     {'label': 'variable1', 'value': 'variable1'},
                     {'label': 'variable2', 'value': 'variable2'},
                     {'label': 'variable3', 'value': 'variable3'},
                     {'label': 'variable4', 'value': 'variable4'},
            ],
            optionHeight=35,                    #height/space between dropdown options
            value='variable1',                    #dropdown value selected automatically when page loads
             multi=True,                        #allow multiple dropdown values to be selected
            searchable=True,                    #allow user-searching of dropdown values
            placeholder=' select variables...',     #gray, default text shown when no option is selected
            clearable=True,   
            style={
                "margin-top": "-0.5cm"

            }                  #allow user to removes the selected value
        ),
    html.Br(),
    html.Br(),
    html.Br(),
   dcc.Graph(id='my_graph')
    ]),
html.Div([
    dcc.Graph(id='the_graph')
])

# -------------------------------------------- PAGE 2 LAYOUT END --------------------------------

#--------------------------------------------- UPDATING INDEX ( PAGE CONTENT) ------------------------------

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return page_1_layout

#--------------------------------------------- UPDATING INDEX ( PAGE CONTENT) END  ------------------------------

# ---------------------------------------------UPDATE GRAPH ------------

@app.callback(
    Output('my_graph', 'figure'),
    Input('read_plant_data', 'n_clicks'),
    State('my_dropdown','value'),
    prevent_initial_call=True
)
def reload_data(n_clicks,yval):
    con = psycopg2.connect(
        host = db_host,
        database = db_name,
        user = db_user,
        password = db_pw
        )
    cur =con.cursor()
    cur.execute ("select * from plant_data")
    rows =cur.fetchall()
    pdata = pd.DataFrame(rows)
    pdata.columns = ['Time_Index', 'variable1', 'variable2', 'variable3','variable4']
    con.commit()     
    cur.close()
    con.close()
    fig = px.line(data_frame=pdata, x='Time_Index', y=yval)
    return fig

# ---------------------------------------------UPDATE GRAPH END ------------

 # --------------------------------------------- UPDATE TABLE --------------------

@app.callback(
    Output('show_table', 'children'),
    Input('display_csv', 'n_clicks'),
    
    prevent_initial_call=True
)
def reload_data(n_clicks):
    con = psycopg2.connect(
        host = db_host,
        database = db_name,
        user = db_user,
        password = db_pw
        )
    cur =con.cursor()
    cur.execute ("select * from plant_data")             
    rows =cur.fetchall()
    pdata = pd.DataFrame(rows)
    pdata.columns = ['Time_Index', 'variable1', 'variable2', 'variable3','variable4']
    con.commit()     
    cur.close()
    con.close()
    table1 = dash_table.DataTable(pdata.to_dict('records'), [{"name": i, "id": i} for i in pdata.columns])
    return table1

    # ------------------------------------- --- UPDATE TABLE END -------------------

# # ------------------------------------------ SAVE DATA CALLBACK -------------------

@app.callback(
    [Output('placeholder', 'children'),
    Output("store", "data")],
    Input('save_to_csv', 'n_clicks'),  
    State('our-table', 'data'),
    State('store', 'data'),
    prevent_initial_call=True)
def df_to_csv(n_clicks, dataset, s):
    output = html.Plaintext("DATA SUBMITTED...!",
                            style={'color':'black', 'font-weight': 'bold', 'font-size': '0.6cm' , 'margin-left': '13.7cm','margin-top': '-02.6cm'})
    no_output = html.Plaintext("", style={'margin': "10px"})
    input_triggered = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    if input_triggered == "save_to_csv":
        s = 5
        html.Plaintext("Executed")
        con = psycopg2.connect(
        host = db_host,
        database = db_name,
        user = db_user,
        password = db_pw
            )
        cur =con.cursor()
        cur.execute ("insert into plant_data (time_index,variable1,variable2,variable3,variable4) values(%s,%s,%s,%s,%s)",
                        (
                        str(datetime.datetime.now()),
                        dataset[0]['variable1'],
                        dataset[0]['variable2'],
                        dataset[0]['variable3'],
                        dataset[0]['variable4']                        
                        )
                    )
        con.commit()     
        cur.close()
        con.close()
        return output, s

# --------------------------------------- SAVE DATA CALLBACK END -------------------

# --------------------------------------- PORT NUMBER -----------------------------

if __name__ == '__main__':  
    app.run_server(debug=True, host='0.0.0.0', port=1999)
    
# -------------------------------------- END OF THE CODE -------------------------py