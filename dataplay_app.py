from shiny import App, ui, render, reactive
import pandas as pd
import plotly.express as px
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.endpoints import leaguedashplayerstats
from datetime import datetime
from shinywidgets import output_widget, render_widget

# 📊 Obtener plantilla de Denver Nuggets
def cargar_roster():
    team_id = [team['id'] for team in teams.get_teams() if team['full_name'] == "Denver Nuggets"][0]
    df = commonteamroster.CommonTeamRoster(team_id=team_id, season="2022-23").get_data_frames()[0]

    def altura_metros(h):
        try:
            pies, pulgadas = map(int, h.split('-'))
            return round((pies * 12 + pulgadas) * 0.0254, 2)
        except:
            return None

    df["Altura (m)"] = df["HEIGHT"].apply(altura_metros)
    df["Peso (kg)"] = df["WEIGHT"].apply(lambda w: round(float(w) * 0.453592, 1) if pd.notna(w) else None)
    df["Nacimiento"] = pd.to_datetime(df["BIRTH_DATE"], errors='coerce').dt.strftime("%b %d, %Y").str.upper()
    df["Experiencia"] = df["EXP"].replace("R", 0).astype(int)
    df["Posición Simple"] = df["POSITION"].str.extract(r"([A-Z]+)")

    columnas = ["NUM", "PLAYER", "POSITION", "Altura (m)", "Peso (kg)", "Nacimiento", "Experiencia", "SCHOOL"]
    df = df[columnas]
    df.columns = ["N°", "Jugador", "Posición", "Altura (m)", "Peso (kg)", "Nacimiento", "Experiencia", "Universidad"]

    return df

# 🎯 Cargar estadísticas por temporada
def cargar_estadisticas(tipo):
    season = "2022-23"
    tipo_api = "Playoffs" if tipo == "Playoffs" else "Regular Season"
    stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        season_type_all_star=tipo_api,
        per_mode_detailed="PerGame"
    ).get_data_frames()[0]

    # Filtrar jugadores de Denver
    stats = stats[stats["TEAM_ABBREVIATION"] == "DEN"]

    columnas = {
        "PLAYER_NAME": "Jugador",
        "PTS": "Puntos",
        "AST": "Asistencias",
        "REB": "Rebotes",
        "STL": "Robos",
        "BLK": "Bloqueos",
        "FG_PCT": "% Campo",
        "FG3_PCT": "% Triples",
        "FT_PCT": "% TL"
    }

    df = stats[list(columnas.keys())].rename(columns=columnas)
    df = df.round(2)
    return df

# 🌐 Interfaz de usuario
app_ui = ui.page_fluid(
    ui.h2("🏀 Dashboard – Plantilla Denver Nuggets 2023"),
    ui.p("Análisis físico y técnico de los jugadores."),
    
    ui.layout_columns(
        ui.column(6,
            ui.output_table("tabla_roster")
        ),
        ui.column(6,
            ui.input_select("filtro_pos", "Filtrar por posición (opcional):", choices=["Todas"], selected="Todas"),
            output_widget("graf_altura"),
            output_widget("graf_peso"),
            output_widget("graf_exp")
        )
    ),

    ui.hr(),

    # 📊 Sección de estadísticas por jugador
ui.h2("📊 Estadísticas Individuales – Denver Nuggets"),
ui.input_radio_buttons("temporada_tipo", "Temporada:", ["Regular Season", "Playoffs"], selected="Regular Season"),
ui.output_table("tabla_estadisticas"),

# 📊 Gráficos 3x3 (barras horizontales)
ui.layout_columns(
    ui.column(4, output_widget("graf_puntos")),
    ui.column(4, output_widget("graf_asistencias")),
    ui.column(4, output_widget("graf_rebotes")),
    ui.column(4, output_widget("graf_robos")),
    ui.column(4, output_widget("graf_bloqueos")),
    ui.column(4, output_widget("graf_fg")),
    ui.column(4, output_widget("graf_fg3")),
    ui.column(4, output_widget("graf_ft")),
    ui.column(4)  # vacío para mantener 3 columnas simétricas
),

# 🎯 Gráfico resumen final
ui.hr(),
ui.h3("🎯 Impacto Ofensivo Global – Promedio Total por Jugador", class_="text-center"),
ui.layout_columns(
    ui.column(12, output_widget("graf_promedio"))
),
ui.hr(),
ui.p("© Proyecto de grado – 2025")

)



# 🔁 Lógica de la aplicación
def server(input, output, session):
    df_completo = cargar_roster()

    @reactive.Calc
    def datos_filtrados():
        if input.filtro_pos() == "Todas":
            return df_completo
        else:
            return df_completo[df_completo["Posición"] == input.filtro_pos()]

    @output
    @render.table
    def tabla_roster():
        return datos_filtrados()[["N°", "Jugador", "Posición", "Altura (m)", "Peso (kg)", "Nacimiento", "Experiencia", "Universidad"]]

    @output
    @render_widget
    def graf_altura():
        df = datos_filtrados()
        return px.histogram(df, x="Altura (m)", nbins=8, color="Posición",
                            title="Distribución de Altura", template="plotly_white", color_discrete_sequence=px.colors.sequential.Blues)

    @output
    @render_widget
    def graf_peso():
        df = datos_filtrados()
        return px.histogram(df, x="Peso (kg)", nbins=8, color="Posición",
                            title="Distribución de Peso", template="plotly_white", color_discrete_sequence=px.colors.sequential.Greens)

    @output
    @render_widget
    def graf_exp():
        df = datos_filtrados()
        return px.histogram(df, x="Experiencia", nbins=6, color="Posición",
                            title="Distribución de Experiencia", template="plotly_white", color_discrete_sequence=px.colors.sequential.Oranges)

    # Dinámicamente actualizamos el selector de posición
    @reactive.Effect
    def actualizar_opciones():
        posiciones = ["Todas"] + sorted(df_completo["Posición"].dropna().unique().tolist())
        ui.update_select("filtro_pos", choices=posiciones)

    # Estadísticas individuales
    @reactive.Calc
    def df_estadisticas():
        return cargar_estadisticas(input.temporada_tipo())

    @output
    @render.table
    def tabla_estadisticas():
        return df_estadisticas()

    @output
    @render_widget
    def graf_puntos():
        df = df_estadisticas().sort_values("Puntos", ascending=True).tail(5)
        fig = px.bar(df, y="Jugador", x="Puntos", orientation="h",
                 title="Top 5 – Puntos", color="Puntos", color_continuous_scale="reds")
        fig.update_layout(yaxis=dict(autorange="reversed"))
        return fig


    @output
    @render_widget
    def graf_asistencias():
        df = df_estadisticas().sort_values("Asistencias", ascending=True).tail(5)
        fig = px.bar(df, y="Jugador", x="Asistencias", orientation="h",
                 title="Top 5 – Asistencias", color="Asistencias", color_continuous_scale="blues")
        fig.update_layout(yaxis=dict(autorange="reversed"))
        return fig

    @output
    @render_widget
    def graf_rebotes():
        df = df_estadisticas().sort_values("Rebotes", ascending=True).tail(5)
        fig = px.bar(df, y="Jugador", x="Rebotes", orientation="h",
                 title="Top 5 – Rebotes", color="Rebotes", color_continuous_scale="greens")
        fig.update_layout(yaxis=dict(autorange="reversed"))
        return fig

    @output
    @render_widget
    def graf_robos():
        df = df_estadisticas().sort_values("Robos", ascending=True).tail(5)
        fig = px.bar(df, y="Jugador", x="Robos", orientation="h",
                     title="Top 5 – Robos", color="Robos", color_continuous_scale="teal")
        fig.update_layout(yaxis=dict(autorange="reversed"))
        return fig

    @output
    @render_widget
    def graf_bloqueos():
        df = df_estadisticas().sort_values("Bloqueos", ascending=True).tail(5)
        fig = px.bar(df, y="Jugador", x="Bloqueos", orientation="h",
                     title="Top 5 – Bloqueos", color="Bloqueos", color_continuous_scale="oranges")
        fig.update_layout(yaxis=dict(autorange="reversed"))
        return fig

    @output
    @render_widget
    def graf_fg():
        df = df_estadisticas().sort_values("% Campo", ascending=True).tail(5)
        fig = px.bar(df, y="Jugador", x="% Campo", orientation="h",
                     title="Top 5 – % Campo", color="% Campo", color_continuous_scale="purples")
        fig.update_layout(yaxis=dict(autorange="reversed"))
        return fig

    @output
    @render_widget
    def graf_fg3():
        df = df_estadisticas().sort_values("% Triples", ascending=True).tail(5)
        fig = px.bar(df, y="Jugador", x="% Triples", orientation="h",
                     title="Top 5 – % Triples", color="% Triples", color_continuous_scale="magenta")
        fig.update_layout(yaxis=dict(autorange="reversed"))
        return fig

    @output
    @render_widget
    def graf_ft():
        df = df_estadisticas().sort_values("% TL", ascending=True).tail(5)
        fig = px.bar(df, y="Jugador", x="% TL", orientation="h",
                     title="Top 5 – % TL", color="% TL", color_continuous_scale="cividis")
        fig.update_layout(yaxis=dict(autorange="reversed"))
        return fig

    @output
    @render_widget
    def graf_promedio():
        df = df_estadisticas().copy()
        df["Promedio Total"] = df[["Puntos", "Asistencias", "Rebotes", "Robos", "Bloqueos", "% Campo", "% Triples", "% TL"]].mean(axis=1)
        df = df.sort_values("Promedio Total", ascending=True).tail(5)
        fig = px.bar(df, y="Jugador", x="Promedio Total", orientation="h",
                     title="🏆 Promedio de Impacto Ofensivo", color="Promedio Total",
                     color_continuous_scale="Plasma", height=500)
        fig.update_layout(yaxis=dict(autorange="reversed"))
        return fig



        

# 🚀 Ejecutar aplicación
app = App(app_ui, server)



# shiny run --reload dataplay_app.py