import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ==========================================
# 1. CONFIGURACIÓN Y ESTILOS
# ==========================================
st.set_page_config(layout="wide", page_title="Crio-Carnot Pro", page_icon="🥭")

st.markdown("""
<style>
    div[data-testid="metric-container"] {
        background-color: rgba(3, 169, 244, 0.05);
        border: 1px solid rgba(3, 169, 244, 0.3);
        padding: 15px 20px;
        border-radius: 12px;
        border-left: 6px solid #0288d1;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    div[data-testid="metric-container"]:hover { transform: translateY(-2px); }
    div[data-testid="stMetricValue"] > div { color: #0288d1; font-weight: 800; }
    .stTabs [data-baseweb="tab"] { font-weight: 600; }
    .stTabs [aria-selected="true"] { border-bottom: 4px solid #0288d1 !important; color: #0288d1; }
    .main-title { text-align: center; color: #01579b; padding-bottom: 10px; font-family: 'Helvetica Neue', sans-serif;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🥭 Crio-Carnot Pro: Concentración por Frío</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Evaluación Termodinámica del Ciclo de Carnot Inverso en Jugos y Néctares.</p>", unsafe_allow_html=True)

# ==========================================
# 2. PARÁMETROS DEL SISTEMA (PANEL LATERAL)
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3183/3183506.png", width=80)
st.sidebar.header("⚙️ Parámetros de Operación")

producto = st.sidebar.selectbox("Producto a Crioconcentrar:", ["Néctar de Mango", "Jugo de Maracuyá"])
masa_kg = st.sidebar.number_input("Masa del lote (kg):", min_value=100, max_value=10000, value=1000, step=100)

st.sidebar.markdown("---")
st.sidebar.subheader("Temperaturas (Depósitos)")
t_caliente = st.sidebar.slider("T. Ambiente / Condensador (TH) °C:", 10.0, 40.0, 25.0)
t_fria = st.sidebar.slider("T. Cámara Fría / Evaporador (TC) °C:", -40.0, -5.0, -15.0)
eficiencia_2da_ley = st.sidebar.slider("Eficiencia del Compresor (%):", 20, 80, 45) / 100.0

st.sidebar.info("💡 **Dato:** El límite teórico máximo de eficiencia de cualquier máquina frigorífica está dictado por el Teorema de Carnot.")

# ==========================================
# 3. CÁLCULOS TERMODINÁMICOS
# ==========================================
# Conversión a Kelvin (Obligatorio para Carnot)
TH_K = t_caliente + 273.15
TC_K = t_fria + 273.15

# COP de Carnot (Refrigeración) -> COP = TC / (TH - TC)
COP_ideal = TC_K / (TH_K - TC_K)
COP_real = COP_ideal * eficiencia_2da_ley

# Propiedades del Néctar (Simplificadas)
Cp_nectar = 3.8  # kJ/kg*K
T_congelacion = -2.5 # °C
T_inicial = 20.0 # °C
Calor_latente_hielo = 334.0 # kJ/kg
porcentaje_agua_congelar = 0.50 # Se congela el 50% del agua para concentrar

# 1. Calor Sensible (Enfriar de 20°C a -2.5°C)
Q_sensible = masa_kg * Cp_nectar * (T_inicial - T_congelacion)
# 2. Calor Latente (Congelar parte del agua) -> Asumimos 85% de agua en el néctar
masa_agua = masa_kg * 0.85
Q_latente = (masa_agua * porcentaje_agua_congelar) * Calor_latente_hielo
# Calor Total a Extraer (QL)
Q_L = Q_sensible + Q_latente 

# Trabajo Requerido (W = QL / COP)
W_ideal_kj = Q_L / COP_ideal
W_real_kj = Q_L / COP_real

W_ideal_kwh = W_ideal_kj / 3600
W_real_kwh = W_real_kj / 3600

# ==========================================
# 4. PESTAÑAS DEL DASHBOARD
# ==========================================
tab1, tab2, tab3 = st.tabs(["📐 Máquina de Carnot", "🧊 Calorimetría del Néctar", "⚡ Gasto Energético"])

with tab1:
    st.subheader("Análisis del Ciclo de Carnot Inverso")
    st.markdown("El ciclo ideal representa el máximo rendimiento posible operando entre dos fuentes térmicas.")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Depósito Caliente (TH)", f"{TH_K:.2f} K", f"{t_caliente}°C")
    c2.metric("Depósito Frío (TC)", f"{TC_K:.2f} K", f"{t_fria}°C")
    c3.metric("Límite de Carnot (COP Máx)", f"{COP_ideal:.2f}")
    
    st.latex(r"COP_{Ideal} = \frac{T_C}{T_H - T_C}")
    
    # Gráfico de influencia de TC en el COP
    tc_array = np.linspace(-40, 0, 100)
    cop_array = (tc_array + 273.15) / (TH_K - (tc_array + 273.15))
    
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=tc_array, y=cop_array, mode='lines', line=dict(color='#0288d1', width=4), name='COP Ideal'))
    fig1.add_trace(go.Scatter(x=[t_fria], y=[COP_ideal], mode='markers', marker=dict(color='red', size=12), name='Punto de Operación'))
    fig1.update_layout(title=f"Evolución del COP ideal manteniendo TH = {t_caliente}°C", 
                       xaxis_title="Temperatura del Evaporador TC (°C)", yaxis_title="COP de Carnot",
                       plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    st.subheader("Requerimiento de Extracción de Calor ($Q_L$)")
    st.markdown("Para formar los cristales de hielo y separar el néctar concentrado, debemos extraer energía sensible y latente.")
    
    r1, r2, r3 = st.columns(3)
    r1.metric("Calor Sensible", f"{Q_sensible:,.0f} kJ", "Enfriamiento líquido")
    r2.metric("Calor Latente", f"{Q_latente:,.0f} kJ", "Cristalización del agua")
    r3.metric("Carga Térmica Total (QL)", f"{Q_L:,.0f} kJ", "Calor absorbido de la fruta")
    
    fig2 = go.Figure(data=[go.Pie(labels=['Calor Sensible (Líquido)', 'Calor Latente (Congelación)'], 
                                  values=[Q_sensible, Q_latente], hole=.4, marker_colors=['#4fc3f7', '#01579b'])])
    fig2.update_layout(title=f"Distribución de la Carga Térmica ({producto})")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("Trabajo del Compresor y Costo Energético")
    st.markdown("Impacto económico de las ineficiencias de la Segunda Ley de la Termodinámica.")
    
    colA, colB = st.columns(2)
    with colA:
        st.warning(f"**Trabajo Ideal (Carnot):**\n\n### {W_ideal_kwh:,.1f} kWh\n\n*(Consumo si la máquina fuera perfecta y reversible)*")
        st.error(f"**Trabajo Real (Compresor Industrial):**\n\n### {W_real_kwh:,.1f} kWh\n\n*(Consumo con una eficiencia del {eficiencia_2da_ley*100}%)*")
    
    with colB:
        costo_kwh = st.number_input("Costo de la Energía Eléctrica (Soles/kWh):", value=0.65, step=0.05)
        ahorro_perdido = (W_real_kwh - W_ideal_kwh) * costo_kwh
        st.success(f"**Costo Eléctrico Real del Lote:**\n\n### S/ {W_real_kwh * costo_kwh:,.2f}")
        st.info(f"**Costo por Ineficiencia Termodinámica:**\n\n### S/ {ahorro_perdido:,.2f} \n*(Dinero perdido respecto a la máquina de Carnot)*")
