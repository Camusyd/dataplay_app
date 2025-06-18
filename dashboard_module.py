from shiny import ui, render, reactive
from shinywidgets import output_widget, render_widget
import plotly.express as px
import pandas as pd

# Define panel_dashboard (interfaz) y server_dashboard (lógica) aquí
def panel_dashboard():
    return ui.page_fluid(
        ui.h2("Demo Interactiva – Dashboard"),
        ui.output_table("tabla_ejemplo"),
        output_widget("grafico_ejemplo")
    )

def server_dashboard(input, output, session):
    @output
    @render.table
    def tabla_ejemplo():
        df = pd.DataFrame({
            "Jugador": ["Jugador 1", "Jugador 2"],
            "Puntos": [25, 18]
        })
        return df

    @output
    @render_widget
    def grafico_ejemplo():
        df = pd.DataFrame({
            "Jugador": ["Jugador 1", "Jugador 2"],
            "Puntos": [25, 18]
        })
        return px.bar(df, x="Jugador", y="Puntos", title="Puntos por Jugador")




