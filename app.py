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
    # Usamos todas las categorías para obtener los meses
    months = sorted(set(month for category in data.values() for month in category.keys()))
    # Crear un array de ceros para el valor inicial del bottom
    bottom = np.zeros(len(months))

    # Configurar los colores
    colors = ['skyblue', 'coral', 'yellowgreen', 'lightcoral', 'cyan']

    fig, ax = plt.subplots(1, 1, figsize=(6, 4))  # Ajustar el tamaño de la gráfica
    
    # Iterar por cada categoría para apilar las barras
    for i, category in enumerate(categories):
        counts = [data[category].get(month, 0) for month in months]  # Obtener los valores para cada mes
        p = ax.bar(months, counts, bottom=bottom, label=category, width=0.2, color=colors[i % len(colors)])  # Agregar la barra
        bottom += np.array(counts)  # Actualizar el bottom para la próxima barra
        
        # Mostrar etiquetas solo si el valor es mayor que 0
        labels = [str(count) if count > 0 else "" for count in counts]  # Crear etiquetas solo para valores > 0
        ax.bar_label(p, labels=labels, label_type='center', fontsize=12)  # Aplicar las etiquetas
        

    # Configurar etiquetas y título
    ax.set_ylabel('Nº de publicaciones', fontsize=16)
    ax.set_title('Nº de publicaciones por Mes', fontsize=16)

    # Configurar el tamaño de los ticks del eje X y Y
    ax.tick_params(axis='x', labelsize=12)  # Tamaño de los valores en el eje X
    ax.tick_params(axis='y', labelsize=12)  # Tamaño de los valores en el eje Y

    # Ajusta la rotación y la alineación de las etiquetas del eje x (meses) para mejorar la legibilidad y evitar que se superpongan.
    plt.xticks(rotation=45, ha="right")

    # Mostrar la leyenda
    ax.legend(fontsize=12)  # Tamaño de la leyenda

    # Mostrar la gráfica en Streamlit
    st.pyplot(fig)

    # Guardar en archivo
    plt.savefig('grap.png', bbox_inches='tight')

def main():
    st.title("Gráfica de publicaciones por mes (Stacked Bar Chart)")
    data = fetch_data()
    
    if data:
        plot_stacked_bar_chart(data)

if __name__ == "__main__":
    main()