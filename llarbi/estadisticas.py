from flask import Blueprint, render_template
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from database import get_database_connection

# Cambié el nombre del blueprint a estadisticas_bp
estadisticas_bp = Blueprint('estadisticas', __name__)

# Obtener la conexión a la base de datos
conexion = get_database_connection()

@estadisticas_bp.route('/estadisticas')
def estadisticas():
    # Supongamos que tienes una función get_database_connection que devuelve una conexión a tu base de datos
    conexion = get_database_connection()

    # Consulta SQL para obtener las estadísticas de partidas de billar con información de gamemode
    consulta_sql = "SELECT gamemode, COUNT(*) as cantidad FROM partida GROUP BY gamemode"

    # Cargar datos desde la base de datos
    datos_partida = pd.read_sql_query(consulta_sql, conexion)

    # Cerrar la conexión
    conexion.close()

    # Crear un gráfico de barras para mostrar las opciones y cantidad de veces que se repite
    plt.bar(datos_partida['gamemode'], datos_partida['cantidad'], alpha=0.7)

    plt.title('Estadísticas de Partidas de Billar por Gamemode')
    plt.xlabel('Gamemode')
    plt.ylabel('Cantidad de Veces')
    plt.xticks(rotation=45, ha='right')  # Rotar etiquetas en el eje x para mayor legibilidad

    # Guardar el gráfico como un archivo PNG en memoria
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)

    # Convertir la imagen a base64 para mostrar en HTML
    img_data = base64.b64encode(img_buf.read()).decode('utf-8')

    # Renderizar la plantilla con el gráfico incrustado
    return render_template('grafico.html', img_data=img_data)
