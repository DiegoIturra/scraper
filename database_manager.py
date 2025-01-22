import psycopg2
from psycopg2 import pool
from threading import Lock

class DatabaseManager:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, db_config):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._pool = pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                user=db_config["user"],
                password=db_config["password"],
                host=db_config["host"],
                port=db_config["port"],
                database=db_config["database"]
            )
    
    def get_connection(self):
        try:
            return self._pool.getconn()
        except Exception as e:
            print(f"Error getting a connection: {e}")
            raise
    
    def release_connection(self, connection):
        try:
            self._pool.putconn(connection)
        except Exception as e:
            print(f"Error releasing connection: {e}")
            raise
    
    def close_all_connections(self):
        try:
            self._pool.closeall()
        except Exception as e:
            print(f"Error al cerrar todas las conexiones: {e}")
            raise


# Ejemplo de uso
# if __name__ == "__main__":
    # # Obtenemos la instancia única
    # database_manager = DatabaseManager(database_config)

    # # Obtenemos una conexión
    # conn = database_manager.get_connection()

    # # Usamos la conexión (ejemplo de ejecución de consulta)
    # try:
    #     with conn.cursor() as cursor:
    #         cursor.execute("SELECT NOW()")
    #         result = cursor.fetchone()
    #         print("Hora actual en la base de datos:", result)
    # finally:
    #     # Liberamos la conexión al pool
    #     database_manager.release_connection(conn)

    # # Cerramos todas las conexiones al finalizar
    # database_manager.close_all_connections()