import streamlit as st
import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamplayerdashboard
import plotly.express as px
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.set_page_config(page_title="Denver Nuggets Dashboard", layout="wide")

# Cargar datos desde NBA API
@st.cache_data
def cargar_datos(season_type):
    team_id = [t for t in teams.get_teams() if t['full_name'] == 'Denver Nuggets'][0]['id']
    df = teamplayerdashboard.TeamPlayerDashboard(
        team_id=team_id, season='2022-23', season_type_all_star=season_type
    ).get_data_frames()[1]
    df['EFFICIENCY'] = (df['PTS'] + df['REB'] + df['AST'] + df['STL'] + df['BLK']
                        - (df['FGA'] - df['FGM']) - df['TOV'])
    return df

# Sidebar
st.sidebar.title("Filtros")
tipo_temporada = st.sidebar.selectbox("Temporada", ["Regular Season", "Playoffs"])
df = cargar_datos(tipo_temporada)

# Filtro por posición
posiciones = df['PLAYER_POSITION'].dropna().unique().tolist()
pos_filtradas = st.sidebar.multiselect("Filtrar por posición", posiciones)
if pos_filtradas:
    df = df[df["PLAYER_POSITION"].isin(pos_filtradas)]

# Título
st.title("📊 Dashboard - Denver Nuggets 2022-23")

# Columnas con gráficos
col1, col2 = st.columns(2)
col1.plotly_chart(px.bar(df.sort_values("EFFICIENCY", ascending=False), x="PLAYER_NAME", y="EFFICIENCY",
                         title="Eficiencia por Jugador", color="EFFICIENCY", color_continuous_scale='Viridis'), use_container_width=True)

col2.plotly_chart(px.scatter(df, x="AST", y="PTS", color="PLAYER_NAME", size="EFFICIENCY",
                             title="Asistencias vs Puntos", hover_name='PLAYER_NAME'), use_container_width=True)

col3, col4 = st.columns(2)
col3.plotly_chart(px.bar(df.sort_values("PTS", ascending=False), x="PLAYER_NAME", y="PTS", color="PTS",
                         title="Puntos por Jugador", color_continuous_scale='Blues'), use_container_width=True)
col4.plotly_chart(px.bar(df.sort_values("REB", ascending=False), x="PLAYER_NAME", y="REB", color="REB",
                         title="Rebotes por Jugador", color_continuous_scale='Purples'), use_container_width=True)

col5, col6 = st.columns(2)
col5.plotly_chart(px.bar(df.sort_values("STL", ascending=False), x="PLAYER_NAME", y="STL", color="STL",
                         title="Robos por Jugador", color_continuous_scale='Greens'), use_container_width=True)
col6.plotly_chart(px.bar(df.sort_values("FG3M", ascending=False), x="PLAYER_NAME", y="FG3M", color="FG3M",
                         title="Triples Encestados", color_continuous_scale='Reds'), use_container_width=True)

# Tabla de datos
st.subheader("📋 Tabla de Jugadores")
st.dataframe(df[["PLAYER_NAME", "PLAYER_POSITION", "PTS", "REB", "AST", "EFFICIENCY"]])

# Botón para descargar CSV
csv = df.to_csv(index=False).encode()
st.download_button("📥 Descargar CSV", csv, file_name="jugadores_filtrados.csv", mime="text/csv")

# Botón para descargar PDF
if st.button("📄 Generar Informe PDF"):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, f"Informe NBA - {tipo_temporada}")
    y = 720
    for _, row in df.iterrows():
        c.drawString(50, y, f"{row['PLAYER_NAME']}: PTS={row['PTS']}, REB={row['REB']}, AST={row['AST']}, EFF={row['EFFICIENCY']}")
        y -= 20
        if y < 50:
            c.showPage()
            y = 750
    c.save()
    st.download_button("📄 Descargar Informe PDF", data=buffer.getvalue(), file_name="informe.pdf", mime="application/pdf")











    
    # python app.py
