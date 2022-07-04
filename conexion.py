from psycopg2 import pool
import sys
from logging import log


class Conexion:
    _DATABASE = 'bank'
    _USERNAME = 'postgres'
    _PASSWORD = 'admin'
    _DB_PORT = '5433'
    _HOST = '127.0.0.1'
    _MIN_CON = 1
    _MAX_CON = 5
    _pool = None

    @classmethod
    def get_pool(cls):
        if cls._pool is None:
            try:
                cls._pool = pool.SimpleConnectionPool(cls._MIN_CON, cls._MAX_CON,
                                                      host=cls._HOST,
                                                      user=cls._USERNAME,
                                                      password=cls._PASSWORD,
                                                      port=cls._DB_PORT,
                                                      database=cls._DATABASE)
                print('Se ha conectado al pool correctamente')
                return cls._pool
            except Exception as e:
                print('Hubo un error al conectarse al pool:', e)
                sys.exit()
        else:
            return cls._pool

    @classmethod
    def get_connect(cls):
        conexion = cls.get_pool().getconn()
        print(f'La conexión ha sido exitosa {conexion}')
        return conexion

    @classmethod
    def liberate_connect(cls, conexion):
        cls.get_pool().putconn(conexion)
        print('Se ha cerrado la sesión')

    @classmethod
    def liberate_all(cls):
        cls.get_pool().closeall()
        print('Se ha cerrado todas las conexiones de la base de datos:', cls._DATABASE)


if __name__ == '__main__':
    variable1 = Conexion.get_connect()
    variable2 = Conexion.get_connect()
    variable3 = Conexion.get_connect()
    variable4 = Conexion.get_connect()
    variable5 = Conexion.get_connect()
    Conexion.liberate_connect(variable1)
    Conexion.liberate_all()

