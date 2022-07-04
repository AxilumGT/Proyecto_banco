import getpass
from usuario_banco import UsuarioBanco
from usuario_dao import UsuarioDAO
import sys


class MenuBanco:
    @staticmethod
    def start_menu():
        print('Bienvenido al Banco\n')
        while True:
            try:
                option = int(input(f'[1] Ingresar cuenta\n'
                                   f'[2] Crear cuenta\n'
                                   f'[3] Salir\n\n'
                                   f'Elija una opción según los números mostrados: '))
                if option == 1:
                    user = MenuBanco.get_user_password()
                    MenuBanco.personal(user)
                elif option == 2:
                    user = UsuarioBanco()
                    UsuarioDAO.insertar(user)
                    continue
                elif option == 3:
                    print('Fin de la aplicación')
                    sys.exit()
                else:
                    raise ValueError('Opción no válida')

            except Exception as e:
                print('Ocurrio un error:', e)


    @staticmethod
    def personal(user):
        print(f'Bienvenido al banco {user.name} {user.last_name}')
        while True:
            try:
                option = int(input(f'\nPuedes ejecutar las siguientes opciones:\n'
                                   f'[1] Transferir\n'
                                   f'[2] Consulta de datos\n'
                                   f'[3] Modificar cuenta\n'
                                   f'[4] Salir de la cuenta\n'
                                   f'Introduzca la opción deseada: '))
                if option == 1:
                    MenuBanco.transferir(user)
                elif option == 2:
                    print(user)
                elif option == 3:
                    while True:
                        option = int(input(f'Puede modificar su contraseña y el correo electronico unicamente\n'
                                           f'[1] Contraseña\n'
                                           f'[2] Correo electrónico\n'
                                           f'[3] Salir\n'
                                           f'Introduzca la opción deseada: '))
                        if option == 1:
                            user.password = user.validate_pass()
                            continue
                        elif option == 2:
                            user.mail = user.validate_mail()
                            continue
                        elif option == 3:
                            UsuarioDAO.update(user.password, user.mail, user.money, user.id_account)
                            break
                        else:
                            print('Opción no válida, intente nuevamente')
                            continue
                elif option == 4:
                    print('Fin de la sesión')
                    break

            except Exception as e:
                print('Ocurrio un error:', e)


    @staticmethod
    def get_user_password():
        for count in range(3):
            username = str(input('Introduzca su usuario: '))
            password = getpass.getpass('Introduzca su contraseña: ')
            user = UsuarioDAO.iniciar_sesion(username, password)
            if user is None:
                print('El usuario o contraseña estan errados, intentelo nuevamente')
                continue
            else:
                return user
        print(f'Ha alcanzado el limite de intentos permitidos\n'
              f'Fin del programa')
        sys.exit()

    @staticmethod
    def transferir(user):
        id_account = str(input('Introduzca el ID de la cuenta a transferir: '))
        amount = float(input('Introduzca la cantidad a transferir: '))
        user2 = UsuarioDAO.select_id_account(id_account)
        prueba = user.money - amount
        if prueba < user.MONEY_MIN:
            print('La transacción no fue ejecutada (Monto insuficiente)')
        else:
            user.money = user.money - amount
            UsuarioDAO.update(user.password, user.mail, user.money, user.id_account)
            user2.money = user2.money + amount
            UsuarioDAO.update(user2.password, user2.mail, user2.money, user2.id_account)


if __name__ == '__main__':
    MenuBanco.start_menu()
