from nba_api.stats.endpoints import teamplayerdashboard
from nba_api.stats.static import teams
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Obtener el ID del equipo Denver Nuggets
nba_teams = teams.get_teams()
denver_nuggets = [team for team in nba_teams if team['full_name'] == 'Denver Nuggets'][0]
team_id = denver_nuggets['id']

# Temporada campeón
season = '2022-23'

# Obtener datos temporada regular y playoffs
regular_df = teamplayerdashboard.TeamPlayerDashboard(
    team_id=team_id,
    season=season,
    season_type_all_star='Regular Season'
).get_data_frames()[1]

playoffs_df = teamplayerdashboard.TeamPlayerDashboard(
    team_id=team_id,
    season=season,
    season_type_all_star='Playoffs'
).get_data_frames()[1]

# Funciones de analítica avanzada
def calcular_eficiencia(df):
    df['EFFICIENCY'] = (df['PTS'] + df['REB'] + df['AST'] + df['STL'] + df['BLK']
                        - (df['FGA'] - df['FGM']) - df['TOV'])
    return df

regular_df = calcular_eficiencia(regular_df)
playoffs_df = calcular_eficiencia(playoffs_df)

# Crear la app Dash
app = dash.Dash(__name__)
app.title = 'Dashboard Avanzado Denver Nuggets 2022-23'

app.layout = html.Div([
    html.H1('Dashboard Avanzado - Denver Nuggets 2022-23', style={'textAlign': 'center'}),

    html.Div([
        html.Label('Selecciona el tipo de temporada:'),
        dcc.Dropdown(
            id='season-type',
            options=[
                {'label': 'Temporada Regular', 'value': 'Regular'},
                {'label': 'Playoffs', 'value': 'Playoffs'}
            ],
            value='Regular'
        )
    ], style={'width': '50%', 'margin': 'auto'}),

    dcc.Graph(id='efficiency-bar'),
    dcc.Graph(id='radar-stats'),
    dcc.Graph(id='scatter-points-assists'),
])

@app.callback(
    [Output('efficiency-bar', 'figure'),
     Output('radar-stats', 'figure'),
     Output('scatter-points-assists', 'figure')],
    [Input('season-type', 'value')]
)
def update_graphs(season_type):
    df = regular_df if season_type == 'Regular' else playoffs_df

    # Gráfico de eficiencia
    fig_eff = px.bar(df.sort_values('EFFICIENCY', ascending=False),
                     x='PLAYER_NAME', y='EFFICIENCY',
                     title='Eficiencia por Jugador', color='EFFICIENCY')

    # Gráfico tipo radar de rendimiento por jugador (usamos un jugador destacado por ejemplo)
    player_radar = df.sort_values('PTS', ascending=False).iloc[0]
    radar_stats = {
        'PTS': player_radar['PTS'],
        'REB': player_radar['REB'],
        'AST': player_radar['AST'],
        'STL': player_radar['STL'],
        'BLK': player_radar['BLK']
    }
    fig_radar = px.line_polar(r=pd.Series(radar_stats),
                               theta=list(radar_stats.keys()),
                               line_close=True,
                               title=f"Radar Stats: {player_radar['PLAYER_NAME']}")

    # Diagrama de dispersín puntos vs asistencias
    fig_scatter = px.scatter(df, x='AST', y='PTS', color='PLAYER_NAME',
                             size='EFFICIENCY',
                             title='Relación Puntos vs Asistencias',
                             hover_name='PLAYER_NAME')

    return fig_eff, fig_radar, fig_scatter

if __name__ == '__main__':
    app.run(debug=True)







