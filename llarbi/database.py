import mysql.connector

def get_database_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="billarG8",
        port="3308"
    )
    return connection

def get_column_names(table_name):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        query = f"DESCRIBE {table_name}"
        cursor.execute(query)
        column_names = [row[0] for row in cursor.fetchall()]

        cursor.close()
        connection.close()

        return column_names
    except Exception as e:
        print("Error al obtener nombres de columnas:", e)
        return []

def get_user_data_by_id(user_id):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        user_data = cursor.fetchone()

        cursor.close()
        connection.close()

        return user_data
    except Exception as e:
        print("Error al obtener datos del usuario por ID:", e)
        return None
    
    

def get_partida_data_by_id(idPartida):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        query = "SELECT * FROM partida WHERE idPartida = %s"
        cursor.execute(query, (idPartida,))
        partida_data = cursor.fetchone()

        cursor.close()
        connection.close()

        return partida_data
    except Exception as e:
        print("Error al obtener datos de la partida por ID:", e)
        return None


def get_data_from_database(table_name):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        data = cursor.fetchall()

        cursor.close()
        connection.close()

        return data
    except Exception as e:
        print("Error al obtener datos de la base de datos:", e)
        return []

def insert_data_into_database(table_name, data):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        placeholders = ", ".join(["%s"] * len(data[0]))
        columns = ", ".join(data[0].keys())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        for row in data:
            values = tuple(row.values())
            cursor.execute(query, values)

        connection.commit()
        cursor.close()
        connection.close()

        return True
    except Exception as e:
        print("Error al insertar datos en la base de datos:", e)
        return False


def update_user_in_database(table_name, user_id, new_data):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        # Define la lista de actualizaciones en el formato "columna = %s"
        updates = [f"{column} = %s" for column in new_data.keys()]

        # Convierte la lista en una cadena separada por comas
        update_str = ", ".join(updates)

        query = f"UPDATE {table_name} SET {update_str} WHERE user_id = %s"  # Suponiendo que el ID del usuario es "user_id"
        values = list(new_data.values())
        values.append(user_id)  # Agrega el ID del usuario al final

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return True
    except Exception as e:
        print("Error al actualizar datos en la base de datos:", e)
        return False
    
    
def update_partida_in_database(table_name, idPartida, new_data):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        # Define la lista de actualizaciones en el formato "columna = %s"
        updates = [f"{column} = %s" for column in new_data.keys()]

        # Convierte la lista en una cadena separada por comas
        update_str = ", ".join(updates)

        query = f"UPDATE {table_name} SET {update_str} WHERE idPartida = %s"  # Suponiendo que el ID del usuario es "idPartida"
        values = list(new_data.values())
        values.append(idPartida)  # Agrega el ID de la partida al final

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return True
    except Exception as e:
        print("Error al actualizar datos en la base de datos:", e)
        return False


def delete_user_from_database(table_name, user_id):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        query = f"DELETE FROM {table_name} WHERE user_id = %s"  # Suponiendo que el ID del usuario es "user_id"
        cursor.execute(query, (user_id,))
        connection.commit()

        cursor.close()
        connection.close()

        return True
    except Exception as e:
        print("Error al eliminar usuario de la base de datos:", e)
        return False




def delete_partida_from_database(table_name, idPartida):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        query = f"DELETE FROM {table_name} WHERE idPartida = %s"  # Suponiendo que el ID del usuario es "idPartida"
        cursor.execute(query, (idPartida,))
        connection.commit()

        cursor.close()
        connection.close()

        return True
    except Exception as e:
        print("Error al eliminar usuario de la base de datos:", e)
        return False
