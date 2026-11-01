import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ==========================================
# 1. CONFIGURACIÓN Y DISEÑO TROPICAL (CSS)
# ==========================================
st.set_page_config(layout="wide", page_title="Crio-Carnot Pro", page_icon="🥭")

st.markdown("""
<style>
    /* Fondo de pantalla general tropical */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1605807646983-377bc5a76493?q=80&w=2000&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Forzar fondo blanco esmerilado en el centro y en el panel lateral */
    .block-container, [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
    }
    
    /* Bordes redondeados solo para el centro */
    .block-container {
        border-radius: 20px;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
    }
    
    /* Forzar letras oscuras en todos los textos, títulos y etiquetas */
    h1, h2, h3, p, label, .stMarkdown, span {
        color: #1a1a1a !important;
    }
    
    /* Estilo de las métricas */
    div[data-testid="metric-container"] {
        background-color: rgba(255, 152, 0, 0.1);
        border: 1px solid rgba(255, 152, 0, 0.4);
        padding: 15px 20px;
        border-radius: 12px;
        border-left: 6px solid #ff9800;
    }
    div[data-testid="stMetricValue"] > div { color: #e65100 !important; font-weight: 800; }
    
    /* Título principal */
    .main-title { text-align: center; color: #e65100 !important; font-weight: 900; padding-bottom: 10px; font-family: sans-serif; }
    
    /* Pestañas */
    .stTabs [data-baseweb="tab"] { font-weight: 700; color: #555 !important; background-color: transparent; }
    .stTabs [aria-selected="true"] { border-bottom: 4px solid #ff9800 !important; color: #e65100 !important; background-color: rgba(255,152,0,0.05);}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🥭 Crio-Carnot Pro: Concentración por Frío</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Evaluación Termodinámica y Nutricional de la Crioconcentración de Néctares.</p>", unsafe_allow_html=True)

# ==========================================
# 2. PANEL LATERAL
# ==========================================
st.sidebar.header("⚙️ Parámetros de Operación")

producto = st.sidebar.selectbox("Materia Prima:", ["Néctar de Mango", "Jugo de Maracuyá"])
masa_kg = st.sidebar.number_input("Masa del lote (kg):", min_value=100, max_value=10000, value=1000, step=100)

st.sidebar.markdown("---")
st.sidebar.subheader("Temperaturas del Ciclo")
t_caliente = st.sidebar.slider("T. Ambiente / Condensador (TH) °C:", 10.0, 40.0, 25.0)
t_fria = st.sidebar.slider("T. Cámara Fría / Evaporador (TC) °C:", -40.0, -5.0, -15.0)
eficiencia_2da_ley = st.sidebar.slider("Eficiencia del Compresor (%):", 20, 80, 45) / 100.0

st.sidebar.markdown("---")
# EFECTO WOW 1: Botón de congelación
if st.sidebar.button("❄️ Encender Cámara de Frío", use_container_width=True):
    st.snow() 
    st.sidebar.success("¡Sistema de ultracongelación activado!")

# ==========================================
# 3. CÁLCULOS TERMODINÁMICOS
# ==========================================
TH_K = t_caliente + 273.15
TC_K = t_fria + 273.15
COP_ideal = TC_K / (TH_K - TC_K)
COP_real = COP_ideal * eficiencia_2da_ley

T_inicial = 20.0 
Calor_latente_hielo = 334.0 
porcentaje_agua_congelar = 0.50 

if producto == "Néctar de Mango":
    Cp_nectar = 3.9  
    porcentaje_agua = 0.82 
    T_congelacion = -2.0 
    tip_texto = "El mango es rico en azúcares reductores. Concentrarlo por frío evita la reacción de Maillard (oscurecimiento) y el sabor a 'caramelo quemado', manteniendo su vibrante color amarillo-naranja intacto."
else: 
    Cp_nectar = 3.7  
    porcentaje_agua = 0.88 
    T_congelacion = -3.0 
    tip_texto = "El maracuyá posee compuestos aromáticos (ésteres) extremadamente volátiles. La crioconcentración asegura que estos no se evaporen, conservando su aroma tropical intenso y su acidez característica."

Q_sensible = masa_kg * Cp_nectar * (T_inicial - T_congelacion)
masa_agua = masa_kg * porcentaje_agua
Q_latente = (masa_agua * porcentaje_agua_congelar) * Calor_latente_hielo
Q_L = Q_sensible + Q_latente 

W_ideal_kwh = (Q_L / COP_ideal) / 3600
W_real_kwh = (Q_L / COP_real) / 3600

# ==========================================
# 4. PESTAÑAS DEL DASHBOARD
# ==========================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "⚙️ Máquina de Carnot", 
    "📈 Diagrama T-S", 
    "🧊 Calorimetría", 
    "⚡ Costo Energético",
    "🛡️ Calidad Nutricional"
])

with tab1:
    st.subheader("Análisis del Ciclo Ideal (1ra y 2da Ley)")
    c1, c2, c3 = st.columns([1, 1, 1.5])
    c1.metric("Depósito Caliente (TH)", f"{TH_K:.2f} K")
    c2.metric("Depósito Frío (TC)", f"{TC_K:.2f} K")
    
    # EFECTO WOW 2: Tacómetro Industrial
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = COP_ideal,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Límite COP Máximo", 'font': {'color': 'black', 'size': 14}},
        gauge = {
            'axis': {'range': [None, 10], 'tickwidth': 1, 'tickcolor': "black"},
            'bar': {'color': "#0288d1"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 3], 'color': "#ffcdd2"},
                {'range': [3, 6], 'color': "#fff9c4"},
                {'range': [6, 10], 'color': "#c8e6c9"}]
        }
    ))
    fig_gauge.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=10), paper_bgcolor='rgba(0,0,0,0)', font=dict(color="black"))
    with c3:
        st.plotly_chart(fig_gauge, use_container_width=True, theme=None)
    
    tc_array = np.linspace(-40, 0, 100)
    cop_array = (tc_array + 273.15) / (TH_K - (tc_array + 273.15))
    
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=tc_array, y=cop_array, mode='lines', line=dict(color='#e65100', width=4), name='COP Ideal'))
    fig1.add_trace(go.Scatter(x=[t_fria], y=[COP_ideal], mode='markers', marker=dict(color='black', size=12), name='Operación Real'))
    fig1.update_layout(title="Influencia del frío en el Coeficiente de Desempeño", xaxis_title="Temperatura TC (°C)", yaxis_title="COP", 
                       plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color="black"))
    st.plotly_chart(fig1, use_container_width=True, theme=None)

with tab2:
    st.subheader("Diagrama Termodinámico Temperatura-Entropía (T-S)")
    
    fig_ts = go.Figure()
    fig_ts.add_trace(go.Scatter(x=[1, 4, 4, 1, 1], y=[TC_K, TC_K, TH_K, TH_K, TC_K], 
                                fill='toself', fillcolor='rgba(255, 152, 0, 0.2)', 
                                line=dict(color='#e65100', width=3), name="Ciclo de Carnot"))
    
    fig_ts.add_annotation(x=2.5, y=TC_K, text="Absorción de Calor (Evaporador)", showarrow=True, ax=0, ay=40)
    fig_ts.add_annotation(x=2.5, y=TH_K, text="Rechazo de Calor (Condensador)", showarrow=True, ax=0, ay=-40)
    fig_ts.add_annotation(x=4, y=(TH_K+TC_K)/2, text="Compresión", showarrow=True, ax=40, ay=0)
    
    fig_ts.update_layout(xaxis_title="Entropía (S)", yaxis_title="Temperatura (K)", 
                         yaxis=dict(range=[TC_K - 20, TH_K + 20]), showlegend=False, 
                         plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color="black"))
    st.plotly_chart(fig_ts, use_container_width=True, theme=None)

with tab3:
    st.subheader(f"Demanda Térmica: {producto}")
    r1, r2, r3 = st.columns(3)
    r1.metric("Calor Sensible (Enfriar)", f"{Q_sensible:,.0f} kJ")
    r2.metric("Calor Latente (Congelar)", f"{Q_latente:,.0f} kJ")
    r3.metric("Carga Térmica (QL)", f"{Q_L:,.0f} kJ")
    
    fig2 = go.Figure(data=[go.Pie(labels=['Calor Sensible', 'Calor Latente (Cristalización)'], 
                                  values=[Q_sensible, Q_latente], hole=.4, marker_colors=['#ffcc80', '#e65100'])])
    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="black"))
    st.plotly_chart(fig2, use_container_width=True, theme=None)

with tab4:
    st.subheader("Ineficiencia del Compresor (Gasto Eléctrico)")
    colA, colB = st.columns(2)
    with colA:
        st.info(f"**Trabajo Teórico (Máquina Perfecta):**\n### {W_ideal_kwh:,.1f} kWh")
        st.error(f"**Trabajo Real (Compresor Industrial):**\n### {W_real_kwh:,.1f} kWh")
    
    with colB:
        costo_kwh = st.number_input("Tarifa Eléctrica (Soles/kWh):", value=0.65, step=0.05)
        ahorro_perdido = (W_real_kwh - W_ideal_kwh) * costo_kwh
        st.success(f"**Costo Total:** S/ {W_real_kwh * costo_kwh:,.2f}")
        st.warning(f"**Pérdida por Entropía:** S/ {ahorro_perdido:,.2f}")

with tab5:
    st.subheader("Beneficio Agroindustrial: Preservación de Vitamina C")
    
    temp_array = ['Crioconcentración (-15°C)', 'Evaporación al Vacío (60°C)', 'Evaporación Abierta (95°C)']
    retencion = [98, 65, 15]
    
    fig3 = go.Figure(go.Bar(x=retencion, y=temp_array, orientation='h', 
                            marker_color=['#4caf50', '#ff9800', '#f44336'],
                            text=[f"{v}% Retención" for v in retencion], textposition='auto'))
    fig3.update_layout(title="Retención de Ácido Ascórbico (Vitamina C) según Proceso", 
                       xaxis_title="% de Vitamina C Retenida", yaxis_title="Tecnología de Concentración",
                       plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=300, font=dict(color="black"))
    st.plotly_chart(fig3, use_container_width=True, theme=None)

# ==========================================
# 5. EXPORTACIÓN DE RESULTADOS Y TIP FINAL
# ==========================================
st.markdown("---")

# Aquí se muestra el Tip Agroindustrial dinámico
st.info(f"💡 **Tip Agroindustrial ({producto}):** {tip_texto}")

reporte_texto = f"""
=========================================
 REPORTE TÉCNICO: CRIO-CARNOT PRO
=========================================
Producto Evaluado: {producto}
Masa del Lote: {masa_kg:,.0f} kg

PARÁMETROS TERMODINÁMICOS:
- Temp. Condensador (TH): {t_caliente} °C ({TH_K:.2f} K)
- Temp. Evaporador (TC): {t_fria} °C ({TC_K:.2f} K)
- Límite de Carnot (COP Ideal): {COP_ideal:.2f}
- Eficiencia del Compresor: {eficiencia_2da_ley*100}%

CALORIMETRÍA:
- Calor Sensible: {Q_sensible:,.2f} kJ
- Calor Latente: {Q_latente:,.2f} kJ
- Carga Térmica Total: {Q_L:,.2f} kJ

GASTO ENERGÉTICO REAL: {W_real_kwh:,.2f} kWh
=========================================
Generado por Simulador Agroindustrial.
"""

col_vacia, col_boton, col_vacia2 = st.columns([1, 2, 1])
with col_boton:
    st.download_button(
        label="📥 Descargar Reporte Técnico del Lote (.txt)",
        data=reporte_texto,
        file_name=f"Reporte_Crio_{producto.split()[2]}.txt",
        mime="text/plain",
        use_container_width=True
    )
