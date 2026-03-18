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
    .sidebar .sidebar-content { 
        background-image: linear-gradient(#1a237e, #2e7d32); 
        color: white; 
    }
    h1 { color: #1a237e; border-bottom: 2px solid #2e7d32; }
    .stTextInput>div>div>input { color: #1a237e; }
    </style>
    """, unsafe_allow_html=True)

# Llave de la organización
ORGANIZATION_KEY = "ic2026"

def main():
    st.title("🚜 Bienvenido a la logística de transporte de buses personal de IC")
    st.subheader("Programar recogidas y seguimiento de flota (Caña de Azúcar/Personal)")
    
    # Autenticación lateral
    auth = st.sidebar.text_input("Llave de Organización", type="password")
    
    if auth != ORGANIZATION_KEY:
        st.sidebar.warning("Ingrese llave ic2026 para operar.")
        st.info("Sistema bloqueado. Por favor, introduzca la credencial de la organización en el panel lateral.")
        return

    # Navegador Lobby
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
                # Aquí se integraría el envío a la DB (Firestore/SQL)

    # 2. SIGUE TU BUS (SIMULACIÓN TÉCNICA)
    elif choice == "2. Sigue tu bus":
        st.header("📍 Tracking de Flota en Tiempo Real")
        
        # Simulación de coordenadas (Cali y alrededores agrícolas)
        map_data = pd.DataFrame({
            'lat': [3.4516, 3.4800, 3.4200],
            'lon': [-76.5320, -76.5000, -76.5500],
            'bus': ['Bus 01 - Cosecha', 'Bus 02 - Fábrica', 'Bus 03 - Campo'],
            'estado': ['En ruta', 'Recogiendo', 'Hacia Ingenio']
        })

        view_state = pdk.ViewState(
            latitude=3.4516, 
            longitude=-76.5320, 
            zoom=11, 
            pitch=0
        )
        
        # Capa de iconos para buses
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

        st.pydeck_chart(pdk.Deck(
            layers=[layer], 
            initial_view_state=view_state, 
            tooltip={"text": "{bus}\nEstado: {estado}"}
        ))
        st.info("Información: Visualizando 3 unidades activas en zona de influencia.")

    # 3. SOLICITAR AUTORIZACIÓN RUTA
    elif choice == "3. Solicitar autorización ruta":
        st.header("🔐 Validación de Ruta")
        with st.form("auth_ruta"):
            st.text_input("ID Personal")
            st.text_input("Jefe/Líder Inmediato")
            st.selectbox("Área de trabajo", ["Campo", "Cosecha", "Fábrica"])
            st.radio("¿Tiene vehículo asignado?", ["Sí", "No"])
            
            if st.form_submit_button("Enviar Solicitud"):
                st.info("Solicitud enviada a central de logística para aprobación.")

    else:
        # Pantalla de inicio (Lobby)
        st.markdown("""
        ### Instrucciones de Operación:
        1.  **Programar**: Use esta opción para definir su punto de recogida diario.
        2.  **Seguimiento**: Verifique la posición de la unidad asignada en tiempo real.
        3.  **Cambios**: Gestione autorizaciones especiales con su supervisor.
        """)
        st.image("https://img.icons8.com/fluency/96/sugar-cane.png", width=100)

if __name__ == "__main__":
    main()