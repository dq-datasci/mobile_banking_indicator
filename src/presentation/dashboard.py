import streamlit as st
import pandas as pd
import plotly.express as px
from pyspark.sql import SparkSession
import os
import sys

# Ensure the root of the project is in the python path to find 'src'
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

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
    
    /* Fix for Streamlit Tabs visibility */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #ffffff !important;
    }
    .stTabs [data-baseweb="tab-list"] button {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px 8px 0 0 !important;
        margin-right: 5px !important;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: rgba(0, 255, 204, 0.15) !important;
        border-bottom: 3px solid #00ffcc !important;
    }
    
    /* Fix for Chat messages and Alerts */
    .stChatMessage p, .stChatMessage div {
        color: #ffffff !important;
    }
    .stAlert p {
        color: #ffffff !important;
    }
    div[data-testid="stChatMessageContent"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 10px;
    }
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

# --- TABS FOR DIFFERENT MODULES ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Métricas Generales", "🧠 Modelos Predictivos (Churn)", "🤖 Agente IA (LangGraph)", "📈 Estocásticos (Markov y Colas)"])

with tab1:
    st.subheader("Análisis Competitivo: NPS por Institución Financiera")

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

with tab2:
    st.subheader("Modelos de Machine Learning: Churn")
    
    st.markdown("Resultados del **Entrenamiento AutoML PyCaret**:")
    try:
        metrics_df = pd.read_csv("docs/MODELS_RESULTS/pycaret_metrics.csv")
        st.dataframe(metrics_df.style.highlight_max(axis=0, subset=['Accuracy', 'AUC', 'F1']), use_container_width=True)
    except Exception as e:
        st.info("No se encontraron resultados de AutoML PyCaret. Ejecuta `python main.py run-automl`.")
        
    st.markdown("---")
    st.markdown("🔮 **Simulador de Predicción de Churn (PyCaret)**")
    
    if os.path.exists("docs/MODELS_RESULTS/best_churn_model.pkl"):
        from pycaret.classification import load_model, predict_model
        
        # Load the model directly (cache to avoid reloading on every interaction)
        @st.cache_resource
        def get_churn_model():
            return load_model("docs/MODELS_RESULTS/best_churn_model")
            
        model = get_churn_model()
        
        st.markdown("Ajusta los parámetros para simular la probabilidad de que un cliente abandone el banco:")
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            sim_length = st.slider("Longitud del mensaje (caracteres)", 0, 500, 150)
        with col_s2:
            sim_hour = st.slider("Hora del día (0-23)", 0, 23, 14)
        with col_s3:
            sim_reply = st.selectbox("¿Tiene respuesta del banco?", [1, 0])
            
        if st.button("Predecir Riesgo de Churn", type="primary"):
            input_df = pd.DataFrame({
                'content_length': [sim_length],
                'hour_of_day': [sim_hour],
                'has_bank_reply': [sim_reply]
            })
            pred = predict_model(model, data=input_df)
            churn_risk = pred['prediction_label'].iloc[0]
            score = pred['prediction_score'].iloc[0]
            
            if churn_risk == 1:
                st.error(f"⚠️ **¡ALTO RIESGO DE CHURN!** (Confianza: {score*100:.1f}%) - Se requiere retargeting inmediato.")
            else:
                st.success(f"✅ **Riesgo Bajo.** El usuario probablemente se quedará. (Confianza: {score*100:.1f}%)")
    else:
        st.info("⏳ El modelo predictivo se está entrenando y guardando. Esto puede tardar ~5 minutos. Cuando termine, actualiza la página para usar el simulador.")

    st.markdown("---")
    st.markdown("Resumen del **Modelo Econométrico Logit**:")
    try:
        with open("docs/MODELS_RESULTS/logit_summary.txt", "r") as f:
            st.code(f.read(), language="text")
    except Exception:
        st.info("No se encontraron resultados de Logit. Ejecuta `python main.py run-models`.")

with tab3:
    st.subheader("Agente LangGraph: Triage y Community Manager")
    st.markdown("Escribe un reporte de falla, queja o reseña para probar el enrutamiento inteligente.")
    
    # Lazy loading of LangGraph agent to avoid blocking startup
    @st.cache_resource
    def get_agent():
        from src.use_cases.langgraph_agent import OmniVocMultiAgent
        return OmniVocMultiAgent()
        
    agent = get_agent()
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Escribe tu queja (ej: Me robaron mi dinero...)"):
        # Display user message
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Process with LangGraph
        with st.spinner("Analizando urgencia y ruteando..."):
            result = agent.process_issue(prompt)
            urgency = result.get("urgency")
            dept = result.get("department")
            response = result.get("response")
            
        # Display agent response
        with st.chat_message("assistant"):
            st.markdown(f"**Análisis LangGraph:**\n- *Urgencia:* {urgency}\n- *Ruteo:* {dept}")
            st.markdown(response)
            
        st.session_state.messages.append({"role": "assistant", "content": f"**Ruteo:** {dept} ({urgency})\n\n{response}"})

with tab4:
    st.subheader("Modelamiento Estocástico (Nivel Matemático)")
    st.markdown("Basado en Cadenas de Markov de Satisfacción y Teoría de Colas (M/M/1) para Atención al Cliente.")
    
    try:
        import json
        with open("docs/MODELS_RESULTS/stochastic_results.json", "r") as f:
            stoch_data = json.load(f)
            
        markov_data = stoch_data.get("markov_chains", {})
        queuing_data = stoch_data.get("queuing_theory", {})
        
        col_m1, col_m2 = st.columns(2)
        
        with col_m1:
            st.markdown("### 🎲 Cadenas de Markov")
            st.markdown("Probabilidades de Transición de Estados de Satisfacción:")
            if "transition_matrix" in markov_data:
                matrix_df = pd.DataFrame(markov_data["transition_matrix"]).T
                fig_hm = px.imshow(
                    matrix_df, 
                    text_auto=True, 
                    color_continuous_scale="Viridis",
                    title="Matriz de Transición"
                )
                fig_hm.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#ffffff")
                st.plotly_chart(fig_hm, use_container_width=True)
            
            if "stationary_probabilities" in markov_data:
                st.markdown("Probabilidad Estacionaria (Riesgo a Largo Plazo):")
                stat_df = pd.DataFrame([markov_data["stationary_probabilities"]])
                st.dataframe(stat_df.style.format("{:.2%}"), use_container_width=True)
                
        with col_m2:
            st.markdown("### ⏱️ Teoría de Colas (Customer Service)")
            st.markdown("Estimación del embudo de retención M/M/1:")
            if queuing_data:
                l = queuing_data.get("lambda_arrivals_per_hour", 0)
                m = queuing_data.get("mu_service_per_hour", 0)
                rho = queuing_data.get("rho_saturation_prob", 0)
                w = queuing_data.get("w_expected_wait_hours", 0)
                
                st.metric("Tasa de Llegada (Quejas/hora)", f"λ = {l:.2f}")
                st.metric("Tasa de Servicio (Respuestas/hora)", f"μ = {m:.2f}")
                st.metric("Probabilidad de Saturación (Utilización)", f"ρ = {rho:.0%}", delta=f"{rho:.0%}", delta_color="inverse")
                
                if w == float('inf'):
                    st.metric("Tiempo Estimado de Espera Promedio", "W = Infinito")
                else:
                    st.metric("Tiempo Estimado de Espera Promedio", f"W = {w:.2f} hrs")
                
                if rho >= 0.95:
                    st.error("🚨 ALERTA: Sistema SATURADO. El tiempo de espera de los clientes quejosos crecerá infinitamente sin intervención.")
                elif rho >= 0.7:
                    st.warning("⚠️ PRECAUCIÓN: El sistema está cerca de su límite operativo.")
                else:
                    st.success("✅ Sistema Estable: Capacidad de respuesta adecuada.")
    except Exception as e:
        st.info("No se encontraron resultados estocásticos. Ejecuta `python main.py run-stochastic` en la terminal.")

st.markdown("---")
st.caption("🚀 OmniVoC Engine v2.0 | Release 1 Completado | IA & DevOps")
