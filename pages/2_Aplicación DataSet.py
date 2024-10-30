import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración inicial
st.title("Análisis Exploratorio del Dataset: Impacto del Trabajo Remoto en la Salud Mental")

# Cargar el dataset CSV
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, "..", "static", "datasets", "Impact_of_Remote_Work_on_Mental_Health.csv")

@st.cache_data
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error("Archivo no encontrado. Verifica la ruta.")
        return pd.DataFrame()  # Retorna un DataFrame vacío en caso de error

df = load_data(file_path)

# Mostrar el DataFrame
st.write("Vista General del Dataset:")
st.dataframe(df)

# Verificar datos antes de continuar
if df.empty:
    st.warning("No se pudo cargar el dataset. Deteniendo análisis.")
else:
    # 1. Valores Faltantes
    st.write("Valores faltantes por columna:")
    st.write(df.isnull().sum())

    # 2. Estadísticas Descriptivas
    st.write("Estadísticas descriptivas:")
    st.write(df.describe())

    # Funciones para visualización
    def plot_histogram(column):
        plt.figure()
        sns.histplot(df[column].dropna(), bins=20, kde=True)
        st.pyplot(plt)
        plt.close()

    def plot_boxplot(column):
        plt.figure()
        sns.boxplot(x=df[column].dropna())
        st.pyplot(plt)
        plt.close()

    # 3. Distribución de Variables Numéricas
    st.write("Distribución de variables numéricas:")
    num_columns = df.select_dtypes(include=['float64', 'int64']).columns
    for col in num_columns:
        st.write(f"Distribución de {col}")
        plot_histogram(col)
        plot_boxplot(col)

    # 4. Mapa de Calor de Correlaciones
    st.write("Mapa de calor de correlaciones entre variables numéricas:")
    num_df = df.select_dtypes(include=['float64', 'int64'])
    corr = num_df.corr()

    def plot_heatmap(corr):
        plt.figure(figsize=(10, 6))
        sns.heatmap(corr, annot=True, cmap='coolwarm', linewidths=0.5)
        st.pyplot(plt)

    plot_heatmap(corr)

    # 5. Visualización de Variables Categóricas
    st.write("Distribución de variables categóricas:")
    cat_columns = df.select_dtypes(include=['object']).columns
    for col in cat_columns:
        st.write(f"Frecuencia de {col}")
        fig, ax = plt.subplots()
        sns.countplot(data=df, y=col, ax=ax)
        st.pyplot(fig)

    # 6. Histograma de Nivel de Estrés
    st.write("Histograma de Nivel de Estrés:")
    if 'Stress_Level' in df.columns:
        plot_histogram('Stress_Level')

    # 7. Filtrado por Ubicación de Trabajo
    if 'Work_Location' in df.columns:
        location = st.selectbox("Selecciona una ubicación para filtrar los datos", df['Work_Location'].dropna().unique())
        filtered_df = df[df['Work_Location'] == location]
        st.write("Datos filtrados por ubicación de trabajo seleccionada:")
        st.dataframe(filtered_df)

    # Asegurarnos de que la columna 'Stress_Level' sea numérica
    df['Stress_Level'] = pd.to_numeric(df['Stress_Level'], errors='coerce')

    # 8. Análisis Bivariado - Promedio de Nivel de Estrés por Ubicación de Trabajo
    if 'Stress_Level' in df.columns and 'Work_Location' in df.columns:
        st.write("Promedio de Nivel de Estrés por Ubicación de Trabajo:")
        location_stress = df.groupby("Work_Location")["Stress_Level"].mean()
        st.bar_chart(location_stress)
