import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamplayerdashboard
import dash
from dash import html, dcc, Input, Output, State, ctx
import plotly.express as px
from dash import dash_table
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import uuid
import os

# --- Datos base ---
nba_teams = teams.get_teams()
denver_nuggets = [team for team in nba_teams if team['full_name'] == 'Denver Nuggets'][0]
team_id = denver_nuggets['id']
season = '2022-23'

def cargar_datos(season_type):
    df = teamplayerdashboard.TeamPlayerDashboard(
        team_id=team_id,
        season=season,
        season_type_all_star=season_type
    ).get_data_frames()[1]
    df['EFFICIENCY'] = (df['PTS'] + df['REB'] + df['AST'] + df['STL'] + df['BLK']
                        - (df['FGA'] - df['FGM']) - df['TOV'])
    return df

regular_df = cargar_datos("Regular Season")
playoffs_df = cargar_datos("Playoffs")
posiciones = ['G', 'F', 'C', 'F-C', 'G-F']

# --- App Dash ---
app = dash.Dash(__name__)
app.title = 'Dashboard Denver Nuggets 2022-23'

app.layout = html.Div(style={'backgroundColor': '#121212', 'color': '#FFFFFF', 'padding': '1rem', 'fontFamily': 'Montserrat'}, children=[
    html.H1("Dashboard Analítico - Denver Nuggets 2022-23", style={'textAlign': 'center', 'color': '#00FFFF'}),

    html.Div([
        html.Label('Temporada:', style={'marginRight': '1rem'}),
        dcc.Dropdown(
            id='season-selector',
            options=[
                {'label': 'Temporada Regular', 'value': 'Regular'},
                {'label': 'Playoffs', 'value': 'Playoffs'}
            ],
            value='Regular',
            style={'width': '200px', 'color': '#000'}
        ),
        html.Label('Posición:', style={'marginLeft': '2rem', 'marginRight': '1rem'}),
        dcc.Dropdown(
            id='position-filter',
            options=[{'label': pos, 'value': pos} for pos in posiciones],
            multi=True,
            placeholder="Filtrar por posición...",
            style={'width': '200px', 'color': '#000'}
        ),
    ], style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '2rem'}),

    dcc.Graph(id='bar-efficiency'),
    dcc.Graph(id='scatter-points-vs-assists'),
    dcc.Graph(id='bar-points'),
    dcc.Graph(id='bar-rebounds'),
    dcc.Graph(id='bar-steals'),
    dcc.Graph(id='bar-threes'),

    html.Div(id='tabla-jugadores'),

    html.Div(style={'textAlign': 'center', 'marginTop': '2rem'}, children=[
        html.Button("Descargar CSV", id='btn_csv', n_clicks=0, style={'marginRight': '1rem'}),
        html.Button("Generar Informe PDF", id='btn_pdf', n_clicks=0)
    ]),

    dcc.Download(id="download_csv"),
    dcc.Download(id="download_pdf")
])

# --- Callbacks ---
@app.callback(
    Output('tabla-jugadores', 'children'),
    Output('bar-efficiency', 'figure'),
    Output('scatter-points-vs-assists', 'figure'),
    Output('bar-points', 'figure'),
    Output('bar-rebounds', 'figure'),
    Output('bar-steals', 'figure'),
    Output('bar-threes', 'figure'),
    Input('season-selector', 'value'),
    Input('position-filter', 'value')
)
def actualizar_dashboard(season_type, posiciones_seleccionadas):
    df = regular_df if season_type == 'Regular' else playoffs_df

    if posiciones_seleccionadas:
        df = df[df['PLAYER_POSITION'].isin(posiciones_seleccionadas)]

    df = df.sort_values('EFFICIENCY', ascending=False)

    # Tabla
    tabla = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in ['PLAYER_NAME', 'PLAYER_POSITION', 'PTS', 'AST', 'REB', 'EFFICIENCY']],
        data=df.to_dict('records'),
        style_table={'overflowX': 'auto', 'backgroundColor': '#1E1E1E'},
        style_cell={'color': '#FFFFFF', 'backgroundColor': '#1E1E1E', 'textAlign': 'center'},
        style_header={'backgroundColor': '#00FFFF', 'color': 'black', 'fontWeight': 'bold'}
    )

    fig_eff = px.bar(df, x='PLAYER_NAME', y='EFFICIENCY', color='EFFICIENCY',
                     title="Eficiencia por Jugador", color_continuous_scale='Viridis')

    fig_scatter = px.scatter(df, x='AST', y='PTS', color='PLAYER_NAME', size='EFFICIENCY',
                             title="Asistencias vs Puntos", hover_name='PLAYER_NAME')

    fig_pts = px.bar(df.sort_values('PTS', ascending=False), x='PLAYER_NAME', y='PTS',
                     title='Puntos por Jugador', color='PTS', color_continuous_scale='Plasma')

    fig_reb = px.bar(df.sort_values('REB', ascending=False), x='PLAYER_NAME', y='REB',
                     title='Rebotes por Jugador', color='REB', color_continuous_scale='Tealgrn')

    fig_stl = px.bar(df.sort_values('STL', ascending=False), x='PLAYER_NAME', y='STL',
                     title='Robos por Jugador', color='STL', color_continuous_scale='Blues')

    fig_threes = px.bar(df.sort_values('FG3M', ascending=False), x='PLAYER_NAME', y='FG3M',
                        title='Triples Encestados por Jugador', color='FG3M', color_continuous_scale='Cividis')

    return tabla, fig_eff, fig_scatter, fig_pts, fig_reb, fig_stl, fig_threes

@app.callback(
    Output("download_csv", "data"),
    Input("btn_csv", "n_clicks"),
    State('season-selector', 'value'),
    State('position-filter', 'value'),
    prevent_initial_call=True,
)
def descargar_csv(n_clicks, season_type, posiciones_seleccionadas):
    df = regular_df if season_type == 'Regular' else playoffs_df
    if posiciones_seleccionadas:
        df = df[df['PLAYER_POSITION'].isin(posiciones_seleccionadas)]
    return dcc.send_data_frame(df.to_csv, filename="jugadores_filtrados.csv", index=False)

@app.callback(
    Output("download_pdf", "data"),
    Input("btn_pdf", "n_clicks"),
    State('season-selector', 'value'),
    State('position-filter', 'value'),
    prevent_initial_call=True
)
def generar_pdf(n_clicks, season_type, posiciones_seleccionadas):
    df = regular_df if season_type == 'Regular' else playoffs_df
    if posiciones_seleccionadas:
        df = df[df['PLAYER_POSITION'].isin(posiciones_seleccionadas)]

    filename = f"reporte_{uuid.uuid4().hex[:8]}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, f"Informe Denver Nuggets - Temporada: {season_type}")

    y = 720
    for i, row in df[['PLAYER_NAME', 'PTS', 'REB', 'AST', 'EFFICIENCY']].iterrows():
        c.drawString(50, y, f"{row['PLAYER_NAME']}: PTS={row['PTS']}, REB={row['REB']}, AST={row['AST']}, EFF={row['EFFICIENCY']}")
        y -= 20
        if y < 50:
            c.showPage()
            y = 750

    c.save()

    with open(filename, "rb") as f:
        contenido = f.read()
    os.remove(filename)
    return dcc.send_bytes(contenido, filename="informe.pdf")

if __name__ == '__main__':
    app.run(debug=True)










    
    # python app.py
#streamlit run app.py




