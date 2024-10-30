import streamlit as st
import pandas as pd
import numpy as np

#configuración de pagina
st.set_page_config(
    page_title = "monitoreo Industrial",
    layout = "wide"
)

st.title("Sistema de monitoreo Industrial") #titulo que aparece en la página
st.write("Bienvenido al sistema de monitoreo en tiempo real")

st.header ("Panel principal")
st.subheader("Datos del sensor")
st.text("Información area del monitoreo")
st.markdown("**Texto con formato markdown**") #texto en negritas

#widgets basicos
temperatura = st.slider("temperatura", min_value=0, max_value=100, value=25) #Configuración de slider

col1, col2 = st.columns(2)

with col1:
    st.metric("Temperatura", f"{temperatura}°C", delta = "1.2°C")

with col2: 
    st.metric("Presion", "1013 hPa", delta = "-2 hPa")
