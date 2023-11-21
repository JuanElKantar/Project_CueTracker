from flask import Blueprint, request, redirect, session, url_for
from datetime import datetime, timedelta
import mysql.connector
from database import get_database_connection


partida_bp = Blueprint('partida', __name__)

@partida_bp.route('/finalizar_partida', methods=['POST'])
def finalizar_partida():
    
    jugador_id = session.get('user_id')
    nombre_jugador = session.get('nombre_jugador')
    
    print("ID del jugador:", jugador_id)
    print("Nombre del jugador:", nombre_jugador)
    
    if request.method == 'POST':
        hora_fin = request.form.get("HoraFin")
        puntaje_local = request.form.get("puntaje_local")

        try:
            db_connection = get_database_connection()
            cursor = db_connection.cursor()

            select_query = "SELECT * FROM partida WHERE Ocupada = TRUE ORDER BY idPartida DESC LIMIT 1"
            cursor.execute(select_query)
            partida = cursor.fetchone()

            if partida:
                # ... (código existente)

                # Insertar puntaje en la tabla estadisticas
                insertar_puntaje(jugador_id=partida[9], puntaje_partida=puntaje_local)

                cursor.execute("UPDATE partida SET Ocupada = FALSE WHERE idPartida = %s", (partida[0],))  # Marcar la mesa como desocupada
                db_connection.commit()

                cursor.close()
                db_connection.close()

                return redirect(url_for('login.login'))  # Redirigir a la página de inicio de sesión
            else:
                return "No se encontraron partidas ocupadas para finalizar"

        except mysql.connector.Error as error:
            return "Error al finalizar la partida: " + str(error)

    return "Algo salió mal"

def calcular_puntaje_partida(partida):
    # Agrega lógica para calcular el puntaje de la partida según tus reglas
    # En este ejemplo, simplemente se devuelve la duración de la partida en minutos como puntaje
    tiempo_jugado = partida[8]  # Índice 8 es GameTime
    minutos_jugados = tiempo_jugado.seconds // 60
    return minutos_jugados

def insertar_puntaje(jugador_id, puntaje_partida):
    try:
        # Obtener la conexión a la base de datos
        connection = get_database_connection()

        # Crear un cursor para ejecutar consultas
        cursor = connection.cursor()

        # Obtener la fecha actual
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Insertar datos en la tabla estadisticas
        insert_query = """
            INSERT INTO estadisticas (jugador_id, puntajePartida, fechaUltimaPartida)
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (jugador_id, puntaje_partida, fecha_actual))

        # Confirmar los cambios en la base de datos
        connection.commit()

        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

        print("Puntaje insertado correctamente")

        return {"status": "success"}
    

    except Exception as e:
        print("Error al insertar puntaje:", str(e))
        return {"status": "error", "message": str(e)}
