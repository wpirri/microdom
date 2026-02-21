import mysql.connector
from mysql.connector import Error


def mysql_connect(host, database, user, password):
    """
    Abre una conexión a MySQL y devuelve el objeto connection.
    """
    try:
        conn = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None


def mysql_disconnect(conn):
    """
    Cierra la conexión si está abierta.
    """
    if conn and conn.is_connected():
        conn.close()


def mysql_execute(conn, query, params=None):
    """
    Ejecuta un query INSERT/UPDATE/DELETE.
    Devuelve True si tuvo éxito.
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return True
    except Error as e:
        print(f"Error ejecutando query: {e}")
        return False
    finally:
        cursor.close()


def mysql_query(conn, query, params=None):
    """
    Ejecuta un SELECT y devuelve todas las filas.
    """
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        return cursor.fetchall()
    except Error as e:
        print(f"Error ejecutando SELECT: {e}")
        return None
    finally:
        cursor.close()