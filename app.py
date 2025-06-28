import streamlit as st
import pandas as pd
import plotly.express as px
from nba_api.stats.endpoints import leaguedashplayerstats
from datetime import datetime
from io import BytesIO
from reportlab.pdfgen import canvas

# ---- CONFIG ----
st.set_page_config(page_title="DataPlay - Análisis Ofensivo", layout="wide")
st.title("🏀 DataPlay - Dashboard Ofensivo de Jugadores NBA")

# ---- Filtros ----
st.sidebar.header("Filtros de Datos") # Encabezado más general
temp_actual = datetime.now().year

# Generar la lista de todas las temporadas disponibles
all_seasons = [f"{y}-{str(y+1)[-2:]}" for y in range(2015, temp_actual)]

# Determinar el índice de la última temporada generada (que debería ser la 2024-2025)
default_season_index = len(all_seasons) - 1

season = st.sidebar.selectbox(
    "Selecciona la temporada",
    all_seasons,
    index=default_season_index # Usamos el índice calculado para la selección por defecto
)
season_type = st.sidebar.radio("Tipo de temporada", ["Regular Season", "Playoffs"])

# ---- Carga de Datos ----
st.sidebar.info(f"Cargando datos de NBA para la temporada {season}...")
@st.cache_data
def cargar_datos(season, season_type):
    stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        season_type_all_star=season_type,
        per_mode_detailed="PerGame"
    )
    df = stats.get_data_frames()[0]
    return df

df_original = cargar_datos(season, season_type) # Cargamos el DataFrame original
st.success("✅ Datos cargados exitosamente")

# --- Aplicar filtro de equipo ---
teams = sorted(df_original['TEAM_ABBREVIATION'].unique())

# --- Buscar el índice de 'OKC' para establecerlo como valor por defecto ---
default_team_name = "OKC"
default_team_index = 0 # Valor por defecto si 'OKC' no se encuentra (será "Todos")
try:
    # El selectbox incluye "Todos" al principio, así que el índice real será +1
    default_team_index = teams.index(default_team_name) + 1
except ValueError:
    # Si por alguna razón 'OKC' no está en la lista (ej: datos de otra temporada)
    # se mantendrá "Todos" como valor por defecto.
    st.sidebar.warning(f"El equipo '{default_team_name}' no se encontró en los datos cargados. Se seleccionó 'Todos' por defecto.")


selected_team = st.sidebar.selectbox(
    "Filtra por Equipo",
    ["Todos"] + list(teams),
    index=default_team_index # Usamos el índice de 'OKC'
)

df_filtered_by_team = df_original.copy() # Creamos una copia para aplicar filtros
if selected_team != "Todos":
    df_filtered_by_team = df_original[df_original['TEAM_ABBREVIATION'] == selected_team]

# Si eliminamos el filtro de posición, df_filtered_by_position es igual a df_filtered_by_team
df_filtered_by_position = df_filtered_by_team.copy()


# --- Aplicar filtro de jugador ---
# Obtenemos los nombres de jugadores únicos del DataFrame ya filtrado
player_names = sorted(df_filtered_by_position['PLAYER_NAME'].unique())
selected_player = st.sidebar.selectbox("Filtra por Jugador", ["Todos"] + list(player_names))

df_final = df_filtered_by_position.copy()
if selected_player != "Todos":
    df_final = df_filtered_by_position[df_filtered_by_position['PLAYER_NAME'] == selected_player]

# ---- Gráficas ----
st.subheader("🔍 Análisis Ofensivo de Jugadores")

# Asegurarse de que haya datos para graficar
if df_final.empty:
    st.warning("No hay datos disponibles para los filtros seleccionados.")
else:
    col1, col2 = st.columns(2)
    with col1:
        fig_pts = px.bar(df_final.sort_values("PTS", ascending=False).head(15),
                         x="PLAYER_NAME", y="PTS",
                         title="Top 15: Puntos por Partido",
                         color="PTS")
        st.plotly_chart(fig_pts, use_container_width=True)

    with col2:
        fig_ast = px.bar(df_final.sort_values("AST", ascending=False).head(15),
                         x="PLAYER_NAME", y="AST",
                         title="Top 15: Asistencias por Partido",
                         color="AST")
        st.plotly_chart(fig_ast, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        fig_eff = px.scatter(df_final, x="MIN", y="PTS", size="FG_PCT",
                             hover_name="PLAYER_NAME", title="Minutos vs Puntos (Tamaño: FG%)",
                             color="FG_PCT")
        st.plotly_chart(fig_eff, use_container_width=True)

    with col4:
        fig_fg3 = px.bar(df_final.sort_values("FG3M", ascending=False).head(15),
                         x="PLAYER_NAME", y="FG3M",
                         title="Top 15: Triples Encestados",
                         color="FG3M")
        st.plotly_chart(fig_fg3, use_container_width=True)

    # ---- Tabla ----
    st.subheader("📋 Datos Detallados de Jugadores")
    columnas_mostrar = ["PLAYER_NAME", "TEAM_ABBREVIATION", "PTS", "AST", "FGM", "FGA", "FG_PCT", "FG3M", "FG3A", "FG3_PCT", "MIN"]
    st.dataframe(df_final[columnas_mostrar].sort_values("PTS", ascending=False), use_container_width=True)

    # ---- Descarga CSV ----
    @st.cache_data
    def convertir_csv(dataframe):
        return dataframe.to_csv(index=False).encode("utf-8")

    csv = convertir_csv(df_final[columnas_mostrar])
    st.download_button("⬇️ Descargar CSV", csv, f"jugadores_{season}_{selected_team}_{season_type.replace(' ', '_')}.csv", "text/csv")

    # ---- Descarga PDF ----
    def generar_pdf(df):
        buffer = BytesIO()
        c = canvas.Canvas(buffer)
        c.setFont("Helvetica-Bold", 16)

        # Título principal del PDF
        title_text = f"Reporte Ofensivo: {season} - {season_type}"
        c.drawString(50, 800, title_text)

        y_offset = 780
        c.setFont("Helvetica", 10)

        # Añadir filtros al PDF
        if selected_team != "Todos":
            c.drawString(50, y_offset, f"Equipo: {selected_team}")
            y_offset -= 18
        if selected_player != "Todos":
            c.drawString(50, y_offset, f"Jugador: {selected_player}")
            y_offset -= 18

        y = y_offset
        # Asegurarse de que haya datos para el PDF
        if not df.empty:
            for i, row in df.head(20).iterrows():
                c.drawString(50, y, f"{row['PLAYER_NAME'][:25]:25} | PTS: {row['PTS']:.1f} | AST: {row['AST']:.1f} | FG%: {row['FG_PCT']:.2%}")
                y -= 18
                if y < 50:
                    c.showPage()
                    y = 800
        else:
            c.drawString(50, y, "No hay datos para los filtros seleccionados.")
        c.save()
        buffer.seek(0)
        return buffer

    pdf_buffer = generar_pdf(df_final[columnas_mostrar])
    st.download_button("📝 Descargar PDF (Resumen)", pdf_buffer, f"reporte_ofensivo_{season}_{selected_team}.pdf")

st.caption("Desarrollado con ❤️ por DataPlay")















#streamlit run app.py
    
    # python app.py
