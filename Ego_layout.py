import pandas as pd
from dash import Dash, html
from dash import dcc, no_update
from dash.dependencies import Input, Output, State
import dash_cytoscape as cyto  # pip install dash-cytoscape
import numpy as np
import dash_bootstrap_components as dbc

# import dash_bootstrap_components as dbc

import visdcc  # pip install visdcc

# 外部css元件
external_stylesheets = ['https://unpkg.com/antd@3.1.1/dist/antd.css',
                        'https://rawgit.com/jimmybow/CSS/master/visdcc/DataTable/Filter.css',
                        'https://cdnjs.cloudflare.com/ajax/libs/vis/4.20.1/vis.min.css',
                        ]
origin_key_dict_pd = pd.read_csv('NER_analysis_data/NER_old/entityDict.csv')

# 關鍵字類別
keyword_class_list = ["com", "rocket", "org", "satellite", "term", "loc"]
filter_class_list = ["com", "rocket", "org", "satellite", "term", "loc"]

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    html.H1("國防太空文集 NER單中心網路分析",
            style={
                'font-size': '36px',
                'textAlign': 'center',
                'backgroundColor': '#daf5ed',
                'margin': '0px',
                'font-weight': 'bold',
                'padding': '5px'
            }
            ),
    html.H6('以特定主題為中心，從文集中選出相關性最高的關鍵詞，並對它們進行社會網絡分析',
            style={
                'font-size': '24px',
                'textAlign': 'center',
                'backgroundColor': '#f2efe4',
                'padding': '3px',
                'margin': '0px',
            }
            ),
    html.Div([
        html.Div([
            dbc.Label("選擇關鍵字類別",
                      style={
                          'font-size': '16px',
                          'color': '#CA774B',
                          'font-weight': 'bold'}),
            # 切換類別下拉式選單
            dcc.Dropdown(
                id='dropdown_choose_class',
                value=4,
                clearable=False,
                options=[
                    {'label': clas, 'value': i}
                    for i, clas in enumerate(keyword_class_list)
                ],
                style={'margin': '0.5rem 0rem 0.8rem 0rem'}
            ),
            dbc.Label("選擇關鍵字",
                      style={
                          'font-size': '16px',
                          'color': '#CA774B',
                          'font-weight': 'bold'}),
            # 選擇中心詞下拉式選單
            dcc.Dropdown(
                id='dropdown_choose_name',
                value='3D printing',
                clearable=False,
                options=[
                    {'label': name, 'value': name}
                    for name in origin_key_dict_pd[origin_key_dict_pd['label'] == keyword_class_list[0]]['keywords'].to_list()
                ],
                style={'margin': '0.5rem 0rem 0.8rem 0rem'}
            ),
            dbc.Label("網路篩選遮罩",
                      style={
                          'font-size': '16px',
                          'color': '#CA774B',
                          'font-weight': 'bold'}),
            # 網路篩選遮罩下拉式選單
            dcc.Dropdown(
                id='dropdown_choose_filter',
                # value= "不篩選",
                clearable=False,
                multi=True,
                options=[
                    {'label': method, 'value': method}
                    for i, method in enumerate(filter_class_list)
                ],
                style={'margin': '0.5rem 0rem 0rem 0rem'}
            ),
            html.H6('針對網路圖的節點類別進行篩選',
                    style={
                        'color': '#66828E',
                        'font-size': '14px',
                        'margin': '0rem 0rem 0.8rem 0rem'}),

            dbc.Label("設定網路節點數量",
                      style={
                          'font-size': '16px',
                          'color': '#CA774B',
                          'font-weight': 'bold',
                          'display': 'inline-block',
                          'margin': '0.5rem 1.5rem 0rem 0rem'}),  # top,right,bottom,left
            dcc.Dropdown(
                id='total_nodes_num',
                options=[{'label': str(i), 'value': i}
                         for i in range(4, 21)],
                value=8,
                style={
                    'verticalAlign': 'top',
                    'margin': '0rem 1.5rem 0rem 0rem',
                    'display': 'inline-block'
                }
            ),
            dbc.Label("依關聯節度篩選鏈結",
                      style={
                          'font-size': '16px',
                          'margin': '1rem 0rem 0rem 0rem',
                          'color': '#CA774B',
                          'font-weight': 'bold',
                          'display': 'block'}),
            # 網路圖篩選節點閥值slider
            dcc.Slider(
                id="threshold_slide", min=0, max=1, step=0.01,
                tooltip={
                    "placement": "bottom",
                    "always_visible": True,
                },
                marks={i/10: str(i/10) for i in range(51)},
                value=0.5
            ),
            dbc.Label("字詞連結段落", style={
                      'font-size': '16px',
                      'color': '#CA774B',
                      'font-weight': 'bold',
                      'margin': '1rem 1.5rem 0rem 0rem',
                      'display': 'inline-block'}),
            # 計算單位選鈕
            dcc.RadioItems(
                id='RadioItems_SenorDoc',
                options=[{'label': '句 ', 'value': 'Sentence'},
                         {'label': '篇', 'value': 'Document'},],
                value='Sentence',
                inline=True,
                style={'margin': '0.5rem 1rem 0rem 0rem',
                       'display': 'inline-block'}
            ),
            dbc.Label("連結強度計算方式",
                      style={
                          'font-size': '16px',
                          'color': '#CA774B',
                          'font-weight': 'bold',
                          'margin': '0.5rem 0rem 0rem 0rem',
                          'display': 'block'}),
            dcc.RadioItems(
                id='RadioItems_CRorCO',
                options=[{'label': '共同出現次數', 'value': 'co-occurrence'},
                         {'label': '相關係數', 'value': 'correlation'},],
                value='correlation',
                inline=True,
                style={'margin': '0.5rem 0rem 0rem 0rem'}
            ),
            dbc.Label("連結強度依據字詞出現頻率", style={
                      'font-size': '14px', 'color': '#66828E', 'margin': '0rem 0rem 0.1rem 0rem', }),
            html.Br(),
            dbc.Label("較高，可選「相關係數」", style={
                      'font-size': '14px', 'color': '#66828E', 'margin': '0rem 0rem 0.1rem 0rem', }),
            html.Br(),
            dbc.Label("較低，可擇「共同出現次數」", style={
                      'font-size': '14px', 'color': '#66828E', 'margin': '0rem 0rem 0.1rem 0rem', }),
        ],
            style={
            'background-color': '#daf5ed',
            'display': 'inline-block',
            'width': '15%',
            'height': '1000px',
            'padding': '0.5%'}
        ),
        html.Div([
            # legend
            html.Div([
                html.Div("term", style={
                 'background-color': "#CA774B", 'padding': '20px', 'color': 'white', 'display': 'inline-block', 'width': '16.6%'}),
                html.Div("loc", style={
                    'background-color': "#CC5F5A", 'padding': '20px', 'color': 'white', 'display': 'inline-block', 'width': '16.6%'}),
                html.Div("com", style={
                    'background-color': "#66828E", 'padding': '20px', 'color': 'white', 'display': 'inline-block', 'width': '16.6%'}),
                html.Div("rocket", style={
                    'background-color': "#FEC37D", 'padding': '20px', 'color': 'white', 'display': 'inline-block', 'width': '16.7%'}),
                html.Div("satellite", style={
                    'background-color': "#678F74", 'padding': '20px', 'color': 'white', 'display': 'inline-block', 'width': '16.6%'}),
                html.Div("org", style={
                    'background-color': "#D4C3AA", 'padding': '20px', 'color': 'white', 'display': 'inline-block', 'width': '16.6%'}),
            ], style={
                'background-color': "#ede7d1",  'color': '#f2efe4', 'height': '7.5%', 'text-align': 'center', 'font-size': '24px', 'padding': '0px'}),
            # 放置網路圖
            html.Div("graph", style={
                'background-color': "white",  'color': 'black'}),
        ], style={'display': 'inline-block', 'width': '50%', 'height': '1000px', 'verticalAlign': 'top'}),
        # 放置文章
        html.Div("article", style={
            'background-color': "#66828E",  'color': 'white', 'display': 'inline-block', 'width': '35%', 'height': '1000px', 'verticalAlign': 'top'}),
    ], style={'height': '100%', 'width': '100%'}),

])

# Turn off reloader if inside Jupyter
app.run_server(debug=True)
