import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ==========================================
# 1. CONFIGURACIÓN Y DISEÑO AGROINDUSTRIAL
# ==========================================
st.set_page_config(layout="wide", page_title="Thermo-Agro Pro", page_icon="🌾")

st.markdown("""
<style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=2000&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
    }
    
    .block-container, [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.96) !important;
    }
    
    .block-container {
        border-radius: 20px;
        padding: 2rem;
        margin-top: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25);
    }
    
    h1, h2, h3, p, label, .stMarkdown, span {
        color: #1b4332 !important;
    }
    
    div[data-testid="metric-container"] {
        background-color: rgba(45, 106, 79, 0.08);
        border: 1px solid rgba(45, 106, 79, 0.3);
        padding: 12px 16px;
        border-radius: 12px;
        border-left: 6px solid #2d6a4f;
    }
    div[data-testid="stMetricValue"] > div { color: #1b4332 !important; font-weight: 800; }
    
    .main-title { text-align: center; color: #1b4332 !important; font-weight: 900; padding-bottom: 5px; font-family: sans-serif; }
    
    .stTabs [data-baseweb="tab"] { font-weight: 700; color: #40916c !important; background-color: transparent; }
    .stTabs [aria-selected="true"] { border-bottom: 4px solid #2d6a4f !important; color: #1b4332 !important; background-color: rgba(45,106,79,0.08);}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🌾 Thermo-Agro Pro: Máquinas Térmicas</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>Simulador de Generación de Energía con Biomasa Agroindustrial (Integrante 2)</b></p>", unsafe_allow_html=True)

# ==========================================
# 2. GESTIÓN DE ESTADO (SESSION STATE SEGURO)
# ==========================================
if 'slider_ta' not in st.session_state: st.session_state['slider_ta'] = 450.0
if 'slider_tb' not in st.session_state: st.session_state['slider_tb'] = 50.0
if 'input_qa' not in st.session_state: st.session_state['input_qa'] = 12000.0
if 'input_w' not in st.session_state: st.session_state['input_w'] = 3000.0

def reset_ejercicio1():
    st.session_state['slider_ta'] = 450.0
    st.session_state['slider_tb'] = 50.0
    st.session_state['input_qa'] = 12000.0
    st.session_state['input_w'] = 3000.0

# ==========================================
# 3. PANEL LATERAL
# ==========================================
st.sidebar.header("⚙️ Parámetros de la Máquina")

st.sidebar.button("🌾 Cargar Ejercicio 1 (Separata)", on_click=reset_ejercicio1, use_container_width=True)
st.sidebar.markdown("---")

biomasa_opcion = st.sidebar.selectbox(
    "Combustible Agrícola (Caldera):", 
    ["Cascarilla de Arroz (PCI ~15 MJ/kg)", "Bagazo de Caña (PCI ~17 MJ/kg)", "Cáscara de Cacao (PCI ~16 MJ/kg)"]
)

t_caliente = st.sidebar.slider("Temp. Caldera / Vapor (TA) °C:", 150.0, 600.0, key='slider_ta', step=10.0)
t_fria = st.sidebar.slider("Temp. Condensador (TB) °C:", 20.0, 90.0, key='slider_tb', step=5.0)

q_entrada = st.sidebar.number_input("Calor Suministrado (QA) [kJ]:", min_value=1000.0, max_value=50000.0, key='input_qa', step=1000.0)

max_w_permitido = float(q_entrada)
if st.session_state['input_w'] > max_w_permitido:
    st.session_state['input_w'] = max_w_permitido

trabajo_real = st.sidebar.number_input("Trabajo Producido (W) [kJ]:", min_value=100.0, max_value=max_w_permitido, key='input_w', step=500.0)

# ==========================================
# 4. CÁLCULOS TERMODINÁMICOS
# ==========================================
TA_K = t_caliente + 273.15
TB_K = t_fria + 273.15

eta_real = (trabajo_real / q_entrada) * 100.0
QB = q_entrada - trabajo_real
eta_carnot = (1.0 - (TB_K / TA_K)) * 100.0
clausius_sum = (q_entrada / TA_K) - (QB / TB_K)

pci_map = {
    "Cascarilla de Arroz (PCI ~15 MJ/kg)": 15000.0,
    "Bagazo de Caña (PCI ~17 MJ/kg)": 17000.0,
    "Cáscara de Cacao (PCI ~16 MJ/kg)": 16000.0
}
pci_val = pci_map[biomasa_opcion]
kg_biomasa = q_entrada / pci_val

# ==========================================
# 5. PESTAÑAS DEL DASHBOARD
# ==========================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏭 Flujo de Energía (Máquina)",
    "⚙️ Eficiencias (Tacómetros)", 
    "⚖️ Desigualdad de Clausius", 
    "📈 Diagrama T-S", 
    "🌾 Biomasa"
])

with tab1:
    st.subheader("Esquema Interactivo de la Planta Térmica (Segunda Ley)")
    
    # EFECTO WOW: Diagrama Sankey de la Máquina Térmica
    fig_sankey = go.Figure(data=[go.Sankey(
        node = dict(
          pad = 30,
          thickness = 30,
          line = dict(color = "black", width = 0.5),
          label = [f"Caldera (TA: {t_caliente}°C)", "Turbina (Máquina)", f"Trabajo Útil (W: {trabajo_real:,.0f} kJ)", f"Condensador (QB: {QB:,.0f} kJ)"],
          color = ["#d62828", "#f77f00", "#2a9d8f", "#003049"]
        ),
        link = dict(
          source = [0, 1, 1], # Caldera -> Turbina -> W & QB
          target = [1, 2, 3], 
          value = [q_entrada, trabajo_real, QB],
          color = ["rgba(214, 40, 40, 0.4)", "rgba(42, 157, 143, 0.4)", "rgba(0, 48, 73, 0.4)"]
      ))])
    
    fig_sankey.update_layout(height=350, font_size=14, margin=dict(l=0, r=0, t=30, b=0), paper_bgcolor='rgba(0,0,0,0)', font=dict(color="black"))
    st.plotly_chart(fig_sankey, use_container_width=True, theme=None)
    
    st.info("💡 **Vista en vivo:** El grosor de las líneas representa la cantidad de energía. Observen visualmente cómo la Segunda Ley obliga a la turbina a desechar gran parte de la energía (línea azul) hacia el condensador, limitando el trabajo generado (línea verde).")

with tab2:
    st.subheader("Balance Termodinámico y Comparación de Eficiencias")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Calor Recibido (QA)", f"{q_entrada:,.0f} kJ")
    col2.metric("Trabajo Útil (W)", f"{trabajo_real:,.0f} kJ")
    col3.metric("Calor Rechazado (QB)", f"{QB:,.0f} kJ")
    col4.metric("Temperaturas (K)", f"TA: {TA_K:.2f}K | TB: {TB_K:.2f}K")
    
    c_gauge1, c_gauge2 = st.columns(2)
    fig_gauge_real = go.Figure(go.Indicator(
        mode = "gauge+number", value = eta_real, number = {'suffix': "%"}, domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Eficiencia Real (η)", 'font': {'color': 'black', 'size': 15}},
        gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#2d6a4f"}, 'steps': [{'range': [0, eta_carnot], 'color': "#d8f3dc"}, {'range': [eta_carnot, 100], 'color': "#ffccd5"}]}
    ))
    fig_gauge_real.update_layout(height=220, margin=dict(l=20, r=20, t=40, b=10), paper_bgcolor='rgba(0,0,0,0)')
    with c_gauge1: st.plotly_chart(fig_gauge_real, use_container_width=True, theme=None)
        
    fig_gauge_carnot = go.Figure(go.Indicator(
        mode = "gauge+number", value = eta_carnot, number = {'suffix': "%"}, domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Límite Teórico de Carnot", 'font': {'color': 'black', 'size': 15}},
        gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#1b4332"}, 'steps': [{'range': [0, 100], 'color': "#e9ecef"}]}
    ))
    fig_gauge_carnot.update_layout(height=220, margin=dict(l=20, r=20, t=40, b=10), paper_bgcolor='rgba(0,0,0,0)')
    with c_gauge2: st.plotly_chart(fig_gauge_carnot, use_container_width=True, theme=None)

with tab3:
    st.subheader("Evaluación de la Segunda Ley (Criterio de Clausius)")
    colA, colB = st.columns([1.2, 1])
    with colA:
        st.write("### Integración de Clausius:")
        st.latex(r"\oint \frac{\delta Q}{T} = \frac{Q_A}{T_A} - \frac{Q_B}{T_B}")
        st.latex(f"\\oint \\frac{{\\delta Q}}{{T}} = \\frac{{{q_entrada:,.0f}}}{{{TA_K:.2f}}} - \\frac{{{QB:,.0f}}}{{{TB_K:.2f}}} = {clausius_sum:.3f} \\text{{ kJ/K}}")
    with colB:
        st.write("### Diagnóstico Termodinámico:")
        if eta_real > eta_carnot + 0.001: st.error("❌ **PROCESO IMPOSIBLE**: Eficiencia real supera a Carnot. Viola la 2da Ley.")
        elif abs(clausius_sum) < 0.001 or abs(eta_real - eta_carnot) < 0.001: st.success("🟢 **CICLO REVERSIBLE (IDEAL)**: Máquina perfecta (∮ dQ/T = 0).")
        else: st.warning("🟡 **CICLO IRREVERSIBLE (MÁQUINA REAL)**: Como ∮ dQ/T < 0 (-11.3 kJ/K), se confirma pérdida por entropía.")

with tab4:
    st.subheader("Diagrama Temperatura - Entropía (T-S)")
    fig_ts = go.Figure()
    fig_ts.add_trace(go.Scatter(x=[1, 4, 4, 1, 1], y=[TB_K, TB_K, TA_K, TA_K, TB_K], fill='toself', fillcolor='rgba(45, 106, 79, 0.15)', line=dict(color='#2d6a4f', width=3), name="Ciclo Carnot"))
    fig_ts.add_annotation(x=2.5, y=TA_K, text="Caldera: Entrada QA", showarrow=True, ax=0, ay=-30)
    fig_ts.add_annotation(x=2.5, y=TB_K, text="Condensador: Rechazo QB", showarrow=True, ax=0, ay=30)
    fig_ts.add_annotation(x=4, y=(TA_K+TB_K)/2, text="Turbina: Trabajo W", showarrow=True, ax=40, ay=0)
    fig_ts.update_layout(xaxis_title="Entropía (S)", yaxis_title="Temperatura (K)", yaxis=dict(range=[TB_K - 30, TA_K + 30]), showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color="black"))
    st.plotly_chart(fig_ts, use_container_width=True, theme=None)

with tab5:
    st.subheader("Aprovechamiento de Residuos Agrícolas (Biomasa)")
    b1, b2, b3 = st.columns(3)
    b1.metric("Biomasa Seleccionada", biomasa_opcion.split('(')[0])
    b2.metric("Poder Calorífico (PCI)", f"{pci_val/1000:.1f} MJ/kg")
    b3.metric("Masa de Biomasa Requerida", f"{kg_biomasa:.3f} kg")
    st.success(f"💡 **Aplicación Real:** En molinos arroceros de la costa peruana, quemar **cascarilla de arroz** para alimentar la caldera reduce el gasto en diésel industrial y promueve la economía circular.")

# ==========================================
# 6. EXPORTACIÓN DE RESULTADOS A EXCEL (.CSV)
# ==========================================
st.markdown("---")
reporte_csv = f"""REPORTE TÉCNICO: MÁQUINAS TÉRMICAS Y CARNOT (EJERCICIO 1)

CATEGORÍA,PARÁMETRO,VALOR,UNIDAD
1. Condición Operativa,Temperatura Fuente Caliente (TA),{t_caliente},°C
1. Condición Operativa,Temperatura Fuente Fría (TB),{t_fria},°C
2. Energética,Calor Suministrado (QA),"{q_entrada:,.2f}",kJ
2. Energética,Trabajo Útil Producido (W),"{trabajo_real:,.2f}",kJ
2. Energética,Calor Rechazado (QB),"{QB:,.2f}",kJ
3. Eficiencias,Eficiencia Térmica Real (eta),{eta_real:.2f},%
3. Eficiencias,Eficiencia Máxima de Carnot (eta_max),{eta_carnot:.2f},%
4. Segunda Ley,Resultado Integral de Clausius,{clausius_sum:.4f},kJ/K
5. Biomasa,Tipo de Combustible,{biomasa_opcion.split('(')[0]},
5. Biomasa,Masa Requerida por Ciclo,{kg_biomasa:.4f},kg
"""
col_vacia, col_boton, col_vacia2 = st.columns([1, 2, 1])
with col_boton:
    st.download_button(label="📊 Descargar Reporte en Excel (.csv)", data=reporte_csv.encode('utf-8-sig'), file_name="Reporte_Maquina_Termica_Ejercicio1.csv", mime="text/csv", use_container_width=True)
