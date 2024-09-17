import requests
import streamlit as st 
import matplotlib.pyplot as plt 

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

# Función para generar la gráfica
def plot_bar_chart(data):
    for category, posts in data.items():
        months = list(posts.keys())
        counts = list(posts.values())

        fig, ax = plt.subplots()
        ax.bar(months, counts)
        ax.set_xlabel('Mes')
        ax.set_ylabel('Número de Posts')
        ax.set_title(f'Número de Posts por Mes en {category}')
        plt.xticks(rotation=45)

        st.pyplot(fig)

def main():
    st.title("Gráfica de Posts por Mes")
    data = fetch_data()
    
    if data:
        plot_bar_chart(data)

if __name__ == "__main__":
    main()
