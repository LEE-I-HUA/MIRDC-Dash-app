from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

dtm = pd.read_csv('freq_DTM.csv')

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='國防 SpaceNews 關鍵字詞聲量趨勢查詢', style={'textAlign': 'center'}),
    html.H2(children='關鍵字趨勢', style={
        'font-size': '28px', 'textAlign': 'center', "color": '#36451a'}),
    html.Div([
        html.Hr(style={'borderWidth': "1vh", "width": "100%",
                "borderColor": "#83A742", "opacity": "unset"}),
        html.H3(children='選擇類別', style={'textAlign': 'left'}),
        dcc.RadioItems(id='inputLabel',
                       options=[
                           {'label': '一般術語', 'value': 'term'},
                           {'label': '公司', 'value': 'com'},
                           {'label': '組織', 'value': 'org'},
                           {'label': '衛星', 'value': 'satellite'},
                           {'label': '國家地區', 'value': 'loc'},
                           {'label': '火箭', 'value': 'rocket'}
                       ],
                       value="loc",
                       inline=True
                       ),
        html.H3(children='選擇關鍵字排名區間', style={'textAlign': 'left'}),
        dcc.RangeSlider(min=1, max=50, step=1, value=[1, 10], tooltip={
                        "placement": "bottom", "always_visible": True}, id='K'),
        html.Div([
            html.Div([
                html.H3(children='起始日', style={
                        'width': '30%', 'display': 'inline-block'}),

                dcc.Dropdown(
                    options=[
                        {'label': '2017', 'value': '2017'},
                        {'label': '2018', 'value': '2018'},
                        {'label': '2019', 'value': '2019'},
                        {'label': '2020', 'value': '2020'},
                        {'label': '2021', 'value': '2021'},
                        {'label': '2022', 'value': '2022'},
                        {'label': '2023', 'value': '2023'},
                    ],
                    value='2017', id='year_from', style={'width': '30%', 'display': 'inline-block'}
                ),
                dcc.Dropdown(
                    options=[
                        {'label': '一月', 'value': '01'},
                        {'label': '二月', 'value': '02'},
                        {'label': '三月', 'value': '03'},
                        {'label': '四月', 'value': '04'},
                        {'label': '五月', 'value': '05'},
                        {'label': '六月', 'value': '06'},
                        {'label': '七月', 'value': '07'},
                        {'label': '八月', 'value': '08'},
                        {'label': '九月', 'value': '09'},
                        {'label': '十月', 'value': '10'},
                        {'label': '十一月', 'value': '11'},
                        {'label': '十二月', 'value': '12'}
                    ],
                    value='01', id='month_from', style={'width': '30%', 'display': 'inline-block'}
                ),
            ], style={'width': '50%', 'display': 'inline-block'}),
            html.Div([
                html.H3(children='終止日', style={
                    'textAlign': 'left', 'width': '30%', 'display': 'inline-block'}),
                dcc.Dropdown(
                    options=[
                        {'label': '2017', 'value': '2017'},
                        {'label': '2018', 'value': '2018'},
                        {'label': '2019', 'value': '2019'},
                        {'label': '2020', 'value': '2020'},
                        {'label': '2021', 'value': '2021'},
                        {'label': '2022', 'value': '2022'},
                        {'label': '2023', 'value': '2023'},
                    ],
                    value='2017', id='year_to', style={'width': '30%', 'display': 'inline-block'}
                ),
                dcc.Dropdown(
                    options=[
                        {'label': '一月', 'value': '01'},
                        {'label': '二月', 'value': '02'},
                        {'label': '三月', 'value': '03'},
                        {'label': '四月', 'value': '04'},
                        {'label': '五月', 'value': '05'},
                        {'label': '六月', 'value': '06'},
                        {'label': '七月', 'value': '07'},
                        {'label': '八月', 'value': '08'},
                        {'label': '九月', 'value': '09'},
                        {'label': '十月', 'value': '10'},
                        {'label': '十一月', 'value': '11'},
                        {'label': '十二月', 'value': '12'}
                    ],
                    value='01', id='month_to', style={'width': '30%', 'display': 'inline-block'}
                )
            ], style={'width': '50%', 'display': 'inline-block'})

        ], style={'margin': '20px'}),
        html.Hr(style={'borderWidth': "1px", "width": "100%",
                "borderColor": "#e7f5d0"}),
    ], style={'color': '#83A742'}),
    html.Div([
        html.Div([
            html.U(children='每月文章篇數', style={
                'font-weight': 'bold', 'font-size': '28px', 'textAlign': 'left', "color": '#36451a'}),
            dcc.Graph(id='line-chart'),
        ], style={'width': '48%', 'display': 'inline-block', 'border-right': '1px solid #83A742', 'border-left': '10px solid white'}),
        html.Div([
            html.U(children='每月文章比重', style={
                'font-weight': 'bold', 'font-size': '28px', 'textAlign': 'left', "color": '#36451a'}),
            dcc.Graph(id='percentage'),], style={'width': '48%', 'display': 'inline-block', 'border-left': '9px solid white'})
    ], style={'margin': '20px'})
])


@app.callback(
    Output('month_from', 'options'),
    Input('year_from', 'value')
)
def update_month_to_options(selected_year):
    if selected_year == '2023':
        return [
            {'label': '一月', 'value': '01'},
            {'label': '二月', 'value': '02'},
            {'label': '三月', 'value': '03'},
            {'label': '四月', 'value': '04'},
            {'label': '五月', 'value': '05'},
            {'label': '六月', 'value': '06'},
            {'label': '七月', 'value': '07'},
            {'label': '八月', 'value': '08'}
        ]
    else:
        return [
            {'label': '一月', 'value': '01'},
            {'label': '二月', 'value': '02'},
            {'label': '三月', 'value': '03'},
            {'label': '四月', 'value': '04'},
            {'label': '五月', 'value': '05'},
            {'label': '六月', 'value': '06'},
            {'label': '七月', 'value': '07'},
            {'label': '八月', 'value': '08'},
            {'label': '九月', 'value': '09'},
            {'label': '十月', 'value': '10'},
            {'label': '十一月', 'value': '11'},
            {'label': '十二月', 'value': '12'}
        ]


@app.callback(
    Output('month_to', 'options'),
    Output('month_to', 'value'),
    Input('year_to', 'value')
)
def update_month_to_options(selected_year):
    if selected_year == '2023':
        options = [
            {'label': '一月', 'value': '01'},
            {'label': '二月', 'value': '02'},
            {'label': '三月', 'value': '03'},
            {'label': '四月', 'value': '04'},
            {'label': '五月', 'value': '05'},
            {'label': '六月', 'value': '06'},
            {'label': '七月', 'value': '07'},
            {'label': '八月', 'value': '08'}
        ]
        value = '04'  # Set value to None by default if no option is selected
    elif selected_year == '2017':
        options = [
            {'label': '三月', 'value': '03'},
            {'label': '四月', 'value': '04'},
            {'label': '五月', 'value': '05'},
            {'label': '六月', 'value': '06'},
            {'label': '七月', 'value': '07'},
            {'label': '八月', 'value': '08'},
            {'label': '九月', 'value': '09'},
            {'label': '十月', 'value': '10'},
            {'label': '十一月', 'value': '11'},
            {'label': '十二月', 'value': '12'}
        ]
        value = '03'  # Set value to '03' if selected_year is '2017'
    else:
        options = [
            {'label': '一月', 'value': '01'},
            {'label': '二月', 'value': '02'},
            {'label': '三月', 'value': '03'},
            {'label': '四月', 'value': '04'},
            {'label': '五月', 'value': '05'},
            {'label': '六月', 'value': '06'},
            {'label': '七月', 'value': '07'},
            {'label': '八月', 'value': '08'},
            {'label': '九月', 'value': '09'},
            {'label': '十月', 'value': '10'},
            {'label': '十一月', 'value': '11'},
            {'label': '十二月', 'value': '12'}
        ]
        value = '06'  # Set value to None by default if no option is selected

    return options, value


@app.callback(
    Output('line-chart', 'figure'),
    Output('percentage', 'figure'),
    Input('inputLabel', 'value'),
    Input('year_from', 'value'),
    Input('month_from', 'value'),
    Input('year_to', 'value'),
    Input('month_to', 'value'),
    Input('K', 'value')
)
def update_output(label, yf, mf, yt, mt, k):
    # begin: the begining month
    begin = (yf+'-'+mf)
    # end: the ending month
    end = (yt+'-'+mt)
    # select dtm by the label we input than get the specific period data
    dtm0 = dtm.loc[dtm['label'] == label].loc[:, begin:end]
    # add a colomn named keywords
    dtm0['keywords'] = dtm.loc[dtm['label'] == label]['keywords']
    # add a column which is the total sum for the keyword in the period
    dtm0['period'] = dtm0.loc[:, begin:end].sum(axis=1)
    # ranking dtm0 by period
    dtm0 = dtm0.sort_values(by='period',  ascending=False)

    # dtm1 is a dtm for the keyword percentage per month
    dtm1 = dtm0.loc[:, begin:end]

    for col in dtm1.columns:
        col_sum = dtm1[col].sum()  # Calculate the sum of the column
        # percentage <- value = value/ sum of the column
        dtm1[col] = (dtm1[col] / col_sum)*100

    # select the keyword in the k interval
    selected_keywords = dtm0['keywords'][k[0]-1:k[1]]
    data = []
    data1 = []
    for keyword in selected_keywords:
        # dtm0.columns[:-2] all column names expect the last two
        y_values = dtm0[dtm0['keywords'] == keyword][list(
            dtm0.columns[:-2])].values.flatten().tolist()

        y_values1 = dtm1[dtm0['keywords'] == keyword][list(
            dtm1.columns)].values.flatten().tolist()
        data.append(
            {'x': list(dtm0.columns[:-2]), 'y': y_values, 'type': 'line', 'name': keyword})
        data1.append(
            {'x': list(dtm1.columns), 'y': y_values1, 'type': 'line', 'name': keyword})
    layout = {
        'title': 'Line Chart of Keyword Counts per Month',
        'xaxis': {'title': 'Months', 'tickformat': "%b\n%Y"},
        'yaxis': {'title': 'Counts'},

    }
    layout1 = {
        'title': 'Line Chart of Keyword percentage per Month',
        'xaxis': {'title': 'Months', 'tickformat': "%b\n%Y"},
        'yaxis': {'title': '%'},
    }
    figure0 = {'data': data, 'layout': layout}
    figure1 = {'data': data1, 'layout': layout1}
    return (figure0, figure1)


if __name__ == '__main__':
    app.run(debug=True)
