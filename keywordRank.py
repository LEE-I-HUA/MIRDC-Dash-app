from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.graph_objects as go

dtm = pd.read_csv('freq_DTM.csv')

# segment labels by colours
colour = ["#CA774B", "#CC5F5A", "#66828E", "#FEC37D", "#678F74", "#D4C3AA"]
E_class = ["term", "loc", "com", "rocket", "satellite", "org"]
dtm['colour'] = dtm['label']
for i in range(0, len(E_class)):
    dtm['colour'] = dtm['colour'].replace({E_class[i]: colour[i]})


def number_to_words(n):
    number_words = {
        1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
        6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
        11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen',
        15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen',
        19: 'nineteen', 20: 'twenty', 30: 'thirty', 40: 'forty',
        50: 'fifty', 60: 'sixty', 70: 'seventy', 80: 'eighty'
    }

    if n in number_words:
        return number_words[n]
    elif n < 100:
        tens = n // 10 * 10
        ones = n % 10
        return number_words[tens] + number_words[ones]
    else:
        return 'Number out of range'


app = Dash(__name__)
app.layout = html.Div([
    html.H1(children='國防 SpaceNews 關鍵字詞頻率排名', style={'textAlign': 'center'}),
    html.Div([
        html.Div([
            html.Div(" ", style={
                 'background-color': "#CA774B", 'padding': '5px', 'color': 'white', 'display': 'inline-block', 'width': '16%'}),
            html.Div(" ", style={
                'background-color': "#CC5F5A", 'padding': '5px', 'color': 'white', 'display': 'inline-block', 'width': '16%'}),
            html.Div(" ", style={
                'background-color': "#66828E", 'padding': '5px', 'color': 'white', 'display': 'inline-block', 'width': '16%'}),
            html.Div(" ", style={
                'background-color': "#FEC37D", 'padding': '5px', 'color': 'white', 'display': 'inline-block', 'width': '16%'}),
            html.Div(" ", style={
                'background-color': "#678F74", 'padding': '5px', 'color': 'white', 'display': 'inline-block', 'width': '16%'}),
            html.Div(" ", style={
                'background-color': "#D4C3AA", 'padding': '5px', 'color': 'white', 'display': 'inline-block', 'width': '16%'}),
        ], style={'text-align': 'center'}),
    ]),
    html.H3(children='選擇關鍵字排名區間', style={'textAlign': 'left'}),
    dcc.RangeSlider(min=1, max=50, step=1, value=[1, 5], tooltip={
        "placement": "bottom", "always_visible": True}, id='K'),
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
            value='01', id='month_from', style={'width': '30%', 'display': 'inline-block', }
        ),], style={'padding': '20px'}),
    html.Div([

        html.Div([
            html.Div("term", style={
                 'background-color': "#CA774B", 'padding': '20px', 'color': 'white', 'display': 'inline-block', 'width': '12%'}),
            html.Div("loc", style={
                'background-color': "#CC5F5A", 'padding': '20px', 'color': 'white', 'display': 'inline-block', 'width': '12%'}),
            html.Div("com", style={
                'background-color': "#66828E", 'padding': '20px', 'color': 'white', 'display': 'inline-block', 'width': '12%'}),
            html.Div("rocket", style={
                'background-color': "#FEC37D", 'padding': '20px', 'color': 'white', 'display': 'inline-block', 'width': '12%'}),
            html.Div("satellite", style={
                'background-color': "#678F74", 'padding': '20px', 'color': 'white', 'display': 'inline-block', 'width': '12%'}),
            html.Div("org", style={
                'background-color': "#D4C3AA", 'padding': '20px', 'color': 'white', 'display': 'inline-block', 'width': '12%'}),
        ], style={'text-align': 'center'}),
        html.Div([dcc.Loading(dcc.Graph(id="graph"), type="cube")],
                 ),
    ]),


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
    Output('graph', 'figure'),
    Input('K', 'value'),
    Input('year_from', 'value'),
    Input('month_from', 'value'),
)
def display_animated_graph(K, yf, mf):
    begin = (yf+'-'+mf)
    # get all unique months
    months = dtm.columns.values.flatten().tolist()[2:]
    # make my dict_key from 'one' to the length of my months
    dict_keys = [number_to_words(i) for i in range(1, len(months))]

    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Year:",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 300, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []
    }

    # make the dict fn
    fn = {}
    for m, d in zip(months, dict_keys):
        # create a dataframe filter out the qualified range
        df = dtm.nlargest(n=K[1], columns=[m])[['keywords', 'colour', m]]
        df = df[K[0]-1:]
        # Melt the DataFrame to reshape it
        df_melted = pd.melt(
            df, id_vars=['keywords', 'colour'], var_name='months', value_name='count')
        # Sort the DataFrame by keywords and months
        df_melted = df_melted.sort_values(by=['months', 'count'])
        fn[d] = df_melted
        slider_step = {"args": [
            [m],
            {"frame": {"duration": 300, "redraw": False},
             "mode": "immediate",
             "transition": {"duration": 300}}
        ],
            "label": m,
            "method": "animate"}
        sliders_dict["steps"].append(slider_step)

    fig1 = go.Figure(
        data=[
            go.Bar(
                # For a horizontal bar char, use the px.bar function with orientation='h'.
                x=fn[dict_keys[months.index(begin)]]['count'],
                y=fn[dict_keys[months.index(begin)]]['keywords'],
                orientation='h',
                # text <- annotations, texttemplate<- formate of text
                text=fn[dict_keys[months.index(
                    begin)]]['count'], texttemplate='%{text:.3s}',
                textfont={'size': 18}, textposition='inside', insidetextanchor='middle',
                width=0.9, marker={'color': fn[dict_keys[months.index(begin)]]['colour']})
        ],
        layout=go.Layout(
            xaxis=dict(range=[0, 500], autorange=False,
                       title=dict(text='count', font=dict(size=18))),
            yaxis=dict(range=[-1, K[1]-K[0]+1], autorange=False,
                       tickfont=dict(size=14)),
            title=dict(text='Amounts apear per month:' + begin,
                       font=dict(size=28), x=0.5, xanchor='center'),
            # Add button
            updatemenus=[
                {
                    "buttons": [
                        {
                            "args": [None, {"frame": {"duration": 500, "redraw": False},
                                            "fromcurrent": True, "transition": {"duration": 300,
                                                                                "easing": "quadratic-in-out"}}],
                            "label": "Play",
                            "method": "animate"
                        },
                        {
                            "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                              "mode": "immediate",
                                              "transition": {"duration": 0}}],
                            "label": "Pause",
                            "method": "animate"
                        }
                    ],
                    "direction": "left",
                    "pad": {"r": 10, "t": 87},
                    "showactive": False,
                    "type": "buttons",
                    "x": 0.1,
                    "xanchor": "right",
                    "y": 0,
                    "yanchor": "top"
                }

            ],
            sliders=[sliders_dict]
        ),

        frames=[
            go.Frame(
                data=[
                    go.Bar(x=value['count'], y=value['keywords'],
                           orientation='h', text=value['count'],
                           marker={'color': value['colour']})
                ],
                layout=go.Layout(
                    xaxis=dict(range=[0, 500], autorange=False),
                    yaxis=dict(range=[-1, K[1]-K[0]+1],
                               autorange=False, tickfont=dict(size=14)),
                    title=dict(text='Amounts apear per month:' + value['months'].values[0],
                               font=dict(size=28))
                )
            )
            for key, value in fn.items()
        ]
    )
    return fig1


if __name__ == '__main__':
    app.run(debug=True)
