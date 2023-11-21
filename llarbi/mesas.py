from flask import Blueprint, render_template, request, redirect, url_for
from database import get_database_connection
from mysql.connector.errors import IntegrityError
import mysql.connector

mesas_bp = Blueprint('mesas', __name__)

@mesas_bp.route('/mapa_mesas', methods=['GET', 'POST'])
def mapa_mesas():
    if request.method == 'POST':
        cantidad_mesas_a_agregar = int(request.form.get('cantidad_mesas', 0))
        if cantidad_mesas_a_agregar > 0:
            agregar_mesas(cantidad_mesas_a_agregar)

    mesas_info = obtener_informacion_mesas()
    print(mesas_info)
    return render_template('mapa_mesas.html', mesas_info=mesas_info)

def agregar_mesas(cantidad_mesas):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        for i in range(1, cantidad_mesas + 1):
            insert_query = """
                INSERT INTO partida (idMesa, NumeroMesa, Ocupada)
                VALUES (%s, %s, FALSE)
            """
            mesa_data = (i, i)
            cursor.execute(insert_query, mesa_data)

        connection.commit()
        cursor.close()
        connection.close()

    except IntegrityError as e:
        print("Error de integridad:", e)
        print("Mensaje de la base de datos:", e.args[1])
    except Exception as e:
        print("Error al agregar mesas:", e)

def obtener_informacion_mesas():
    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        select_query = """
            SELECT NumeroMesa, Ocupada, GameMode, Players, HoraInicio
            FROM partida
        """
        cursor.execute(select_query)
        mesas_info = cursor.fetchall()

        cursor.close()
        connection.close()

        return mesas_info

    except Exception as e:
        print("Error al obtener información de las mesas:", e)
        return []

@mesas_bp.route('/finalizar_partida/<int:numero_mesa>', methods=['POST'])
def finalizar_partida(numero_mesa):
    if request.method == 'POST':
        hora_fin = request.form.get("HoraFin")

        try:
            db_connection = get_database_connection()
            cursor = db_connection.cursor()

            select_query = "SELECT * FROM partida WHERE NumeroMesa = %s AND Ocupada = TRUE ORDER BY idPartida DESC LIMIT 1"
            cursor.execute(select_query, (numero_mesa,))
            partida = cursor.fetchone()

            if partida:
                tiempo_jugado_minutos = partida['GameTime'].seconds // 60

                cursor.execute("UPDATE partida SET HoraFin = %s WHERE idPartida = %s", (hora_fin, partida['idPartida']))
                cursor.execute("UPDATE partida SET GameTime = TIMEDIFF(HoraFin, HoraInicio) WHERE idPartida = %s", (partida['idPartida'],))

                costo_por_minuto = partida['CostoPorMinuto']
                costo_total = tiempo_jugado_minutos * costo_por_minuto
                cursor.execute("UPDATE partida SET CostoTotal = %s WHERE idPartida = %s", (costo_total, partida['idPartida']))

                cursor.execute("UPDATE partida SET Ocupada = FALSE WHERE idPartida = %s", (partida['idPartida'],))

                db_connection.commit()

                cursor.close()
                db_connection.close()

                return redirect(url_for('mesas.mapa_mesas'))

            else:
                return "No se encontraron partidas para actualizar en la mesa {}".format(numero_mesa)

        except mysql.connector.Error as error:
            return "Error al finalizar la partida: " + str(error)

    return "Algo salió mal"