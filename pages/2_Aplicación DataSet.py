import os
import pandas as pd
import streamlit as st

# Cargar el dataset CSV
# Obtén la ruta absoluta del archivo actual (2_Aplicación DataSet.py)
current_dir = os.path.dirname(__file__)
# Construye la ruta completa hacia el archivo CSV
file_path = os.path.join(current_dir, "..", "static", "datasets", "Impact_of_Remote_Work_on_Mental_Health.csv")

# Carga el archivo CSV
df = pd.read_csv(file_path)

# Mostrar el DataFrame
st.dataframe(df)

# Análisis exploratorio básico
st.write("Estadísticas descriptivas:")
st.write(df.describe())

# Histograma de nivel de estrés
import matplotlib.pyplot as plt
plt.hist(df['Stress_Level'])
st.pyplot(plt)

# Filtrar por ubicación de trabajo
location = st.selectbox("Selecciona una ubicación", df['Work_Location'].unique())
filtered_df = df[df['Work_Location'] == location]
st.dataframe(filtered_df)

#Q