import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from datetime import datetime

# Configuración técnica de interfaz
st.set_page_config(page_title="Logística IC", layout="wide")

# Estilo visual: Azul, Verde, Caña de Azúcar
st.markdown("""
    <style>
    .main { background-color: #f0f5f0; }
    .stButton>button { background-color: #2e7d32; color: white; }
    .sidebar .sidebar-content { background-image: linear-gradient(#1a237e, #2e7d32); color: white; }
    h1 { color: #1a237e; border-bottom: 2px solid #2e7d32; }
    </style>
    """, unsafe_allow_html=True)

# Llave de la organización
ORGANIZATION_KEY = "ic2026"

def main():
    st.title("🚜 Bienvenido a la logística de transporte de buses personal de IC")
    st.subheader("Programar recogidas y seguimiento de flota (Caña de Azúcar/Personal)")
    
    auth = st.sidebar.text_input("Llave de Organización", type="password")
    
    if auth != ORGANIZATION_KEY:
        st.warning("Ingrese llave ic2026 para operar.")
        return

    menu = ["Lobby", "1. Programa tu recogida", "2. Sigue tu bus", "3. Solicitar autorización ruta"]
    choice = st.sidebar.selectbox("Navegador-Lobby", menu)

    # 1. PROGRAMA TU RECOGIDA
    if choice == "1. Programa tu recogida":
        st.header("📋 Registro de Recogida")
        with st.form("form_recogida"):
            col1, col2 = st.columns(2)
            with col1:
                id_pers = st.text_input("ID Personal")
                cel = st.text_input("Celular")
                area = st.selectbox("Área de trabajo", ["Campo", "Cosecha", "Fábrica"])
            with col2:
                dir_rec = st.text_input("Dirección de recogida")
                bus_aut = st.text_input("Bus autorizado / Caso especial")
                jefe = st.text_input("Nombre y Apellido Jefe/Líder")
            
            if st.form_submit_button("Programar"):
                st.success(f"Recogida programada para ID {id_pers}. Sector: {area}")

    # 2. SIGUE TU BUS (SIMULACIÓN TÉCNICA)
    elif choice == "2. Sigue tu bus":
        st.header("📍 Tracking de Flota en Tiempo Real")
        
        # Datos aleatorios para 3 buses (Cali/Zona Agrícola aprox)
        map_data = pd.DataFrame({
            'lat': [3.4516, 3.4800, 3.4200],
            'lon': [-76.5320, -76.5000, -76.5500],
            'bus': ['Bus 01 - Cosecha', 'Bus 02 - Fábrica', 'Bus 03 - Campo']
        })

        view_state = pdk.ViewState(latitude=3.4516, longitude=-76.5320, zoom=12, pitch=0)
        
        layer = pdk.Layer(
            "IconLayer",
            map_data,
            get_position='[lon, lat]',
            get_icon='''{
                "url": "https://img.icons8.com/color/48/bus.png",
                "width": 128, "height": 128, "anchorY": 128
            }''',
            get_size=4,
            pickable=True
        )

        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{bus}"}))
        st.info("Información: 3 buses activos en ruta principal.")

    # 3. SOLICITAR AUTORIZACIÓN
    elif choice == "3. Solicitar autorización ruta":
        st.header("🔐 Validación de Ruta")
        with st.form("auth_ruta"):
            st.text_input("ID Personal")
            st.text_input("Jefe/Líder Inmediato")
            st.selectbox("Área de trabajo", ["Campo", "Cosecha", "Fábrica"])
            st.radio("¿Tiene vehículo asignado?", ["Sí", "No"])
            if st.form_submit_button("Enviar Solicitud"):
                st.info("Solicitud enviada a central de logística.")

    else:
        st.write("Seleccione una opción en el menú de la izquierda para gestionar el transporte.")

if __name__ == "__main__":
    main()