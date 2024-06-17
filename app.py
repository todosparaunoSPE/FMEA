# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 10:15:58 2024

@author: jperezr
"""

import streamlit as st
import pandas as pd
import numpy as np
import base64

import plotly.express as px  # Importar Plotly Express
from unidecode import unidecode  # Importar la función unidecode desde la librería unidecode



# Función para simular fallos
def simulate_failures(mean_time_between_failures, simulation_time):
    num_failures = np.random.poisson(lam=simulation_time / mean_time_between_failures)
    return num_failures

# Función para realizar análisis FMEA
def perform_fmea(failure_modes, effects, causes, detection_controls):
    if len(failure_modes) == len(effects) == len(causes) == len(detection_controls):
        fmea_data = pd.DataFrame({
            'Modo de Fallo': failure_modes,
            'Efecto': effects,
            'Causa': causes,
            'Detection Control': detection_controls,
        })
        return fmea_data
    else:
        raise ValueError("All lists must have the same length")

# Inicializar el estado de sesión para el historial de simulaciones y los resultados del FMEA
if 'simulation_history' not in st.session_state:
    st.session_state.simulation_history = []

if 'fmea_results' not in st.session_state:
    st.session_state.fmea_results = None

# Listas predefinidas
failure_modes_list = [
    "Falla del motor", 
    "Fuga de gas", 
    "Bloqueo del filtro", 
    "Fallo del sensor de presión", 
    "Sobrecalentamiento del compresor"
]

effects_list = [
    "Parada del sistema", 
    "Pérdida de eficiencia", 
    "Aumento de la presión", 
    "Lecturas incorrectas", 
    "Daño en componentes"
]

causes_list = [
    "Desgaste mecánico", 
    "Defectos en las juntas", 
    "Falta de mantenimiento", 
    "Fallos electrónicos", 
    "Lubricación inadecuada"
]

detection_controls_list = [
    "Monitoreo de vibraciones", 
    "Inspecciones regulares", 
    "Cambio de filtros", 
    "Calibración de sensores", 
    "Sistemas de enfriamiento"
]

st.title('Herramienta de Evaluación de Confiabilidad para Sistemas de Compresión de Gas')


# Contenido principal que irá en el cuerpo de la página
def main():
    
    
    st.sidebar.title('Contenidos')
    st.sidebar.markdown('# Introducción')
    st.sidebar.markdown('''
    ### Introducción al Sistema de Compresión de Gas
    
    Un sistema de compresión de gas es un conjunto de componentes diseñados para aumentar la presión de un gas mediante compresión. Este tipo de sistemas son fundamentales en diversas industrias, como la industria petroquímica, la industria de procesamiento de alimentos, y en aplicaciones de HVAC (calefacción, ventilación y aire acondicionado).
    
    Es crucial evaluar la confiabilidad de estos sistemas debido a su papel en operaciones críticas y su impacto en la productividad y la seguridad. La evaluación de confiabilidad permite identificar posibles fallas, prevenir paradas no planificadas y optimizar el mantenimiento preventivo, asegurando así la operación eficiente y segura del sistema.
    ''')
    
    st.sidebar.markdown('''
    # Uso de la Herramienta
    
    Esta herramienta de evaluación de confiabilidad del sistema de compresión de gas está diseñada para ayudarte a entender mejor el comportamiento del sistema frente a fallos potenciales. A continuación, se explica cómo utilizar la aplicación:
    
    1. **Entrada de Datos del Sistema:**
       - Ingresa el tiempo medio entre fallos (MTBF) esperado y el tiempo de simulación para evaluar el sistema.
    
    2. **Simulación de Fallos:**
       - Basado en los datos ingresados, la herramienta simula el número esperado de fallos durante el tiempo de simulación especificado.
    
    3. **Análisis FMEA (Análisis de Modos y Efectos de Falla):**
       - Selecciona automáticamente modos de falla, efectos, causas y controles de detección, proporcionando un análisis de riesgos estructurado.
    
    4. **Recomendaciones de Mantenimiento:**
       - Proporciona recomendaciones basadas en el análisis para mejorar la confiabilidad del sistema, como intervalos óptimos de mantenimiento.
    
    5. **Análisis de Sensibilidad:**
       - Realiza un análisis de sensibilidad para entender cómo cambian los resultados al variar los parámetros clave, como el MTBF.
    
    6. **Exportación de Resultados:**
       - Permite exportar los resultados del análisis FMEA y otros datos relevantes para su revisión o análisis externo.
    ''')
    
    st.sidebar.markdown('''
    # Recursos Adicionales
    
    Para una comprensión más profunda del mantenimiento de sistemas de compresión de gas y la evaluación de confiabilidad, se recomienda consultar los siguientes recursos:
    
    - **Normas y Directrices Técnicas:** Investigar las normativas y estándares relevantes de la industria para mantenimiento y operación seguros.
      
    - **Publicaciones y Artículos Técnicos:** Revisar artículos científicos y técnicos sobre métodos avanzados de análisis de riesgos y confiabilidad.
    
    - **Cursos y Capacitaciones:** Considerar cursos en línea o capacitaciones sobre mantenimiento predictivo y análisis de fallas en sistemas industriales.
    
    - **Comunidades y Foros:** Participar en comunidades en línea o foros de discusión sobre mantenimiento industrial para intercambiar experiencias y buenas prácticas.
    
    Estos recursos pueden proporcionar una base sólida para profundizar en la gestión de la confiabilidad de sistemas de compresión de gas y mejorar la eficiencia operativa en entornos industriales.
    ''')

# Créditos del creador
st.sidebar.markdown("---")
st.sidebar.text("Creado por:")
st.sidebar.markdown("<span style='color: yellow;'>Javier Horacio Pérez Ricárdez</span>", unsafe_allow_html=True)    



# Entrada de datos
st.header("Entrada de Datos del Sistema")
mean_time_between_failures = st.number_input("Tiempo Medio Entre Fallos (horas)", min_value=1, value=1000)
simulation_time = st.number_input("Tiempo de Simulación (horas)", min_value=1, value=10000)

# Simulación de fallos
st.header("Simulación de Fallos")
num_failures = simulate_failures(mean_time_between_failures, simulation_time)
st.write(f"Número esperado de fallos en {simulation_time} horas: {num_failures}")
st.session_state.simulation_history.append((simulation_time, num_failures))

# Mostrar historial de simulaciones
if st.checkbox("Mostrar historial de simulaciones"):
    st.subheader("Historial de Simulaciones")
    for sim_time, num_fail in st.session_state.simulation_history:
        st.write(f"Tiempo de simulación: {sim_time} horas, Número de fallos: {num_fail}")

# Análisis FMEA con asignación automática
st.header("Análisis de Modos y Efectos de Falla (FMEA)")
st.write("Resultados del análisis FMEA automático:")

# Simular selección automática de modos de falla, efectos, causas y controles de detección
num_items = min(len(failure_modes_list), len(effects_list), len(causes_list), len(detection_controls_list))
selected_indices = np.random.choice(num_items, size=num_failures, replace=True)

selected_failure_modes = [failure_modes_list[i] for i in selected_indices]
selected_effects = [effects_list[i] for i in selected_indices]
selected_causes = [causes_list[i] for i in selected_indices]
selected_detection_controls = [detection_controls_list[i] for i in selected_indices]

st.session_state.fmea_results = perform_fmea(selected_failure_modes, selected_effects, selected_causes, selected_detection_controls)

# Mostrar resultados del análisis FMEA si hay datos disponibles
if st.session_state.fmea_results is not None:
    st.dataframe(st.session_state.fmea_results)
else:
    st.warning("No hay resultados de FMEA disponibles.")

# Recomendaciones de mantenimiento
st.header("Recomendaciones de Mantenimiento")
optimal_maintenance_interval = mean_time_between_failures / 2  # Ejemplo simplificado
st.write(f"Intervalo óptimo de mantenimiento: {optimal_maintenance_interval} horas")

# Impacto en la producción
production_impact = num_failures * 100  # Ejemplo simplificado: 100 unidades perdidas por fallo
st.write(f"Impacto estimado en la producción: {production_impact} unidades perdidas")

# Análisis de sensibilidad
st.header("Análisis de Sensibilidad")
sensitivity_range = st.slider("Rango de sensibilidad (%)", 0, 100, 10)
sensitivity_analysis = []
for change in np.linspace(-sensitivity_range, sensitivity_range, 5):
    new_mtbf = mean_time_between_failures * (1 + change / 100)
    new_failures = simulate_failures(new_mtbf, simulation_time)
    sensitivity_analysis.append((change, new_failures))

sensitivity_df = pd.DataFrame(sensitivity_analysis, columns=["Cambio (%)", "Fallos"])
st.write("Resultados del análisis de sensibilidad:")
st.dataframe(sensitivity_df)

# Gráfico interactivo de resultados de sensibilidad
st.header("Gráfico Interactivo de Sensibilidad")
fig = px.line(sensitivity_df, x="Cambio (%)", y="Fallos", title="Análisis de Sensibilidad del MTBF")
st.plotly_chart(fig)


# Función para eliminar acentos de las columnas de un DataFrame
def remove_accents(df):
    df_copy = df.copy()
    for col in df_copy.columns:
        if df_copy[col].dtype == 'object':  # Solo aplica a columnas de tipo objeto (strings)
            df_copy[col] = df_copy[col].apply(lambda x: unidecode(str(x)) if pd.notnull(x) else x)
    return df_copy

# Definir la aplicación de Streamlit
st.header("Exportación de Resultados")
if st.button("Exportar resultados como CSV"):
    if st.session_state.fmea_results is not None and not st.session_state.fmea_results.empty:
        # Eliminar acentos del DataFrame
        fmea_results_clean = remove_accents(st.session_state.fmea_results)
        
        # Convertir el DataFrame a CSV en memoria sin acentos
        csv = fmea_results_clean.to_csv(index=False, encoding='utf-8-sig')
        
        # Ofrecer opción para guardar el archivo
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="resultados_fmea.csv">Haga clic aquí para descargar el archivo CSV</a>'
        st.markdown(href, unsafe_allow_html=True)
    else:
        st.error("No hay resultados de FMEA para exportar o el DataFrame está vacío.")



if __name__ == '__main__':
    main()



