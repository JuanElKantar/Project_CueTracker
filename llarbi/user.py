from flask import Blueprint, render_template, session
from login import obtener_nombre_jugador  # Asegúrate de importar la función adecuada

user_bp = Blueprint('user', __name__)

# Ruta para /user
@user_bp.route('/user')
def user():
    # Accede a la información del jugador desde la sesión
    jugador_id = session.get('user_id')
    nombre_jugador = session.get('nombre_jugador')

    # Imprime la información para debug
    print("ID del jugador:", jugador_id)
    print("Nombre del jugador:", nombre_jugador)

    # Resto del código...


    # Agrega aquí la lógica que deseas para la vista de usuario
    # Puedes utilizar jugador_id y nombre_jugador en tu lógica

    return render_template('user.html', jugador_id=jugador_id, nombre_jugador=nombre_jugador)
