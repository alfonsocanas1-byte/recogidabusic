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
    </style>
    """, unsafe_allow_html=True)

# Parámetros Base
ORGANIZATION_KEY = "ic2026"
FILE_RECOGIDA = "registrorecogida.json"
FILE_AUTORIZACION = "registroautorizacionruta.json"

def cargar_json(filepath, key_raiz):
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {"organizacion": ORGANIZATION_KEY, key_raiz: []}

def guardar_json(filepath, datos):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)

def main():
    st.title("🚜 Bienvenido a la logística de transporte de buses personal de IC")
    
    auth = st.sidebar.text_input("Llave de Organización", type="password")
    if auth != ORGANIZATION_KEY:
        st.sidebar.warning("Ingrese llave ic2026")
        st.info("Sistema bloqueado.")
        return

    menu = ["Lobby", "1. Programa tu recogida", "2. Sigue tu bus", "3. Solicitar autorización ruta"]
    choice = st.sidebar.selectbox("Navegador-Lobby", menu)

    # --- LOBBY ---
    if choice == "Lobby":
        st.header("🏟️ Lobby de Control")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📂 Leer Programa Recogida"):
                data = cargar_json(FILE_RECOGIDA, "programa_recogida")
                if data["programa_recogida"]:
                    st.table(pd.DataFrame(data["programa_recogida"]))
                else:
                    st.info("Sin registros en recogida.")

        with col2:
            if st.button("📂 Leer Autorizaciones"):
                data = cargar_json(FILE_AUTORIZACION, "solicitudes_autorizacion")
                if data["solicitudes_autorizacion"]:
                    st.table(pd.DataFrame(data["solicitudes_autorizacion"]))
                else:
                    st.info("Sin registros en autorizaciones.")

    # --- 1. PROGRAMA TU RECOGIDA ---
    elif choice == "1. Programa tu recogida":
        st.header("📋 Registro de Recogida")
        with st.form("form_recogida"):
            id_p = st.text_input("ID Personal / Nombre")
            cel = st.text_input("Celular")
            area = st.selectbox("Área", ["Campo", "Cosecha", "Fábrica"])
            direc = st.text_input("Dirección")
            bus = st.text_input("Bus Autorizado")
            jefe = st.text_input("Jefe/Líder")
            
            if st.form_submit_button("Guardar Recogida"):
                db = cargar_json(FILE_RECOGIDA, "programa_recogida")
                db["programa_recogida"].append({
                    "id_personal": id_p, "direccion_recogida": direc, "celular": cel,
                    "bus_autorizado": bus, "area_trabajo": area, "jefe_lider": jefe,
                    "fecha_registro": datetime.now().isoformat(), "estado_solicitud": "activo"
                })
                guardar_json(FILE_RECOGIDA, db)
                st.success("Registrado.")

    # --- 2. SIGUE TU BUS ---
    elif choice == "2. Sigue tu bus":
        st.header("📍 Tracking de Flota")
        map_data = pd.DataFrame({'lat': [3.4516, 3.4800], 'lon': [-76.5320, -76.5000], 'bus': ['Bus 01', 'Bus 02']})
        map_data["icon_data"] = [{"url": "https://img.icons8.com/color/48/bus.png", "width": 128, "height": 128, "anchorY": 128} for _ in range(len(map_data))]
        
        view = pdk.ViewState(latitude=3.4516, longitude=-76.5320, zoom=11)
        layer = pdk.Layer("IconLayer", map_data, get_position='[lon, lat]', get_icon='icon_data', get_size=40, pickable=True)
        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view, tooltip={"text": "{bus}"}))

    # --- 3. SOLICITAR AUTORIZACIÓN RUTA ---
    elif choice == "3. Solicitar autorización ruta":
        st.header("🔐 Formulario de Autorización")
        with st.form("form_auth"):
            id_p = st.text_input("ID Personal")
            nom = st.text_input("Nombre y Apellido")
            jefe = st.text_input("Jefe/Líder Inmediato")
            razon = st.text_area("Razón de solicitud uso ruta")
            vehiculo = st.radio("¿Tiene vehículo de la empresa?", ["Sí", "No"])
            contratista = st.radio("¿Es contratista?", ["Sí", "No"])
            
            if st.form_submit_button("Enviar Solicitud"):
                db = cargar_json(FILE_AUTORIZACION, "solicitudes_autorizacion")
                db["solicitudes_autorizacion"].append({
                    "id_personal": id_p, "nombre_apellido": nom, "jefe_lider_inmediato": jefe,
                    "razon_solicitud": razon, "tiene_vehiculo_empresa": vehiculo,
                    "es_contratista": contratista, "fecha_solicitud": datetime.now().isoformat(),
                    "estado": "Pendiente"
                })
                guardar_json(FILE_AUTORIZACION, db)
                st.success("Solicitud guardada en registroautorizacionruta.json")

if __name__ == "__main__":
    main()