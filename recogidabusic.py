import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import json
import os
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

# Parámetros Base
ORGANIZATION_KEY = "ic2026"
JSON_FILE = "registrorecogida.json"

def cargar_datos():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"organizacion": ORGANIZATION_KEY, "programa_recogida": []}

def guardar_datos(datos):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)

def main():
    st.title("🚜 Bienvenido a la logística de transporte de buses personal de IC")
    st.subheader("Programar recogidas y seguimiento de flota (Caña de Azúcar/Personal)")
    
    auth = st.sidebar.text_input("Llave de Organización", type="password")
    
    if auth != ORGANIZATION_KEY:
        st.sidebar.warning("Ingrese llave ic2026 para operar.")
        st.info("Sistema bloqueado. Introduzca la credencial en el panel lateral.")
        return

    datos_json = cargar_datos()
    menu = ["Lobby", "1. Programa tu recogida", "2. Sigue tu bus", "3. Solicitar autorización ruta"]
    choice = st.sidebar.selectbox("Navegador-Lobby", menu)

    if choice == "1. Programa tu recogida":
        st.header("📋 Registro de Recogida")
        with st.form("form_recogida"):
            col1, col2 = st.columns(2)
            with col1:
                id_pers = st.text_input("ID Personal / Nombre completo")
                cel = st.text_input("Celular")
                area = st.selectbox("Área de trabajo", ["Campo", "Cosecha", "Fábrica"])
            with col2:
                dir_rec = st.text_input("Dirección de recogida")
                bus_aut = st.text_input("Bus autorizado")
                jefe = st.text_input("Nombre y Apellido Jefe/Líder")
            
            if st.form_submit_button("Programar"):
                nueva_entrada = {
                    "id_personal": id_pers,
                    "direccion_recogida": dir_rec,
                    "celular": cel,
                    "bus_autorizado": bus_aut,
                    "area_trabajo": area,
                    "jefe_lider": jefe,
                    "fecha_registro": datetime.now().isoformat(),
                    "estado_solicitud": "activo"
                }
                datos_json["programa_recogida"].append(nueva_entrada)
                guardar_datos(datos_json)
                st.success(f"Recogida registrada en registrorecogida.json para {id_pers}")

    elif choice == "2. Sigue tu bus":
        st.header("📍 Tracking de Flota en Tiempo Real")
        
        map_data = pd.DataFrame({
            'lat': [3.4516, 3.4800, 3.4200],
            'lon': [-76.5320, -76.5000, -76.5500],
            'bus': ['Bus 01 - Cosecha', 'Bus 02 - Fábrica', 'Bus 03 - Campo'],
            'estado': ['En ruta', 'Recogiendo', 'Hacia Ingenio']
        })

        icon_data = {
            "url": "https://img.icons8.com/color/48/bus.png",
            "width": 128, "height": 128, "anchorY": 128
        }
        map_data["icon_data"] = [icon_data for _ in range(len(map_data))]

        view_state = pdk.ViewState(latitude=3.4516, longitude=-76.5320, zoom=11, pitch=0)
        
        layer = pdk.Layer(
            "IconLayer",
            map_data,
            get_position='[lon, lat]',
            get_icon='icon_data',
            get_size=40,
            pickable=True
        )

        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            layers=[layer], 
            initial_view_state=view_state, 
            tooltip={"text": "{bus}\nEstado: {estado}"}
        ))
        st.info("Visualizando 3 unidades activas.")

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
        st.markdown("### Instrucciones de Operación:")
        st.write("Gestionar transporte de personal agrícola IC.")
        st.image("https://img.icons8.com/fluency/96/sugar-cane.png", width=100)

if __name__ == "__main__":
    main()