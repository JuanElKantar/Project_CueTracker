# Importa los módulos necesarios

from flask import Blueprint, render_template, request, redirect, flash
from database import get_data_from_database, get_database_connection, update_user_in_database, delete_partida_from_database
from database import delete_user_from_database, get_user_data_by_id, get_partida_data_by_id, update_partida_in_database

# Crea el Blueprint para la administración

admin_bp = Blueprint('admin', __name__)

# Ruta para /admin
@admin_bp.route('/admin')
def admin():
    # Agrega aquí la lógica que deseas para la vista de administrador
    return render_template('admin.html')  # Cambia 'admin.html' por tu plantilla correspondiente

# Ruta para mostrar la lista de usuarios registrados
@admin_bp.route('/admin/users')
def show_users():
    # Obtén los datos de usuarios de la base de datos
    users = get_data_from_database('users')

    # Renderiza una plantilla HTML para mostrar la lista de usuarios y pasa los datos de los usuarios
    return render_template('usersview.html', users=users)

# Ruta para editar un usuario por su ID
@admin_bp.route('/admin/editaruser/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'GET':
        # Obtén los datos del usuario por su ID desde la base de datos
        user_data = get_user_data_by_id(user_id)  # Implementa esta función para obtener los datos del usuario
        return render_template('editaruser.html', user=user_data)

    if request.method == 'POST':
        # Obtiene los nuevos datos del usuario del formulario
        new_data = {
            'userName': request.form['username'],
            'lastName': request.form['apellido'],
            'password_user': request.form['password'],
            'nodocumento': request.form['documento'],
            'email': request.form['email'],
            'id_rol': request.form['rol']
        }

        if update_user_in_database('users', user_id, new_data):
            flash('Usuario actualizado exitosamente', 'success')
        else:
            flash('Error al actualizar el usuario', 'error')
        return redirect('/admin/users')

# Ruta para eliminar un usuario por su ID
# Ruta para eliminar un usuario por su ID
@admin_bp.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if delete_user_from_database('users', user_id):
        flash('Usuario eliminado exitosamente', 'success')
    else:
        flash('Error al eliminar el usuario', 'error')
    return redirect('/admin/users')




# Ruta para mostrar la lista de partidas registrados
@admin_bp.route('/admin/partida')
def show_partida():
    # Obtén los datos de usuarios de la base de datos
    partida = get_data_from_database('partida')

    # Renderiza una plantilla HTML para mostrar la lista de usuarios y pasa los datos de los usuarios
    return render_template('partidasview.html', partida=partida)



