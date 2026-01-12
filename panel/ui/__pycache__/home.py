import streamlit as st
import plotly.express as px
from utils.data_loader import get_data_info
from utils.config import COLORS

def render_home_page(df):
    st.markdown("## 👋 Bienvenido al Análisis de Videojuegos")
    st.markdown("""
    Esta aplicación interactiva te permite explorar y analizar datos de ventas de videojuegos
    desde 1980 hasta 2020. Descubre tendencias, patrones y insights del mercado global de videojuegos.
    """)
    
    st.markdown("---")
    
    info = get_data_info(df)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🎮 Total de Juegos",
            value=f"{info['total_games']:,}",
            delta=None
        )
    with col2:
        st.metric(
            label="💰 Ventas Totales",
            value=f"{info['total_sales']:,.0f}M",  # :.0f = sin decimales, M = millones
            delta=None
        )
    with col3:
        st.metric(
            label="📈 Promedio de Ventas",
            value=f"{info['avg_sales']:.2f}M",  # :.2f = 2 decimales
            delta=None
        )
    with col4:
        st.metric(
            label="📅 Rango de Años",
            value=f"{info['year_range'][0]} - {info['year_range'][1]}", # Formato: 1980-2020
            delta=None
        )
    
    st.markdown("---")
    
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="🕹️ Plataformas Únicas",
            value=info['total_platforms'],
            delta=None
        )
    with col2:
        st.metric(
            label="🎲 Géneros Únicos",
            value=info['total_genres']
        )
    with col3:
        st.metric(
            label="🏢 Publishers Únicos",
            value=info['total_publishers']
        )      
    st.markdown("---")
    
    
    st.markdown("### 🌍 Ventas por Región")
    
    col1, col2 = st.columns([2,1])
    
    with col1:
        region_data = {
            'Región': ['Norteamérica', 'Europa', 'Japón', 'Otras Regiones'],
            'Ventas (M)': [
                info['na_sales'],
                info['eu_sales'],
                info['jp_sales'],
                info['other_sales']
            ]
        }
    
        fig = px.pie(
            region_data,
            values='Ventas (M)',
            names='Región',
            title="Ventas Totales por Región (1980-2020)",
            color='Región',
            color_discrete_map={
                'Norteamérica': COLORS['na'],
                'Europa': COLORS['eu'],
                'Japón': COLORS['jp'],
                'Otras Regiones': COLORS['other']
            },
            hole=0.4
        )
    
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label'
        )
    
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Ventas por Región")
    
        st.markdown(f"- **Norteamérica:** {info['na_sales']:,.0f}M")
        st.markdown(f"- **Europa:** {info['eu_sales']:,.0f}M")
        st.markdown(f"- **Japón:** {info['jp_sales']:,.0f}M")
        st.markdown(f"- **Otras Regiones:** {info['other_sales']:,.0f}M")
    
        st.markdown("---")
    
    
    
    st.markdown(""" Top 10 Videojuegos con Mayores Ventas Globales""")
    
    top_games = df.nlargest(10, 'Global_Sales')[['Rank', 'Name', 'Platform', 'Year', 'Genre', 'Global_Sales']]
    
    fig = px.bar(
        top_games,
        x='Global_Sales',
        y='Name',
        orientation='h',        
        title="Top 10 Videojuegos con Mayores Ventas Globales",
        labels={'Global_Sales': 'Ventas Globales (M)',
                'Name': 'Videojuego'},
        color='Genre',
        color_continuous_scale=px.colors.sequential.Blues
    )  
    
    fig.update_layout(
        yaxis={'categoryorder':'total ascending'},
        height=500)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    