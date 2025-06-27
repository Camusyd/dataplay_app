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
st.sidebar.header("Filtros de Temporada")
temp_actual = datetime.now().year
season = st.sidebar.selectbox("Selecciona la temporada", [f"{y}-{str(y+1)[-2:]}" for y in range(2015, temp_actual)])
season_type = st.sidebar.radio("Tipo de temporada", ["Regular Season", "Playoffs"])

# ---- Carga de Datos ----
st.sidebar.info("Cargando datos de NBA...")
@st.cache_data

def cargar_datos(season, season_type):
    stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        season_type_all_star=season_type,
        per_mode_detailed="PerGame"
    )
    df = stats.get_data_frames()[0]
    return df

df = cargar_datos(season, season_type)
st.success("✅ Datos cargados exitosamente")

# ---- Gráficas ----
st.subheader("🔍 Análisis Ofensivo de Jugadores")

col1, col2 = st.columns(2)
with col1:
    fig_pts = px.bar(df.sort_values("PTS", ascending=False).head(15),
                     x="PLAYER_NAME", y="PTS",
                     title="Top 15: Puntos por Partido",
                     color="PTS")
    st.plotly_chart(fig_pts, use_container_width=True)

with col2:
    fig_ast = px.bar(df.sort_values("AST", ascending=False).head(15),
                     x="PLAYER_NAME", y="AST",
                     title="Top 15: Asistencias por Partido",
                     color="AST")
    st.plotly_chart(fig_ast, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    fig_eff = px.scatter(df, x="MIN", y="PTS", size="FG_PCT",
                         hover_name="PLAYER_NAME", title="Minutos vs Puntos (Tamaño: FG%)",
                         color="FG_PCT")
    st.plotly_chart(fig_eff, use_container_width=True)

with col4:
    fig_fg3 = px.bar(df.sort_values("FG3M", ascending=False).head(15),
                     x="PLAYER_NAME", y="FG3M",
                     title="Top 15: Triples Encestados",
                     color="FG3M")
    st.plotly_chart(fig_fg3, use_container_width=True)

# ---- Tabla ----
st.subheader("📋 Datos Detallados de Jugadores")
columnas_mostrar = ["PLAYER_NAME", "TEAM_ABBREVIATION", "PTS", "AST", "FGM", "FGA", "FG_PCT", "FG3M", "FG3A", "FG3_PCT", "MIN"]
st.dataframe(df[columnas_mostrar].sort_values("PTS", ascending=False), use_container_width=True)

# ---- Descarga CSV ----
@st.cache_data
def convertir_csv(dataframe):
    return dataframe.to_csv(index=False).encode("utf-8")

csv = convertir_csv(df[columnas_mostrar])
st.download_button("⬇️ Descargar CSV", csv, f"jugadores_{season}_{season_type.replace(' ', '_')}.csv", "text/csv")

# ---- Descarga PDF ----
def generar_pdf(df):
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, f"Reporte Ofensivo: {season} - {season_type}")
    c.setFont("Helvetica", 10)
    y = 780
    for i, row in df.head(20).iterrows():
        c.drawString(50, y, f"{row['PLAYER_NAME'][:25]:25} | PTS: {row['PTS']:.1f} | AST: {row['AST']:.1f} | FG%: {row['FG_PCT']:.2%}")
        y -= 18
        if y < 50:
            c.showPage()
            y = 800
    c.save()
    buffer.seek(0)
    return buffer

pdf_buffer = generar_pdf(df[columnas_mostrar])
st.download_button("📝 Descargar PDF (Resumen)", pdf_buffer, f"reporte_ofensivo_{season}.pdf")

st.caption("Desarrollado con ❤️ por DataPlay")















    
    # python app.py
