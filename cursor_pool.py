from conexion import Conexion


class CursorPool:
    def __init__(self):
        self._conexion = None
        self._cursor = None

    def __enter__(self):
        print('Iniciando el método with con __enter__')
        self._conexion = Conexion.get_connect()
        self._cursor = self._conexion.cursor()
        return self._cursor

    def __exit__(self, exc_type, exc_value, exc_tranceback):
        print('Se esta ejecutando el método __exit__')
        if exc_value:
            self._conexion.rollback()
            print(f'Ocurrio un error: {exc_type} {exc_value} {exc_tranceback}')
        else:
            self._conexion.commit()
            print('Se ha ejecutado un commit')
        self._cursor.close()
        Conexion.liberate_connect(self._conexion)


if __name__ == '__main__':
    with CursorPool() as cursor:
        print('Se abrió el pool')
        cursor.execute('SELECT * FROM account_bank')
