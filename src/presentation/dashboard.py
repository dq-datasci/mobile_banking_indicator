import streamlit as st
import pandas as pd
import plotly.express as px
from pyspark.sql import SparkSession
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="OmniVoC Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PREMIUM STYLING (Glassmorphism & Dark Mode) ---
st.markdown("""
<style>
    /* Global App Background */
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Typography */
    h1, h2, h3 {
        color: #00ffcc !important;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    /* Custom HTML Metrics to guarantee readability */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: transform 0.2s ease-in-out;
        text-align: center;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #00ffcc;
        box-shadow: 0 8px 32px 0 rgba(0, 255, 204, 0.2);
    }
    .metric-label {
        color: #e0e0e0;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-value {
        color: #ffffff;
        font-size: 2.8rem;
        font-weight: 800;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.5);
    }
    .metric-delta {
        font-size: 1rem;
        font-weight: bold;
        margin-top: 5px;
    }
    .delta-positive { color: #00ffcc; }
    .delta-negative { color: #ff4757; }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING (CACHED) ---
@st.cache_resource
def get_spark():
    return SparkSession.builder \
        .appName("OmniVoC-Dashboard") \
        .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.1.0") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .master("local[*]") \
        .getOrCreate()

@st.cache_data
def get_nps_data():
    spark = get_spark()
    if os.path.exists("data/gold/Aggr_NPS"):
        df = spark.read.format("delta").load("data/gold/Aggr_NPS").toPandas()
        return df
    else:
        return pd.DataFrame()

# --- HEADER ---
st.title("⚡ OmniVoC Executive Dashboard")
st.markdown("*Real-time Mobile Banking Intelligence & Retargeting*")
st.markdown("---")

df_nps = get_nps_data()

if df_nps.empty:
    st.error("No se encontraron datos en la capa Gold. Ejecuta `python main.py run-all` primero.")
    st.stop()

# --- FILTERS ---
st.subheader("🎯 Filtros Estratégicos")
bancos_disponibles = ["Todos los Bancos"] + sorted(df_nps['bank_name'].unique().tolist())
banco_seleccionado = st.selectbox("Seleccione un Banco a analizar:", bancos_disponibles)

# Filter dataframe
if banco_seleccionado != "Todos los Bancos":
    df_filtered = df_nps[df_nps['bank_name'] == banco_seleccionado]
else:
    df_filtered = df_nps

st.markdown("<br>", unsafe_allow_html=True)

# --- TOP METRICS (HTML Custom Cards) ---
col1, col2, col3, col4 = st.columns(4)

total_reviews = df_filtered['total_reviews'].sum()
total_promoters = df_filtered['promoters'].sum()
total_detractors = df_filtered['detractors'].sum()
if total_reviews > 0:
    global_nps = ((total_promoters / total_reviews) - (total_detractors / total_reviews)) * 100
else:
    global_nps = 0.0

delta_class = "delta-positive" if global_nps >= 0 else "delta-negative"
delta_symbol = "▲" if global_nps >= 0 else "▼"

def render_metric(label, value, is_nps=False):
    if is_nps:
        return f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-delta {delta_class}">{delta_symbol} {global_nps:.1f} pts</div>
        </div>
        """
    else:
        return f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """

with col1:
    st.markdown(render_metric("Total Reseñas Analizadas", f"{total_reviews:,}"), unsafe_allow_html=True)
with col2:
    st.markdown(render_metric("Promotores (Leales)", f"{total_promoters:,}"), unsafe_allow_html=True)
with col3:
    st.markdown(render_metric("Detractores (Riesgo)", f"{total_detractors:,}"), unsafe_allow_html=True)
with col4:
    st.markdown(render_metric("Net Promoter Score", f"{global_nps:.1f}", is_nps=True), unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# --- VISUALIZATIONS ---
st.subheader("📊 Análisis Competitivo: NPS por Institución Financiera")

# Bar Chart de NPS usando Plotly
fig_nps = px.bar(
    df_nps, 
    x='bank_name', 
    y='nps_score', 
    color='nps_score',
    color_continuous_scale=px.colors.diverging.RdYlGn,
    text_auto='.1f',
    labels={'bank_name': 'Banco', 'nps_score': 'Net Promoter Score'},
    template="plotly_dark"
)

fig_nps.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    title_font_color="#00ffcc",
    font_color="#ffffff",
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
)

if banco_seleccionado != "Todos los Bancos":
    # Highlight selected bank by adding an annotation or making it clear
    fig_nps.add_annotation(
        x=banco_seleccionado, y=global_nps,
        text="👉 Seleccionado", showarrow=True, arrowhead=1, yshift=10,
        font=dict(color="#00ffcc", size=14)
    )

st.plotly_chart(fig_nps, use_container_width=True)

st.markdown("---")

# Composición de Usuarios
st.subheader("👥 Composición de Base de Usuarios")

# Melt dataset for stacked bar
df_melted = df_nps.melt(
    id_vars=['bank_name'], 
    value_vars=['promoters', 'passives', 'detractors'],
    var_name='Segmento', 
    value_name='Volumen'
)

# Custom Colors
color_discrete_map = {
    'promoters': '#00b894',
    'passives': '#fdcb6e',
    'detractors': '#d63031'
}

fig_comp = px.bar(
    df_melted, 
    x='bank_name', 
    y='Volumen', 
    color='Segmento',
    color_discrete_map=color_discrete_map,
    barmode='stack',
    template="plotly_dark"
)

fig_comp.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color="#ffffff",
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
)

st.plotly_chart(fig_comp, use_container_width=True)

st.markdown("---")
st.caption("🚀 OmniVoC Engine v1.0 | Sprint 3 MVP Finalizado")

# --- VISUALIZATIONS ---
st.subheader("📊 Análisis Competitivo: NPS por Institución Financiera")

# Bar Chart de NPS usando Plotly
fig_nps = px.bar(
    df_nps, 
    x='bank_name', 
    y='nps_score', 
    color='nps_score',
    color_continuous_scale=px.colors.diverging.RdYlGn,
    text_auto='.1f',
    labels={'bank_name': 'Banco', 'nps_score': 'Net Promoter Score'},
    template="plotly_dark"
)

fig_nps.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    title_font_color="#00ffcc",
    font_color="#b2bec3"
)

st.plotly_chart(fig_nps, use_container_width=True)

st.markdown("---")

# Composición de Usuarios
st.subheader("👥 Composición de Base de Usuarios")

# Melt dataset for stacked bar
df_melted = df_nps.melt(
    id_vars=['bank_name'], 
    value_vars=['promoters', 'passives', 'detractors'],
    var_name='Segmento', 
    value_name='Volumen'
)

# Custom Colors
color_discrete_map = {
    'promoters': '#00b894',
    'passives': '#fdcb6e',
    'detractors': '#d63031'
}

fig_comp = px.bar(
    df_melted, 
    x='bank_name', 
    y='Volumen', 
    color='Segmento',
    color_discrete_map=color_discrete_map,
    barmode='stack',
    template="plotly_dark"
)

fig_comp.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color="#b2bec3"
)

st.plotly_chart(fig_comp, use_container_width=True)

st.markdown("---")
st.caption("🚀 OmniVoC Engine v1.0 | Sprint 3 MVP Finalizado")
