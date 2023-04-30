from dash import Dash, html, dash_table, dcc, Input, Output, State
import pandas as pd
from mysql_utils import (get_universities, get_faculty_names, get_faculty_info_position, get_faculty_info_email, 
                         get_faculty_info_interst, get_faculty_info_phone, get_faculty_info_photo, get_faculty_rank_keyword,
                         get_publications, keywords_by_year, add_faculty, get_keywords, get_uID_from_uName,
                         get_count_faculty, remove_faculty, add_trigger_faculty, add_fac_keyword_score_view,
                         add_uni_index, fac_uID_null, get_fac_from_view, get_fac_keyword_scores, get_all_pubs,
                         add_keyword)
from mongodb_utils import *
from neo4j_utils import *
import plotly_express as px


try:
    add_trigger_faculty()
except:
    print("Trigger alreayd added")

try:
    add_fac_keyword_score_view()
except:
    print('View already added')

try:
    add_uni_index()
except:
    print('index already added')

try:
    fac_uID_null()
except:
    print('constraint already added')


app = Dash(__name__)

app.layout = html.Div([
    html.Title('Dashboard to Rule the Academic World'),
    html.H1('Dashboard to Rule the Academic World', style={'font-size':'60px', 'color':'red'}),
    html.Div([

        html.Div([
            html.H3('Faculty Information', style={'text-align': 'center'}),
            dcc.Dropdown(get_universities(), id='university-dropdown', placeholder='Select University'),

            dcc.Dropdown(id='faculty-dropdown', placeholder='Select Faculty'),
            
            html.Div([
                html.Div(id='faculty-info'),
                    html.P(id='fac-display-name'),
                    html.Div([
                        html.P("Faculty Name: "),
                        html.P('Faculty Position: '),
                        html.P('Faculty Phone:'),
                        html.P('Faculty Email:'),
                        html.P('Faculty Research Interest:'),
                        html.P('Faculty Photo:')
                    ], id='fac-display-position'),

            ], style={'padding-left':'20px', 'padding-right': '20px', 'padding-top':'20px', 'padding-bottom': '20px', 'width':'300px', 'height':'500px'})
        ], style={'display':'inline-block', 'padding-top':'0px', 'float':'left',
                   'vetical-align':'middle', 'border-style':'solid', 'border-radius':'20px'}),

        html.Div([
            html.H3('Number of Publications Each Year by Keyword For a University'),
            dcc.Dropdown(options=get_keywords(), id='keyword-graph-dropdown', placeholder='Select Keyword'),
            dcc.Dropdown(options=get_universities(), id='keyword-university-dropdown', placeholder='Select University'),

            html.H2('Publications by Year', style={'text-align': 'center'}),
            dcc.Graph(figure={},id='keyword-year-graph')

        ], style={'display':'inline-block','padding-left': '10px','padding-right':'10px', 'float': 'left', 'vetical-align':'middle',
                  'border-style':'solid', 'border-radius':'20px'}),
        
        html.Div([
            html.Div([
                html.H3('Enter or Remove a New Faculty Member'),
                dcc.Input(id='input-faculty-university', placeholder='Enter Faculty University'),
                dcc.Input(id='input-faculty-name', placeholder='Enter Faculty Name'),
                dcc.Input(id='input-faculty-position', placeholder='Enter Faculty Position'),
                dcc.Input(id='input-faculty-interest', placeholder='Enter Faculty Research Interest'),
                dcc.Input(id='input-faculty-email', placeholder='Enter Faculty Email'),
                dcc.Input(id='input-faculty-phone', placeholder='Enter Faculty Phone'),
                dcc.Input(id='input-faculty-photoURL', placeholder='Enter Faculty Photo URL'),
                html.Button('Add Faculty', id='button-faculty', style= {'background': 'black', 'color':'white'}),
                html.Button('Remove Faculty', id='button-remove-faculty'),
                html.P(id='added-faculty-message', style={'text-align':'center'}),
                html.P(id='removed-faculty-message', style={'text-align':'center'})
        ], style={'display':'grid','border-style':'solid', 'border-radius':'20px', 'height':'350px'}),
            html.Div([
                html.H3('Add a Keyword to a Publication'),
                dcc.Dropdown(get_all_pubs(), id='add-keyword-pub-dropdown', placeholder='Select Publication'),
                dcc.Dropdown(get_keywords(), id='add-keyword-dropdown', placeholder='Select Keyword to add'),
                dcc.Input(id='add-keyword-score', placeholder='Add Score (if avaliable)'),
                html.Button('Add Keyword', id='add-keyword-button'),
                html.P(id='keyword-added-message')       
            ], style={'display':'grid', 'border-style':'solid', 'border-radius':'20px', 'height':'250px'})

    ], style = {'display':'grid', 'border-style':'hidden', 'height':'600px'})

    ], style = {'display':'block', 'padding-bottom':'40px', 'text-align':'left', 'border-style':'hidden'}),

    html.Div([
        html.Div([
            html.H2('Get Publications By Faculty'),
            dcc.Dropdown(get_unis_neo4j(), id='university-pub-dropdown', placeholder='Select University'),
            dcc.Dropdown(id='faculty-pub-dropdown', placeholder='Select Faculty'),

            html.Div([
                html.Label("Publications"),
                html.Div(id='faculty-pub-data-table')
            ])],style={'display':'grid'})],
                style={'text-align':'left', 'display':'grid', 'height': '600px', 'border-style':'solid', 'border-radius':'20px'}),
     html.Div([
        html.Div([
            html.H3('Compare Keywords Scores For Faculty'),
            dcc.Dropdown(get_fac_from_view(), placeholder='Select Faculty', id='fac-view-dropdown'),

            html.H2('Keyword Scores', style={'text-align': 'center'}),
            dcc.Graph(figure={},id='keyword-score-graph')], 
        style = {'display':'grid','border-style':'solid', 'border-radius':'20px',
                 'height':'600px', 'width':'45%', 'float':'left' }),

        html.Div([
            html.H3('Total Count of Publications For Keywords By Year'),
            dcc.Dropdown(get_keywords_monogo(), id='keyword-year-graph-mongo-drowdown', placeholder='Select Keyword'),

            html.H2('Keyword Publications Per Year', style={'text-align': 'center'}),
            dcc.Graph(figure={}, id='keyword-year-mongo-graph')],
            style = {'display':'grid','border-style':'solid', 'border-radius':'20px',
                 'height':'600px', 'width':'45%', 'float':'left' })         
    ], style = {'display':'block', 'border-style':'hidden','text-align':'center'})


    
], style={'text-align':'center', 'display':'grid'})

@app.callback(
    Output('faculty-dropdown', 'options'),
    Input('university-dropdown', 'value'),
    prevent_initial_call = True
)

def update_fac_info_dropdown(value):
    return get_faculty_names(value)

@app.callback(
        Output(component_id='fac-display-name', component_property='children'),
        Input(component_id='faculty-dropdown', component_property='value'),
        prevent_initial_call=True
)

def update_fac_info_name(value):
    return ['Faculty name: ' + value]

@app.callback(
        Output(component_id='fac-display-position', component_property='children'),
        Input(component_id='faculty-dropdown', component_property='value'),
        prevent_initial_call = True
)

def update_fac_info_position(value):
    position = get_faculty_info_position(value)
    phone = get_faculty_info_phone(value)
    email = get_faculty_info_email(value)
    interest = get_faculty_info_interst(value)
    photo_url = get_faculty_info_photo(value)
    return (
        html.P('Position: ' + position),
        html.P('Phone: ' + phone),
        html.P('Email: ' + email),
        html.P('Research Interest: ' + interest),
        html.P('Faculty Photo: '),
        html.Img(src=photo_url)

    )


@app.callback(
    Output(component_id='keyword-year-graph', component_property='figure'),
    Input(component_id='keyword-graph-dropdown', component_property='value'),
    Input(component_id='keyword-university-dropdown', component_property='value'),
    prevent_initial_call = True
)
def keywords_year_graph(keyword, uni):
    result = keywords_by_year(uni, keyword)
    df = pd.DataFrame.from_dict(result)
    fig = px.bar(df, x='year', y='count', labels={'year':'Year', 'count':'Number of Publications'},text_auto=True)
    return fig

@app.callback(
    Output(component_id='added-faculty-message', component_property='children'),
    [Input(component_id='button-faculty', component_property='n_clicks'),
    State(component_id='input-faculty-university', component_property='value'),
    State(component_id='input-faculty-name', component_property='value'),
    State(component_id='input-faculty-position', component_property='value'),
    State(component_id='input-faculty-interest', component_property='value'),
    State(component_id='input-faculty-email', component_property='value'),
    State(component_id='input-faculty-phone', component_property='value'),
    State(component_id='input-faculty-photoURL', component_property='value')],
    prevent_initial_call=True
)
def add_facutlty_call(click, u_name, f_name, f_position, f_interest, f_email, f_phone, f_photoURL):
    if u_name is None:
        if f_name is None:
            return ['Please enter the name of the university and the name of the faculty']
        else:
            return['Please enter the name of the University']
    if f_name is None:
        return ['Please enter the name of the faculty']
    if f_position is None:
        f_position = 'NULL'
    else:
        f_position = '"'+ f_position + '"'
    if f_interest is None:
        f_interest = 'NULL'
    else:
        f_interest = '"'+ f_interest + '"'
    if f_email is None:
        f_email = 'NULL'
    else:
        f_email = '"' + f_email + '"'
    if f_phone is None:
        f_phone = 'NULL'
    else:
        f_phone = '"' + f_phone + '"'
    if f_photoURL is None:
        f_photoURL = 'NULL'
    else:
        f_photoURL = '"' + f_photoURL + '"'
    count_fac = get_count_faculty()
    f_id = str(count_fac + 1)
    a = add_faculty(u_name, f_id, f_name, f_position, f_interest, f_email, f_phone, f_photoURL)
    if a == 'error':
        return ['Could not add faculty: University does not exist']
    else:
        return ['Added faculty member: ' + f_name + ' to the database']


@app.callback(
    Output(component_id='removed-faculty-message', component_property='children'),
    [Input(component_id='button-remove-faculty', component_property='n_clicks'),
    State(component_id='input-faculty-university', component_property='value'),
    State(component_id='input-faculty-name', component_property='value'),
    State(component_id='input-faculty-position', component_property='value'),
    State(component_id='input-faculty-interest', component_property='value'),
    State(component_id='input-faculty-email', component_property='value'),
    State(component_id='input-faculty-phone', component_property='value'),
    State(component_id='input-faculty-photoURL', component_property='value')],
    prevent_initial_call=True
)
def remove_faculty_call(click, u_name, f_name, f_position, f_interest, f_email, f_phone, f_photoURL):
    if u_name is None:
        if f_name is None:
            return ['Please enter the name of the university and the name of the faculty']
        else:
            return['Please enter the name of the University']
    if f_name is None:
        return ['Please enter the name of the faculty']
    u_id = str(get_uID_from_uName(u_name))
    if u_id == 'not found':
        return ['University is not in the system']
    remove_faculty(u_id, f_name)
    return [f_name + ' was removed from the database']

@app.callback(
    Output(component_id='faculty-pub-dropdown', component_property='options'),
    Input(component_id='university-pub-dropdown', component_property='value'),
    prevent_inital_call=True
)

def update_pub_faculty(value):
    return get_faculty_neo4j(value)


@app.callback(
    Output(component_id='faculty-pub-data-table', component_property='children'),
    Input(component_id='faculty-pub-dropdown', component_property='value'),
    Input(component_id='university-pub-dropdown', component_property='value'),
    prevent_inital_call=True
)

def update_table(fac, uni):
    df = get_fac_publications_neo4j(fac, uni)
    data = df.to_dict('records')
    columns = [{"name": i, "id": i,} for i in (df.columns)]
    return dash_table.DataTable(data = data, columns=columns, page_size=10, style_table={'overflowX': 'auto'},
                                 style_data={'backgroundColor': 'rgb(0,0,255)', 'color':'white'},
                                style_cell={'width':'100px', 'maxWidth':'100px','overflow': 'hidden', 'textOverflow': 'ellipsis',})

@app.callback(
    Output(component_id='keyword-score-graph', component_property='figure'),
    Input(component_id='fac-view-dropdown', component_property='value'),
    prevent_initial_call = True
)

def get_score_graph(value):
    result = get_fac_keyword_scores(value)
    df = pd.DataFrame.from_dict(result)
    fig = px.pie(df, values='score', names='keyword')
    return fig

@app.callback(
    Output(component_id='keyword-added-message', component_property='children'),
    [Input(component_id='add-keyword-button', component_property='n_clicks'),
     State(component_id='add-keyword-pub-dropdown', component_property='value'),
     State(component_id='add-keyword-dropdown', component_property='value'),
     State(component_id='add-keyword-score', component_property='value')],
    prevent_initial_call = True
)

def update_keyword(clicks, title, keyword, score):
    if title is None or keyword is None:
        return ["Select items to add"]
    if score is None:
        score = 'NULL'
    add_keyword(title, keyword, score)
    return ['"' + keyword + '"' + ' was added to ' + '"' + title + '"']

@app.callback(
    Output(component_id='keyword-year-mongo-graph', component_property='figure'),
    Input(component_id='keyword-year-graph-mongo-drowdown', component_property='value'),
    prevent_initial_call = True
)

def get_keyword_mongo_graph(value):
    result = keyword_per_year_mongo(value)
    df = pd.DataFrame.from_dict(result)
    fig = px.line(df, x='year', y='count', markers=True)
    return fig


if __name__ == '__main__':
    app.run_server()