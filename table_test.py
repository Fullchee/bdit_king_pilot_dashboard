from collections import OrderedDict

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

df = pd.read_csv("data/test.csv")

def generate_cell_class(colNum):
    if colNum == 0:
        return 'segname'
    else:
        return 'segother'
    
def generate_row_class(selected_str, current_str):
    # if selected_str == current_str:
    if current_str == 'Queen':
        return 'selected';
    else:
        return 'notselected';

def generate_table(dataframe, street_name=None, max_rows=30):
    return html.Table(
        [
         html.Tr( [html.Td(""), html.Td("Eastbound",colSpan=2), html.Td("Westbound",colSpan=2)] )
        ] +
        [
         html.Tr( [html.Td(""), html.Td("After"), html.Td("Baseline"), html.Td("After"), html.Td("Baseline")] )
        ] +
        [html.Tr([
            html.Td(dataframe.iloc[i][col], id = (dataframe.iloc[i]['street'] + '_' + str(dataframe.columns.get_loc(col)+1)), className = generate_cell_class(dataframe.columns.get_loc(col))) for col in dataframe.columns
        ], id= dataframe.iloc[i]['street'], className = generate_row_class(street_name, dataframe.iloc[i]['street']), n_clicks=0) for i in range(min(len(dataframe), max_rows))]
        , id = 'data_table'
    )

app = dash.Dash()

app.layout = html.Div([
#        html.Div(children=[
#            html.H1(children='King Street Pilot'),
#            ], className='row twelve columns'),
        
        html.Div([    
            html.Div(children=[
                        html.Div(id='div-table', children=generate_table(df)),
                        html.Div(id='row-selected', children='Selected row')],
                    className='four columns'
                    ),
                html.Div(children=[
                        html.H2(children='Chart goes here')],
                    className='eight columns'
                    ),
            ], className = 'row')

        ])

#Super critical to store in an OrderedDict
#This is a bad implementation, should be changed to a hidden div, see: https://community.plot.ly/t/app-not-resetting-with-page-refresh/5020/10
#https://plot.ly/dash/sharing-data-between-callbacks
CLICKS = OrderedDict([(df.iloc[i]['street'], 0) for i in range(len(df))])

# updates table and chart - causes infinite loop currently
#@app.callback(Output('div-table', 'children'),
#              [Input('row-selected','children')] )
#def update_table(street_name):
#    table = generate_table(df, street_name)
#    return table;


@app.callback(Output('row-selected','children'),
              [Input(df.iloc[i]['street'], 'n_clicks') for i in range(len(df))] )
def button_click(*rows):
    global CLICKS
    state_clicked = ''
    n_clicks_clicked = 0
    for (state, n_click_old), n_click_new in zip(CLICKS.items(), rows):
        if n_click_new > n_click_old:
            state_clicked = state
            n_clicks_clicked = n_click_new
    
    CLICKS[state_clicked] = n_clicks_clicked
    return state_clicked

app.css.append_css({
    'external_url': 'https://cityoftoronto.github.io/bdit_king_pilot_dashboard/css/dashboard.css'
})
    
if __name__ == '__main__':
    app.run_server(debug=True)