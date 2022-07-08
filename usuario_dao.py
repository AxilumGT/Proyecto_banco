import bcrypt
from cursor_pool import CursorPool
from usuario_banco import UsuarioBanco


class UsuarioDAO:
    _SELECT = 'SELECT * FROM account_bank'
    _INSERT = 'INSERT INTO account_bank(id_account, username, password, mail, name, last_name, money)' \
              'VALUES (%s, %s, %s, %s, %s, %s, %s)'
    _UPDATE = 'UPDATE account_bank SET password=%s, mail=%s, money=%s WHERE id_account=%s'
    _DELETE = 'DELETE FROM account_bank WHERE id_account=%s'

    @classmethod
    def iniciar_sesion(cls, mail, password):
        # Esta función busca en la base de datos el mail de entrada y si existe obtiene todos los datos
        # del usuario, ademas de verificar si la contraseña es correcta
        txt = ' WHERE mail=%s'
        with CursorPool() as cursor:
            try:
                cursor.execute(cls._SELECT + txt, (mail,))
                registro = cursor.fetchone()
                if bcrypt.checkpw(password.encode(), registro[2].encode()):
                    print(registro)
                    persona = UsuarioBanco(registro[0], registro[1], registro[2], registro[3],
                                           registro[4], registro[5], registro[6])
                    print('Se ha obtenido el usuario correctamente')
                else:
                    raise NameError('El usuario no se ha encontrado')

            except Exception as e:
                print('Ocurrio un error:', e)
                persona = None
            finally:
                return persona

    @classmethod
    def select_id_account(cls, id_account):
        # Busca el ID del usuario y se obtiene todos los datos del usuario para crear un objeto UsuarioBanco
        txt = ' WHERE id_account=%s'
        with CursorPool() as cursor:
            cursor.execute(cls._SELECT + txt, (id_account,))
            registro = cursor.fetchone()
            print(registro)
            persona = UsuarioBanco(registro[0], registro[1], registro[2], registro[3],
                                   registro[4], registro[5], registro[6])
            print('Se ha obtenido el usuario correctamente')
            return persona

    @classmethod
    def select_all(cls):
        with CursorPool() as cursor:
            cursor.execute(cls._SELECT)
            registros = cursor.fetchall()
            for registro in registros:
                print(registro)

    @classmethod
    def insertar(cls, user):
        with CursorPool() as cursor:
            txt = ' WHERE mail=%s'
            cursor.execute(cls._SELECT + txt, (user.mail,))
            registro = cursor.fetchone()
            if registro[3] == user.mail:
                raise ValueError('El mail existe, no se puede registrar el usuario')
            else:
                valores = (user.id_account, user.username, user.password, user.mail,
                           user.name, user.last_name, user.money)
                cursor.execute(cls._INSERT, valores)
                print(f'Usuario insertado: {user}')

    @classmethod
    def update(cls, password, mail, money, id_account):
        with CursorPool() as cursor:
            cursor.execute(cls._UPDATE, (UsuarioBanco.encrypt(password), mail, money, id_account))
            print(f'Los cambios han sido realizados')

    @classmethod
    def eliminar(cls, id_account):
        with CursorPool() as cursor:
            user = UsuarioDAO.select_id_account(id_account)
            cursor.execute(cls._DELETE, (id_account,))
            print(f'El usuario ID:{id_account}-USER:{user.username} fue eliminado de la base de datos')


if __name__ == '__main__':
    user = UsuarioDAO.select_id_account('04744214')
    UsuarioDAO.eliminar(user.id_account)
