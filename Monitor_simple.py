# Parte 1 - Importar librerías.
import streamlit as st                                  # Librería de streamlit.
import random                                           # Librería números aleatorios.
import time                                             # Librería de tiempo.
import plotly.express as px                             #
import pandas as pd                                     #
import numpy as np 

# Parte 2 - Configuraciones iniciales.
class SensorTemperatura: 
    def __init__(self):                                 # Se está definiendo un método privado / constructor.
        self.valor_base = 25
    
    def leer(self):                                     # Leerá el valor base con variación.
        return self.valor_base + random.uniform(-5,5)   # Traerá valor base y lo vareará -5 o +5.

#datos de ejemplo 
df = pd.DataFrame({
    'tiempo' : pd.date_range(start= '2024-01-01', periods=100, freq='H'), #timestap
    'temperatura' : np.random.normal(25,3,100), #Config de temperatura
    'presion' : np.random.normal(1013, 5, 100) #config de presion
}) #creacion de diccionario xd 


sensor1 = SensorTemperatura()                           # Primero se define clase y luego se manda llamar.

grafica = st.empty()                                    # Se deja un espacio para colocar la gráfica.

#controles por barra lateral 
st.sidebar.header("Configuracion")

#selector de parametros
parametro = st.sidebar.selectbox(
    "Seleccione parametro",
    ["temperatura", "presion", "humedad"]
)

#rango de fechas 
fecha_inicio = st.sidebar.date_input("Fecha Inicio")
fecha_fin = st.sidebar.date_input("Fecha Fin")

#organizacion es pestañas
tab1, tab2 = st.tabs(["Tiempo real", "Historico"])

with tab1: 
    st.header("Monitoreo en Tiempo Real")
    if st.button("Iniciar monitoreo"):
        for i in range(100):                                # Se leerá 100 veces.
            temperatura = sensor1.leer()                    # Tendrá el valor de la lectura.
            grafica.metric("Temperatura Actual",f"{temperatura:.1f}°C",f"{temperatura - 25:.1f}°C")
            time.sleep(1)                                   # Se modificará cada segundo.

with tab2: 
    st.header("Datos Historicos")
    #Historico de temperatura
    fig = px.line(df, x='tiempo', y='temperatura', title='Historico de temperatura')
    st.plotly_chart(fig, use_container_width= True) #Widget para garficos 

    #grafica de dispercion 
    scatter = px.scatter(df, x = 'tiempo', y = 'presion', title= 'historico de presion')
    st.plotly_chart(scatter,use_container_width= True)