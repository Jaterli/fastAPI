import requests
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# URL de la API FastAPI
API_URL = "https://raw.githubusercontent.com/Jaterli/jtlblog/main/public/data/postsByMonth.json"

# Función para obtener los datos de la API
def fetch_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error al cargar los datos.")
        return {}

# Función para generar la gráfica de barras apiladas
@st.cache_data
def plot_stacked_bar_chart(data):
    # Obtener todas las categorías y los meses
    categories = list(data.keys())
    months = list(next(iter(data.values())).keys())  # Usamos la primera categoría para obtener los meses

    # Crear un array de ceros para el valor inicial del bottom
    bottom = np.zeros(len(months))

    # Configurar los colores
    colors = ['skyblue', 'coral', 'yellowgreen', 'lightcoral', 'cyan']

    fig, ax = plt.subplots(figsize=(2, 0.8))  # Ajustar el tamaño de la gráfica

    # Iterar por cada categoría para apilar las barras
    for i, category in enumerate(categories):
        counts = [data[category].get(month, 0) for month in months]  # Obtener los valores para cada mes
        p = ax.bar(months, counts, bottom=bottom, label=category, width=0.3, color=colors[i % len(colors)])  # Agregar la barra
        bottom += np.array(counts)  # Actualizar el bottom para la próxima barra
        ax.bar_label(p, label_type='center', fontsize=6)
        

    # Configurar etiquetas y título
    # ax.set_xlabel('Mes', fontsize=12)
    ax.set_ylabel('Número de Posts', fontsize=7)
    ax.set_title('Número de Posts por Mes', fontsize=7)

    # Configurar el tamaño de los ticks del eje X y Y
    ax.tick_params(axis='x', labelsize=7)  # Tamaño de los valores en el eje X
    ax.tick_params(axis='y', labelsize=7)  # Tamaño de los valores en el eje Y
    # Mostrar la leyenda con un tamaño personalizado

    plt.xticks(rotation=45)

    # Mostrar la leyenda
    ax.legend(fontsize=6)  # Tamaño de la leyenda


    # Mostrar la gráfica en Streamlit
    st.pyplot(fig)
    
    # Guardar en archivo
    plt.savefig('grap.png')

def main():
    # st.title("Gráfica de Posts por Mes (Stacked Bar Chart)")
    data = fetch_data()
    
    if data:
        plot_stacked_bar_chart(data)

if __name__ == "__main__":
    main()
