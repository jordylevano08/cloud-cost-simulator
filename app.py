import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Configuración de la página
st.set_page_config(page_title="Cloud Cost Simulator", layout="wide")

st.title("🚀 Simulador de Migración: On-Premise vs. AWS")
st.markdown("""
Esta herramienta ayuda a decidir la estrategia de inversión en infraestructura 
basada en el costo total de propiedad (TCO).
""")

# 2. Barra lateral para que el usuario mueva los números
st.sidebar.header("Configuración de Parámetros")
n_servidores = st.sidebar.slider("Número de Servidores", 1, 50, 10)
costo_hardware = st.sidebar.number_input("Costo por Servidor Físico ($)", value=5000)
costo_cloud_mes = st.sidebar.number_input("Costo mensual AWS por instancia ($)", value=150)
años = st.sidebar.slider("Horizonte de tiempo (Años)", 1, 5, 3)

# 3. Lógica de cálculo (El motor de la app)
meses = range(1, (años * 12) + 1)
costo_onprem = [ (n_servidores * costo_hardware) for _ in meses] # Inversión inicial fuerte
costo_cloud = [ (n_servidores * costo_cloud_mes * m) for m in meses] # Pago por uso mensual

df_costos = pd.DataFrame({
    "Mes": meses,
    "On-Premise": costo_onprem,
    "AWS Cloud": costo_cloud
})

# 4. Visualización interactiva
st.subheader("Comparativa de Costo Acumulado")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df_costos["Mes"], df_costos["On-Premise"], label="On-Premise (CAPEX)", linewidth=3, color='red')
ax.plot(df_costos["Mes"], df_costos["AWS Cloud"], label="AWS Cloud (OPEX)", linewidth=3, color='green')
ax.set_xlabel("Meses")
ax.set_ylabel("Costo Total ($)")
ax.legend()
st.pyplot(fig)

# 5. El "Insight" Dinámico
punto_equilibrio = (n_servidores * costo_hardware) / (n_servidores * costo_cloud_mes)
st.info(f"💡 El punto de equilibrio ocurre en el mes **{int(punto_equilibrio)}**. Después de este mes, la nube empieza a ser más cara que haber comprado el hardware.")