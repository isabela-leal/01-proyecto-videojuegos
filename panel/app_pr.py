import streamlit as st
import pandas as pd

from utils.confing import PAGE_CONFIG

st.set_page_config(**PAGE_CONFIG)

st.title("Análisis de ventas de videojuegos")
st.markdown("---")

with st.sidebar:
    st.title("Análisis de ventas de videojuegos")
    st.markdown("---")

page = st.radio(
        "Ir a",
        (
            "Inicio",
            "Dashboard General",
            "Análisis por Género",
            "Análisis por Plataforma",
            "Análisis por Región",
        ),
    )

st.markdown("---")
st.info("Utiliza el menú para navegar entre las diferentes secciones del análisis.")
st.markdown("---")
