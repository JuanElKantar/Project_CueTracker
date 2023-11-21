from flask import Blueprint, render_template, request, flash, redirect
from database import get_database_connection

registrar_bp = Blueprint('registrar', __name__)

def is_nodocumento_unique(nodocumento):
    try:
        # Obtener la conexión a la base de datos
        connection = get_database_connection()

        # Crear un cursor para ejecutar consultas
        cursor = connection.cursor()

        # Realizar una consulta para verificar si el número de documento ya existe
        query = "SELECT COUNT(*) FROM users WHERE nodocumento = %s"
        cursor.execute(query, (nodocumento,))
        count = cursor.fetchone()[0]

        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

        return count == 0  # Si count es 0, el número de documento es único; de lo contrario, no es único.
    except Exception as e:
        print("Error al verificar el número de documento:", e)
        return False

def insert_user_into_database(userName, lastName, email, nodocumento, password_user):
    if not is_nodocumento_unique(nodocumento):
        return False  # El número de documento no es único, no se puede registrar el usuario.

    try:
        # Obtener la conexión a la base de datos
        connection = get_database_connection()

        # Crear un cursor para ejecutar consultas
        cursor = connection.cursor()

        # Resto del código para insertar el usuario (sin cambios)
        insert_query = """
            INSERT INTO users (userName, lastName, email, nodocumento, password_user, id_rol)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        user_data = (userName, lastName, email, nodocumento, password_user, 2)  # 2 es el id_rol deseado
        cursor.execute(insert_query, user_data)

        # Confirmar los cambios en la base de datos
        connection.commit()

        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

        return True
    except Exception as e:
        print("Error al registrar usuario:", e)
        return False

@registrar_bp.route("/registrar", methods=["GET", "POST"])
def registrar_handler():
    if request.method == 'POST':
        userName = request.form["userName"]
        lastName = request.form["lastName"]
        email = request.form["email"]
        nodocumento = request.form["nodocumento"]
        password_user = request.form["password_user"]

        if is_nodocumento_unique(nodocumento):
            if insert_user_into_database(userName, lastName, email, nodocumento, password_user):
                flash("Usuario registrado correctamente")
                return redirect('/')
            else:
                flash("Error al registrar usuario. Por favor, inténtalo nuevamente.")
        else:
            flash("El número de documento ya está en uso. Por favor, elige otro número de documento.")

    return render_template('registrar_usuario.html')
