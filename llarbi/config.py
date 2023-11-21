from flask import Blueprint, render_template, request, redirect, session, url_for
from database import get_database_connection
from mysql.connector.errors import IntegrityError
import datetime


config_bp = Blueprint('config', __name__)

def is_mesa_ocupada(numero_mesa):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        select_query = "SELECT Ocupada FROM partida WHERE NumeroMesa = %s AND Ocupada = TRUE ORDER BY idPartida DESC LIMIT 1"
        cursor.execute(select_query, (numero_mesa,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        if result:
            return True  # Si se encuentra una partida ocupada, la mesa está ocupada
        else:
            return False  # Si no se encuentra una partida ocupada, la mesa está desocupada
    except Exception as e:
        print("Error al verificar la ocupación de la mesa:", e)
        return True  # En caso de error, asumir que la mesa está ocupada


# ... (tu código anterior) ...

def insert_config_into_database(GameMode, Players, HoraInicio, NumeroMesa):
    try:
        # Obtener la conexión a la base de datos
        connection = get_database_connection()

        # Crear un cursor para ejecutar consultas
        cursor = connection.cursor()
        
        user_id = session.get('user_id')

        # Buscar la última partida de la mesa especificada
        select_query = """
            SELECT idMesa, Ocupada
            FROM partida
            WHERE NumeroMesa = %s
            ORDER BY idPartida DESC
            LIMIT 1
        """
        cursor.execute(select_query, (NumeroMesa,))
        last_config = cursor.fetchone()

        if last_config and not last_config[1]:
            # Si la última configuración existe y la mesa está libre, actualizar esa configuración
            update_query = """
                UPDATE partida
                SET GameMode = %s, Players = %s, HoraInicio = %s, Ocupada = TRUE
                WHERE idMesa = %s
            """
            config_data = (GameMode, Players, HoraInicio, last_config[0])
            cursor.execute(update_query, config_data)
        else:
            # Si la última mesa está ocupada o no existe, insertar una nueva configuración de partida
            insert_query = """
                INSERT INTO partida (NumeroMesa, GameMode, Players, HoraInicio, Ocupada)
                VALUES (%s, %s, %s, %s, TRUE)
            """
            config_data = (NumeroMesa, GameMode, Players, HoraInicio)
            cursor.execute(insert_query, config_data)

        # Confirmar los cambios en la base de datos
        connection.commit()

        return True  # Si la configuración se guarda correctamente, devuelve True

    except IntegrityError as e:
        # Imprimir detalles específicos del error de integridad
        print("Error de integridad:", e)
        print("Mensaje de la base de datos:", e.args[1])

        return False
    except Exception as e:
        # Imprimir detalles de otros errores
        print("Error al guardar la configuración de partida:", e)
        return False
    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()


@config_bp.route('/config', methods=['GET', 'POST'])
def config_handler():
    if request.method == 'POST':
        if "GameMode" in request.form and "Players" in request.form:
            GameMode = request.form["GameMode"]
            Players = request.form["Players"]
            HoraInicio = request.form["HoraInicio"]
            NumeroMesa = request.form["NumeroMesa"]

            # Verificar si la mesa está ocupada
            if is_mesa_ocupada(NumeroMesa):
                return "La mesa está ocupada. No se puede crear una nueva partida."

            # Guardar la configuración de la partida en la base de datos
            if insert_config_into_database(GameMode, Players, HoraInicio, NumeroMesa):
                if Players == "1":
                    return redirect(url_for('config.oneplayer_handler'))
                elif Players == "2":
                    return redirect(url_for('config.twoplayer_handler'))
                elif Players == "3":
                    return redirect(url_for('config.threeplayer_handler'))
                elif Players == "4":
                    return redirect(url_for('config.forplayer_handler'))
                else:
                    return "Número de jugadores no válido. Por favor, seleccione una cantidad válida."
            else:
                return "Error al guardar la configuración de partida. Por favor, inténtalo nuevamente."

    return render_template('config_partida.html')


@config_bp.route('/oneplayer', methods=['GET'])
def oneplayer_handler():
    return render_template('oneplayer.html')

@config_bp.route('/twoplayer', methods=['GET'])
def twoplayer_handler():
    return render_template('twoplayer.html')

@config_bp.route('/threeplayer', methods=['GET'])
def threeplayer_handler():
    return render_template('threeplayer.html')

@config_bp.route('/forplayer', methods=['GET'])
def forplayer_handler():
    return render_template('forplayer.html')