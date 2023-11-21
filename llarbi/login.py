from flask import Blueprint, render_template, request, redirect, session, flash
from database import get_database_connection

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST', 'GET'])
def login():
    show_error = False  # Variable para controlar si se muestra un mensaje de error

    if request.method == 'POST':
        nodocumento = request.form['nodocumento']
        password = request.form['password']

        if not nodocumento or not password:
            show_error = True
        else:
            connection = get_database_connection()
            cursor = connection.cursor()

            query = "SELECT user_id, password_user, id_rol FROM users WHERE nodocumento = %s"
            cursor.execute(query, (nodocumento,))
            user_data = cursor.fetchone()

            if user_data is not None:
                user_id, stored_password, id_rol = user_data
                if password == stored_password:
                    # Guardar la información del jugador en la sesión
                    session['user_id'] = user_id
                    session['nombre_jugador'] = obtener_nombre_jugador(user_id)  # Debes implementar esta función

                    flash('Inicio de sesión exitoso')
                    if id_rol == 1:
                        return redirect('/admin')
                    elif id_rol == 2:
                        return redirect('/user')
                    else:
                        flash('El usuario tiene un rol no válido.', 'error')
                        show_error = True
                else:
                    flash('Credenciales fallidas. Contraseña incorrecta. Por favor, inténtalo nuevamente.', 'error')
                    show_error = True
            else:
                flash('Credenciales fallidas. Usuario no encontrado. Por favor, verifica tus credenciales.', 'error')
                show_error = True

    return render_template('index.html', show_error=show_error)

def obtener_nombre_jugador(user_id):
    # Debes implementar esta función para obtener el nombre del jugador a partir del ID
    # Puedes realizar una consulta a la base de datos u obtener el nombre de otra manera
    # Aquí te doy un ejemplo básico que puedes adaptar según tu esquema de base de datos
    connection = get_database_connection()
    cursor = connection.cursor()

    query = "SELECT userName FROM users WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        return None
