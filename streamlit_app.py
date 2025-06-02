#!/usr/bin/env python3
"""
Sistema de Gestión de Proyectos de Construcción - Icon Bay Torres
Versión Python con Streamlit para interfaz web profesional
Autor: Sistema desarrollado para gestión de proyectos
Fecha: 2025
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import io
import base64

# Configuración de la página
st.set_page_config(
    page_title="Icon Bay Torres - Sistema de Gestión",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejorar el diseño
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    .kpi-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #4F46E5;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .metric-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .category-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    .status-pending { background-color: #fef3c7; color: #92400e; }
    .status-completed { background-color: #d1fae5; color: #065f46; }
    .status-delayed { background-color: #fecaca; color: #991b1b; }
    
    /* Ocultar el menú de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

class ConstructionManager:
    def __init__(self):
        self.load_data()
    
    def load_data(self):
        """Carga los datos de los 94 hitos del proyecto Icon Bay Torres"""
        self.hitos_data = [
            {"id": 1, "numero": 1, "titulo": "Excavacion y relleno", "mes_programado": 1, "mes_real": None, "avance": 0, "categoria": "Excavación y Cimentación"},
            {"id": 2, "numero": 2, "titulo": "Construcción de cimentación", "mes_programado": 2, "mes_real": None, "avance": 0, "categoria": "Excavación y Cimentación"},
            {"id": 3, "numero": 3, "titulo": "Construccion de cimentacion compensada y fundicion de PB", "mes_programado": 2, "mes_real": None, "avance": 0, "categoria": "Excavación y Cimentación"},
            {"id": 4, "numero": 4, "titulo": "Fundición de piso 1", "mes_programado": 2, "mes_real": None, "avance": 0, "categoria": "Estructura"},
            {"id": 5, "numero": 5, "titulo": "Fundición de piso 2", "mes_programado": 3, "mes_real": None, "avance": 0, "categoria": "Estructura"},
            {"id": 6, "numero": 6, "titulo": "Fundición de piso 3", "mes_programado": 4, "mes_real": None, "avance": 0, "categoria": "Estructura"},
            {"id": 7, "numero": 7, "titulo": "Fundicion de cubierta", "mes_programado": 5, "mes_real": None, "avance": 0, "categoria": "Estructura"},
            {"id": 8, "numero": 8, "titulo": "Alero y otros elementos de hormigon", "mes_programado": 7, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 9, "numero": 9, "titulo": "Paredes PB y Piso 1", "mes_programado": 5, "mes_real": None, "avance": 0, "categoria": "Estructura"},
            {"id": 10, "numero": 10, "titulo": "Paredes P2 y P3", "mes_programado": 6, "mes_real": None, "avance": 0, "categoria": "Paredes y Muros"},
            {"id": 11, "numero": 11, "titulo": "Enlucido Interior PB y P1", "mes_programado": 6, "mes_real": None, "avance": 0, "categoria": "Enlucidos"},
            {"id": 12, "numero": 12, "titulo": "Enlucido Interior P2, P3 y Cubierta", "mes_programado": 7, "mes_real": None, "avance": 0, "categoria": "Estructura"},
            {"id": 13, "numero": 13, "titulo": "Otras paredes", "mes_programado": 7, "mes_real": None, "avance": 0, "categoria": "Paredes y Muros"},
            {"id": 14, "numero": 14, "titulo": "Otros enlucidos, filos y cuadres de boquetes", "mes_programado": 8, "mes_real": None, "avance": 0, "categoria": "Enlucidos"},
            {"id": 15, "numero": 15, "titulo": "Enlucido Exterior Posterior", "mes_programado": 7, "mes_real": None, "avance": 0, "categoria": "Enlucidos"},
            {"id": 16, "numero": 16, "titulo": "Enlucido Exterior Frontal y laterales", "mes_programado": 8, "mes_real": None, "avance": 0, "categoria": "Enlucidos"},
            {"id": 17, "numero": 17, "titulo": "Enlucido piso", "mes_programado": 7, "mes_real": None, "avance": 0, "categoria": "Estructura"},
            {"id": 18, "numero": 18, "titulo": "Primera cara de Paredes PB y Piso 1", "mes_programado": 7, "mes_real": None, "avance": 0, "categoria": "Estructura"},
            {"id": 19, "numero": 19, "titulo": "Primera cara de paredes P2 y P3", "mes_programado": 8, "mes_real": None, "avance": 0, "categoria": "Paredes y Muros"},
            {"id": 20, "numero": 20, "titulo": "Cierre de paredes con sus instalaciones", "mes_programado": 9, "mes_real": None, "avance": 0, "categoria": "Paredes y Muros"},
            {"id": 21, "numero": 21, "titulo": "Compra De Revestimientos", "mes_programado": 4, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 22, "numero": 22, "titulo": "Instalacion de revestimiento piso y paredes PB P1", "mes_programado": 8, "mes_real": None, "avance": 0, "categoria": "Estructura"},
            {"id": 23, "numero": 23, "titulo": "Instalacion de revestimiento piso y paredes P2 P3", "mes_programado": 9, "mes_real": None, "avance": 0, "categoria": "Estructura"},
            {"id": 24, "numero": 24, "titulo": "Instalacion mesones cocina y baños", "mes_programado": 13, "mes_real": None, "avance": 0, "categoria": "Instalaciones"},
            {"id": 25, "numero": 25, "titulo": "Tumbado PB, P1", "mes_programado": 8, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 26, "numero": 26, "titulo": "Tumbado P2, P3", "mes_programado": 9, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 27, "numero": 27, "titulo": "Tumbado Madereado, Lobby y Otros", "mes_programado": 13, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 28, "numero": 28, "titulo": "Primera mano de acabados de paredes", "mes_programado": 12, "mes_real": None, "avance": 0, "categoria": "Paredes y Muros"},
            {"id": 29, "numero": 29, "titulo": "Segunda Mano y acabados final", "mes_programado": 13, "mes_real": None, "avance": 0, "categoria": "Acabados"},
            {"id": 30, "numero": 30, "titulo": "Pintura Exterior", "mes_programado": 12, "mes_real": None, "avance": 0, "categoria": "Acabados"},
            {"id": 31, "numero": 31, "titulo": "Materiales de aluminio y vidrio", "mes_programado": 6, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 32, "numero": 32, "titulo": "Montaje de aluminio y vidrio frontal y posterior", "mes_programado": 10, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 33, "numero": 33, "titulo": "Montaje de aluminio y vidrio Laterales", "mes_programado": 11, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 34, "numero": 34, "titulo": "Puertas piso Pb y P1", "mes_programado": 11, "mes_real": None, "avance": 0, "categoria": "Estructura"},
            {"id": 35, "numero": 35, "titulo": "Puertas piso P 2, P3 y closet", "mes_programado": 12, "mes_real": None, "avance": 0, "categoria": "Estructura"},
            {"id": 36, "numero": 36, "titulo": "Pasamano de vidrio", "mes_programado": 11, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 37, "numero": 37, "titulo": "Viga I", "mes_programado": 8, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 38, "numero": 38, "titulo": "Otras carpinterias", "mes_programado": 10, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 39, "numero": 39, "titulo": "Compra Piezas Sanitarias", "mes_programado": 11, "mes_real": None, "avance": 0, "categoria": "Instalaciones"},
            {"id": 40, "numero": 40, "titulo": "Impermeabilizacion de Cubierta", "mes_programado": 10, "mes_real": None, "avance": 0, "categoria": "Estructura"},
            {"id": 41, "numero": 41, "titulo": "Impermeabilizacion de duchas y marcos", "mes_programado": 9, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 42, "numero": 42, "titulo": "Otras imperemabiliaciones", "mes_programado": 11, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 43, "numero": 43, "titulo": "Fabricacion de cocinas 60%", "mes_programado": 4, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 44, "numero": 44, "titulo": "Despacho Cocinas 4 dept 20%", "mes_programado": 11, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 45, "numero": 45, "titulo": "Despacho Cocinas 4 dept 20%", "mes_programado": 12, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 46, "numero": 46, "titulo": "Instalaciones verticales AP PB Y P1", "mes_programado": 7, "mes_real": None, "avance": 0, "categoria": "Instalaciones"},
            {"id": 47, "numero": 47, "titulo": "Instalaciones en tumbados AP PB Y P1", "mes_programado": 8, "mes_real": None, "avance": 0, "categoria": "Instalaciones"},
            {"id": 48, "numero": 48, "titulo": "Instalaciones verticales AASS PB Y P1", "mes_programado": 7, "mes_real": None, "avance": 0, "categoria": "Instalaciones"},
            {"id": 49, "numero": 49, "titulo": "Instalaciones en tumbados AASS PB Y P1", "mes_programado": 8, "mes_real": None, "avance": 0, "categoria": "Instalaciones"},
            {"id": 50, "numero": 50, "titulo": "Instalaciones verticales AALL PB Y P1", "mes_programado": 7, "mes_real": None, "avance": 0, "categoria": "Instalaciones"},
            {"id": 51, "numero": 51, "titulo": "Instalaciones en tumbados AALL PB Y P1", "mes_programado": 8, "mes_real": None, "avance": 0, "categoria": "Instalaciones"},
            {"id": 52, "numero": 52, "titulo": "Instalaciones verticales AP P2 Y P3", "mes_programado": 8, "mes_real": None, "avance": 0, "categoria": "Instalaciones"},
            {"id": 53, "numero": 53, "titulo": "Instalaciones en tumbados AP P2 Y P3", "mes_programado": 9, "mes_real": None, "avance": 0, "categoria": "Instalaciones"},
            {"id": 54, "numero": 54, "titulo": "Instalaciones verticales AASS P2 Y P3", "mes_programado": 8, "mes_real": None, "avance": 0, "categoria": "Instalaciones"},
            {"id": 55, "numero": 55, "titulo": "Instalaciones en tumbados AASS P2 Y P3", "mes_programado": 9, "mes_real": None, "avance": 0, "categoria": "Instalaciones"},
            {"id": 56, "numero": 56, "titulo": "Instalaciones verticales AALL P2 Y P3", "mes_programado": 8, "mes_real": None, "avance": 0, "categoria": "Instalaciones"},
            {"id": 57, "numero": 57, "titulo": "Instalaciones en tumbados AALL P2 Y P3", "mes_programado": 9, "mes_real": None, "avance": 0, "categoria": "Instalaciones"},
            {"id": 58, "numero": 58, "titulo": "Canalizacion exterior AASS", "mes_programado": 10, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 59, "numero": 59, "titulo": "Canalizacion exterior AALL", "mes_programado": 10, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 60, "numero": 60, "titulo": "Canalizacion exterior AP", "mes_programado": 10, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 61, "numero": 61, "titulo": "Bombas", "mes_programado": 13, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 62, "numero": 62, "titulo": "Tableros electricos", "mes_programado": 10, "mes_real": None, "avance": 0, "categoria": "Instalaciones"},
            {"id": 63, "numero": 63, "titulo": "Acometidas principales", "mes_programado": 11, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 64, "numero": 64, "titulo": "Paneles electricos", "mes_programado": 8, "mes_real": None, "avance": 0, "categoria": "Instalaciones"},
            {"id": 65, "numero": 65, "titulo": "Canaletas", "mes_programado": 8, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 66, "numero": 66, "titulo": "Tuberias circuitos derivados Pb P1", "mes_programado": 7, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 67, "numero": 67, "titulo": "Tuberias circuitos derivados P2 P3", "mes_programado": 8, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 68, "numero": 68, "titulo": "Cableado circuitos PB P1", "mes_programado": 7, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 69, "numero": 69, "titulo": "Cableado circuitos P2 P3", "mes_programado": 8, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 70, "numero": 70, "titulo": "Tuberias electronica PB P1", "mes_programado": 7, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 71, "numero": 71, "titulo": "Cableado electronica PB P1", "mes_programado": 7, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 72, "numero": 72, "titulo": "Equipos electronicos PB P1", "mes_programado": 7, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 73, "numero": 73, "titulo": "Tuberias electronica P2 P3", "mes_programado": 8, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 74, "numero": 74, "titulo": "Cableado electronica P2 P3", "mes_programado": 8, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 75, "numero": 75, "titulo": "Equipos electronicos P2 P3", "mes_programado": 8, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 76, "numero": 76, "titulo": "Ducteria extraccion PB P1", "mes_programado": 7, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 77, "numero": 77, "titulo": "Ducteria de extraccion P2 P3", "mes_programado": 8, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 78, "numero": 78, "titulo": "Paso tuberia cobre PB P1", "mes_programado": 7, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 79, "numero": 79, "titulo": "Paso tuberia cobre P2 P3", "mes_programado": 8, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 80, "numero": 80, "titulo": "Montaje de extractores", "mes_programado": 13, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 81, "numero": 81, "titulo": "Fabricacion ascensor", "mes_programado": 7, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 82, "numero": 82, "titulo": "Entrega y puesta en marcha ascensor", "mes_programado": 13, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 83, "numero": 83, "titulo": "Tuberia empotrada GLP", "mes_programado": 8, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 84, "numero": 84, "titulo": "Dotacion Calentadores", "mes_programado": 13, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 85, "numero": 85, "titulo": "Cajetines y pruebas GLP", "mes_programado": 12, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 86, "numero": 86, "titulo": "Pasamano metalico", "mes_programado": 13, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 87, "numero": 87, "titulo": "Puertas y louver aluminio", "mes_programado": 13, "mes_real": None, "avance": 0, "categoria": "Acabados"},
            {"id": 88, "numero": 88, "titulo": "Construccion de cisterna", "mes_programado": 7, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 89, "numero": 89, "titulo": "Cerramiento", "mes_programado": 10, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 90, "numero": 90, "titulo": "Bodega", "mes_programado": 11, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 91, "numero": 91, "titulo": "Varios de obra", "mes_programado": 10, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 92, "numero": 92, "titulo": "Topes y numeracion de parqueo", "mes_programado": 13, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 93, "numero": 93, "titulo": "Tuberia sistema contra incendio", "mes_programado": 9, "mes_real": None, "avance": 0, "categoria": "Otros"},
            {"id": 94, "numero": 94, "titulo": "Luminarias", "mes_programado": 13, "mes_real": None, "avance": 0, "categoria": "Otros"}
        ]
        
        self.df = pd.DataFrame(self.hitos_data)
        self.project_info = {
            "torre": "13B",
            "area": 1563.32,
            "duracion_meses": 13,
            "fecha_inicio": datetime.now(),
            "cliente": "Icon Bay Torres"
        }
    
    def calculate_kpis(self):
        """Calcula los KPIs principales del proyecto"""
        total_hitos = len(self.df)
        hitos_completados = len(self.df[self.df['avance'] == 100])
        avance_global = self.df['avance'].mean()
        hitos_con_retraso = len(self.df[(self.df['mes_real'].notna()) & 
                                      (self.df['mes_real'] > self.df['mes_programado'])])
        
        return {
            "total_hitos": total_hitos,
            "hitos_completados": hitos_completados,
            "avance_global": avance_global,
            "hitos_con_retraso": hitos_con_retraso,
            "porcentaje_completado": (hitos_completados / total_hitos) * 100
        }
    
    def get_timeline_data(self):
        """Genera datos para el gráfico de línea temporal"""
        timeline_data = []
        for mes in range(1, 14):
            hitos_mes = self.df[self.df['mes_programado'] <= mes]
            if len(hitos_mes) > 0:
                avance_acumulado = hitos_mes['avance'].mean()
                hitos_completados = len(hitos_mes[hitos_mes['avance'] == 100])
            else:
                avance_acumulado = 0
                hitos_completados = 0
            
            timeline_data.append({
                "mes": f"Mes {mes}",
                "avance_acumulado": avance_acumulado,
                "hitos_completados": hitos_completados
            })
        
        return pd.DataFrame(timeline_data)
    
    def get_category_distribution(self):
        """Obtiene la distribución por categorías"""
        category_stats = self.df.groupby('categoria').agg({
            'id': 'count',
            'avance': ['mean', 'sum'],
            'mes_real': lambda x: x.notna().sum()
        }).round(2)
        
        category_stats.columns = ['total_hitos', 'avance_promedio', 'avance_total', 'completados']
        category_stats = category_stats.reset_index()
        
        return category_stats
    
    def export_to_csv(self):
        """Exporta los datos a CSV"""
        output = io.StringIO()
        self.df.to_csv(output, index=False, encoding='utf-8')
        return output.getvalue()

def main():
    # Inicializar el gestor de construcción
    if 'construction_manager' not in st.session_state:
        st.session_state.construction_manager = ConstructionManager()
    
    cm = st.session_state.construction_manager
    
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🏗️ Sistema de Gestión de Construcción</h1>
        <h2>Icon Bay Torres</h2>
        <p>Gestión Profesional de Proyectos • 94 Hitos • 13 Meses • 1,563.32 m²</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar para configuración del proyecto
    with st.sidebar:
        st.header("⚙️ Configuración del Proyecto")
        
        torre = st.text_input("Torre", value=cm.project_info["torre"])
        area = st.number_input("Área (m²)", value=cm.project_info["area"], min_value=0.0)
        cliente = st.text_input("Cliente", value=cm.project_info["cliente"])
        
        st.header("📊 Filtros")
        categorias = ['Todas'] + list(cm.df['categoria'].unique())
        categoria_filtro = st.selectbox("Filtrar por Categoría", categorias)
        
        mes_analisis = st.selectbox("Mes de Análisis", 
                                   ['Todos'] + [f"Mes {i}" for i in range(1, 14)])
        
        st.header("📁 Exportar Datos")
        if st.button("📥 Descargar CSV", use_container_width=True):
            csv_data = cm.export_to_csv()
            st.download_button(
                label="💾 Guardar Archivo CSV",
                data=csv_data,
                file_name=f"Icon_Bay_Torres_{torre}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    # Calcular KPIs
    kpis = cm.calculate_kpis()
    
    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📋 Gestión de Hitos", "📈 Análisis", "⚙️ Configuración"])
    
    with tab1:
        st.header("Dashboard Ejecutivo")
        
        # KPIs principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="🎯 Avance Global",
                value=f"{kpis['avance_global']:.1f}%",
                delta=f"{kpis['porcentaje_completado']:.1f}% completado"
            )
        
        with col2:
            st.metric(
                label="📊 Total de Hitos",
                value=kpis['total_hitos'],
                delta=f"{kpis['hitos_completados']} completados"
            )
        
        with col3:
            st.metric(
                label="✅ Hitos Completados",
                value=kpis['hitos_completados'],
                delta=f"{kpis['total_hitos'] - kpis['hitos_completados']} pendientes"
            )
        
        with col4:
            st.metric(
                label="⚠️ Hitos con Retraso",
                value=kpis['hitos_con_retraso'],
                delta="Requieren atención" if kpis['hitos_con_retraso'] > 0 else "En tiempo"
            )
        
        st.markdown("---")
        
        # Gráficos principales
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Secuencia de Hitos (Primeros 20)")
            
            # Gráfico de barras para los primeros 20 hitos
            df_chart = cm.df.head(20).copy()
            df_chart['mes_real_display'] = df_chart['mes_real'].fillna(0)
            
            fig_bar = go.Figure()
            
            fig_bar.add_trace(go.Bar(
                name='Mes Programado',
                x=df_chart['numero'],
                y=df_chart['mes_programado'],
                marker_color='lightblue',
                text=df_chart['mes_programado'],
                textposition='auto'
            ))
            
            fig_bar.add_trace(go.Bar(
                name='Avance %',
                x=df_chart['numero'],
                y=df_chart['avance'],
                marker_color='lightgreen',
                text=df_chart['avance'].astype(str) + '%',
                textposition='auto',
                yaxis='y2'
            ))
            
            fig_bar.update_layout(
                title="Programación vs Avance por Hito",
                xaxis_title="Número de Hito",
                yaxis_title="Mes Programado",
                yaxis2=dict(title="Avance (%)", overlaying='y', side='right'),
                height=400,
                showlegend=True
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            st.subheader("📈 Progreso Temporal Acumulado")
            
            # Gráfico de línea temporal
            timeline_df = cm.get_timeline_data()
            
            fig_line = go.Figure()
            
            fig_line.add_trace(go.Scatter(
                x=timeline_df['mes'],
                y=timeline_df['avance_acumulado'],
                mode='lines+markers',
                name='Avance Acumulado (%)',
                line=dict(color='blue', width=3),
                marker=dict(size=8)
            ))
            
            fig_line.add_trace(go.Scatter(
                x=timeline_df['mes'],
                y=timeline_df['hitos_completados'],
                mode='lines+markers',
                name='Hitos Completados',
                line=dict(color='green', width=3),
                marker=dict(size=8),
                yaxis='y2'
            ))
            
            fig_line.update_layout(
                title="Evolución del Proyecto",
                xaxis_title="Periodo",
                yaxis_title="Avance Acumulado (%)",
                yaxis2=dict(title="Hitos Completados", overlaying='y', side='right'),
                height=400,
                showlegend=True
            )
            
            st.plotly_chart(fig_line, use_container_width=True)
        
        # Distribución por categorías
        st.subheader("🏗️ Distribución por Categorías")
        
        category_df = cm.get_category_distribution()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de pastel
            fig_pie = px.pie(
                category_df, 
                values='total_hitos', 
                names='categoria',
                title="Distribución de Hitos por Categoría",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Tabla de estadísticas por categoría
            st.markdown("**Estadísticas por Categoría:**")
            
            for _, row in category_df.iterrows():
                st.markdown(f"""
                <div class="kpi-card">
                    <strong>{row['categoria']}</strong><br>
                    📊 {row['total_hitos']} hitos • 
                    ✅ {row['completados']} completados • 
                    📈 {row['avance_promedio']:.1f}% avance promedio
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.header("📋 Gestión de Hitos")
        
        # Filtros y búsqueda
        col1, col2, col3 = st.columns(3)
        
        with col1:
            buscar = st.text_input("🔍 Buscar hito", placeholder="Ingrese título o número...")
        
        with col2:
            if categoria_filtro != 'Todas':
                df_filtrado = cm.df[cm.df['categoria'] == categoria_filtro]
            else:
                df_filtrado = cm.df.copy()
        
        with col3:
            ordenar_por = st.selectbox("Ordenar por", 
                                     ["numero", "mes_programado", "avance", "categoria"])
        
        # Aplicar filtros
        if buscar:
            df_filtrado = df_filtrado[
                df_filtrado['titulo'].str.contains(buscar, case=False, na=False) |
                df_filtrado['numero'].astype(str).str.contains(buscar, na=False)
            ]
        
        df_filtrado = df_filtrado.sort_values(ordenar_por)
        
        st.markdown(f"**Mostrando {len(df_filtrado)} de {len(cm.df)} hitos**")
        
        # Editor de hitos
        st.subheader("✏️ Editor de Hitos")
        
        # Paginación
        items_per_page = 20
        total_pages = (len(df_filtrado) + items_per_page - 1) // items_per_page
        
        if total_pages > 1:
            page = st.selectbox("Página", range(1, total_pages + 1)) - 1
        else:
            page = 0
        
        start_idx = page * items_per_page
        end_idx = start_idx + items_per_page
        df_page = df_filtrado.iloc[start_idx:end_idx]
        
        # Tabla editable
        edited_df = st.data_editor(
            df_page,
            column_config={
                "numero": st.column_config.NumberColumn("Hito #", disabled=True),
                "titulo": st.column_config.TextColumn("Título", width="large"),
                "categoria": st.column_config.SelectboxColumn(
                    "Categoría",
                    options=list(cm.df['categoria'].unique())
                ),
                "mes_programado": st.column_config.NumberColumn(
                    "Mes Programado", 
                    min_value=1, 
                    max_value=13
                ),
                "mes_real": st.column_config.NumberColumn(
                    "Mes Real", 
                    min_value=1, 
                    max_value=13
                ),
                "avance": st.column_config.ProgressColumn(
                    "Avance",
                    min_value=0,
                    max_value=100,
                    format="%d%%"
                )
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Botón para guardar cambios
        if st.button("💾 Guardar Cambios", type="primary"):
            # Actualizar los datos en el DataFrame principal
            for idx, row in edited_df.iterrows():
                original_idx = df_page.index[idx - start_idx] if idx >= start_idx else idx
                if original_idx in cm.df.index:
                    cm.df.loc[original_idx] = row
            st.success("✅ Cambios guardados exitosamente!")
            st.rerun()
    
    with tab3:
        st.header("📈 Análisis Avanzado")
        
        # Análisis de distribución temporal
        st.subheader("📅 Análisis de Distribución Temporal")
        
        # Distribución de hitos por mes
        monthly_dist = cm.df.groupby('mes_programado').size().reset_index()
        monthly_dist.columns = ['mes', 'cantidad_hitos']
        
        fig_monthly = px.bar(
            monthly_dist,
            x='mes',
            y='cantidad_hitos',
            title="Distribución de Actividades por Mes",
            labels={'mes': 'Mes', 'cantidad_hitos': 'Cantidad de Hitos'},
            color='cantidad_hitos',
            color_continuous_scale='Blues'
        )
        
        st.plotly_chart(fig_monthly, use_container_width=True)
        
        # Análisis de carga de trabajo
        st.subheader("⚖️ Análisis de Carga de Trabajo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            max_mes = monthly_dist.loc[monthly_dist['cantidad_hitos'].idxmax()]
            st.metric(
                "🔴 Mes con Mayor Carga",
                f"Mes {max_mes['mes']}",
                f"{max_mes['cantidad_hitos']} actividades"
            )
        
        with col2:
            avg_monthly = monthly_dist['cantidad_hitos'].mean()
            st.metric(
                "📊 Promedio Mensual",
                f"{avg_monthly:.1f} actividades",
                "por mes"
            )
        
        # Matriz de riesgo
        st.subheader("🚨 Matriz de Riesgo")
        
        # Crear matriz de riesgo basada en la concentración de actividades
        risk_analysis = monthly_dist.copy()
        risk_analysis['nivel_riesgo'] = pd.cut(
            risk_analysis['cantidad_hitos'],
            bins=[0, 5, 10, 20, float('inf')],
            labels=['Bajo', 'Medio', 'Alto', 'Crítico']
        )
        
        risk_colors = {'Bajo': 'green', 'Medio': 'yellow', 'Alto': 'orange', 'Crítico': 'red'}
        
        fig_risk = px.bar(
            risk_analysis,
            x='mes',
            y='cantidad_hitos',
            color='nivel_riesgo',
            title="Matriz de Riesgo por Mes",
            labels={'mes': 'Mes', 'cantidad_hitos': 'Cantidad de Hitos'},
            color_discrete_map=risk_colors
        )
        
        st.plotly_chart(fig_risk, use_container_width=True)
        
        # Recomendaciones
        st.subheader("💡 Recomendaciones")
        
        critical_months = risk_analysis[risk_analysis['nivel_riesgo'] == 'Crítico']
        if not critical_months.empty:
            st.error(f"⚠️ **Atención**: Los meses {', '.join(map(str, critical_months['mes']))} tienen carga crítica de trabajo.")
            st.markdown("""
            **Acciones recomendadas:**
            - Redistribuir actividades no críticas
            - Asignar recursos adicionales
            - Implementar seguimiento semanal
            - Considerar paralelización de tareas
            """)
        else:
            st.success("✅ La distribución de trabajo está balanceada.")
    
    with tab4:
        st.header("⚙️ Configuración Avanzada")
        
        # Información del proyecto
        st.subheader("📋 Información del Proyecto")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Nombre del Proyecto", value="Icon Bay Torres")
            st.date_input("Fecha de Inicio", value=datetime.now())
            st.number_input("Presupuesto Total (USD)", min_value=0, value=1000000)
        
        with col2:
            st.text_input("Gerente de Proyecto", placeholder="Nombre del gerente")
            st.date_input("Fecha de Finalización", value=datetime.now() + timedelta(days=365))
            st.text_area("Descripción", placeholder="Descripción del proyecto...")
        
        # Configuraciones del sistema
        st.subheader("🔧 Configuraciones del Sistema")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.checkbox("Notificaciones automáticas", value=True)
            st.checkbox("Alertas de retraso", value=True)
            st.selectbox("Idioma", ["Español", "English"])
        
        with col2:
            st.checkbox("Backup automático", value=True)
            st.checkbox("Modo oscuro", value=False)
            st.selectbox("Zona horaria", ["UTC-5", "UTC-6", "UTC"])
        
        # Gestión de usuarios
        st.subheader("👥 Gestión de Usuarios")
        
        user_data = {
            "Usuario": ["Admin", "Gerente", "Ingeniero", "Supervisor"],
            "Rol": ["Administrador", "Gerente de Proyecto", "Ingeniero Civil", "Supervisor de Obra"],
            "Permisos": ["Completo", "Lectura/Escritura", "Lectura", "Lectura"],
            "Estado": ["Activo", "Activo", "Activo", "Inactivo"]
        }
        
        users_df = pd.DataFrame(user_data)
        st.dataframe(users_df, use_container_width=True)
        
        # Estadísticas del sistema
        st.subheader("📊 Estadísticas del Sistema")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📁 Registros Totales", len(cm.df))
        
        with col2:
            st.metric("📂 Categorías", len(cm.df['categoria'].unique()))
        
        with col3:
            st.metric("📅 Duración", "13 meses")
        
        with col4:
            st.metric("🏢 Área Total", f"{area:,.2f} m²")
        
        # Opciones de exportación
        st.subheader("📤 Opciones de Exportación")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Exportar Dashboard", use_container_width=True):
                st.info("Funcionalidad en desarrollo")
        
        with col2:
            if st.button("📋 Exportar Hitos", use_container_width=True):
                csv_data = cm.export_to_csv()
                st.download_button(
                    "💾 Descargar CSV",
                    csv_data,
                    f"hitos_icon_bay_{datetime.now().strftime('%Y%m%d')}.csv",
                    "text/csv"
                )
        
        with col3:
            if st.button("📈 Exportar Análisis", use_container_width=True):
                st.info("Funcionalidad en desarrollo")

if __name__ == "__main__":
    main()
