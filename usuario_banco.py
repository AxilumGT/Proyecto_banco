import getpass
import numpy as np
import bcrypt


class UsuarioBanco:
    MONEY_MIN = 0

    def __init__(self, id_account=None, username=None, password=None,
                 mail=None, name=None, last_name=None, money=0.0):
        self.id_account = self.create_id_account(id_account)
        self.__username = self.validate_user(username)
        self.__password = self.validate_pass(password)
        self.__mail = self.validate_mail(mail)
        self.__name = self.validate_name('nombre', name)
        self.__last_name = self.validate_name('apellido', last_name)
        self.__money = money

    @staticmethod
    def validate_user(username):
        # Valida el nombre de usuario según ciertas condiciones
        # Conditional
        # Mayor a 8 caracteres y menor a 32
        # No contener elementos especiales
        if username is None:
            while True:
                username = str(input('Introduzca el nombre de usuario: '))
                try:
                    if (len(username) >= 8) and (len(username) <= 32):
                        for elemento in username:
                            if (not elemento.isalpha()) and (not elemento.isnumeric()):
                                raise ValueError('El nombre de usuario no debe contener caracteres especiales')
                        print('La nombre de usuario es correcto')
                        return username
                    else:
                        raise ValueError(
                            'El nombre de usuario no cumple con los requerimientos de longitud de caracteres [8-32]')

                except Exception as e:
                    print(f'Hubo un error: {e}')
        else:
            return username

    @staticmethod
    def validate_pass(password=None):
        # Valida la contraseña según ciertas condiciones
        # Esta funcion solo funciona con el terminal
        # Conditional
        # Mayor a 8 caracteres y menor a 32
        # Contener una letra minúscula
        # Contener una letra mayúscula
        # Tener 3 números
        # Contener un elemento especial
        if password is None:
            verificar = [False, False, False, [False, False, False], False]
            while True:
                password = getpass.getpass('Introduzca su contraseña: ')
                password_res = getpass.getpass('Introduzca nuevamente su contraseña: ')
                try:
                    if password == password_res:
                        if (len(password) >= 8) and (len(password) <= 32): verificar[0] = True
                        count = 0
                        for i in range(len(password)):
                            if password[i].isnumeric():
                                verificar[3][count] = True
                                count += 1
                                if count == 3: break
                        for elemento in password:
                            if elemento.islower(): verificar[1] = True
                            if elemento.isupper(): verificar[2] = True
                            if (not elemento.isalpha()) and (not elemento.isnumeric()): verificar[4] = True
                        for comprobar in verificar:
                            if isinstance(comprobar, list):
                                for re_comprobar in comprobar:
                                    if re_comprobar is False:
                                        raise ValueError('La contraseña no cumple con los requerimientos')
                            elif comprobar is False:
                                raise ValueError('La contraseña no cumple con los requerimientos')
                        print('La contraseña es correcta')
                        password = UsuarioBanco.encrypt(password)
                        return password
                    else:
                        raise ValueError('La contraseña no coincide con la repetición')
                except Exception as e:
                    print(f'Hubo un error: {e}')
        else:
            return password

    @staticmethod
    def validate_mail(mail=None):
        # Valida el correo electronico dependiendo del tipo de este
        if mail is None:
            able = np.array(['@gmail.com', '@hotmail.com', '@outlook.com'])
            while True:
                try:
                    mail = str(input('Introduzca su correo electronico: '))
                    for i in range(len(able)):
                        if mail.endswith(able[i]) or mail == '':
                            print('El correo electronico es válido')
                            return mail
                    raise ValueError('Este correo no esta permitido, intente uno nuevo')
                except Exception as e:
                    print(f'Hubo un error: {e}')
        else:
            return mail

    @staticmethod
    def validate_name(first_last, name):
        # Valida el nombre o el apellido dependiendo de ciertas condiciones
        # Conditional
        # Pide si es primer nombre o el apellido
        # Comenzar con mayúscula cada nuevo añadido
        # No contener caracteres especiales
        # Tener un máximo de 3 espaciados
        if name is None:
            while True:
                try:
                    name_fl = str(input(f'Introduzca su {first_last}: '))
                    if len(name_fl.split()) > 3:
                        raise ValueError(f'El {first_last} no debe contener más de 3 palabras')
                    for element in name_fl.split():
                        if not element[0].isupper():
                            raise ValueError(f'El {first_last} no comienza con mayúsculas')
                        for i in range(len(element)):
                            if (not element[i].isnumeric()) and (not element[i].isalpha()):
                                raise ValueError(f'El {first_last} no debe contener caracteres especiales')
                    return name_fl
                except Exception as e:
                    print(f'Hubo un error: {e}')
        else:
            return name

    @staticmethod
    def create_id_account(id_account):
        # Crea una ID aleatoria
        if id_account is None:
            characters = np.append(np.array(['a', 'b', 'c', 'd', 'e', 'f']), range(10))
            new_id = ''
            for i in range(8):
                new_id += np.random.choice(characters)
            return new_id
        else:
            return id_account

    @staticmethod
    def encrypt(password):
        # Permite encriptar la contraseña y la devuelve como tipo de dato de str
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=10))
        return hashed.decode()

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username):
        self.__username = username

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password

    @property
    def mail(self):
        return self.__mail

    @mail.setter
    def mail(self, mail):
        self.__mail = mail

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, last_name):
        self.__last_name = last_name

    @property
    def money(self):
        return self.__money

    @money.setter
    def money(self, amount):
        self.__money = float(amount)

    def __str__(self):
        return f'\nDatos del usuario:\n\n' \
               f'ID Cuenta: {self.id_account}\n' \
               f'Nombre de usuario: {self.__username}\n' \
               f'Correo electronico: {self.__mail}\n' \
               f'Nombre: {self.__name}\n' \
               f'Apellido: {self.__last_name}\n' \
               f'Monto: {self.__money}'
