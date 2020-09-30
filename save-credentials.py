from cryptography.fernet import Fernet
import ctypes
import os
import time
import sys


def create_key(file_mode='w'):
    file_name = 'key.key'
    with open(file_name, file_mode) as key_in:
        key = Fernet.generate_key()
        key_in.write(key.decode())
        ctypes.windll.kernel32.SetFileAttributesW(file_name, 2)
    return key


def check_key():
    try:
        with open('key.key', 'r') as key_in:
            chars = key_in.read()
            if len(chars):
                return chars.encode()

            return create_key(file_mode='a')

    except FileNotFoundError:
        return create_key(file_mode='w')


class Credentials:
    def __init__(self, key=check_key()):
        self.__local = ""
        self.__username = ""
        self.__key = key
        self.__password = ""

    @property
    def local(self):
        return self.__local

    @local.setter
    def local(self, local):
        while local == '':
            local = input('Enter a proper User name, blank is not accepted:')
        self.__local = local

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username):
        while username == '':
            username = input('Enter a proper User name, blank is not accepted:')
        self.__username = username

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        print(self.__key)
        f = Fernet(self.__key)
        self.__password = f.encrypt(password.encode()).decode()
        del f

    def create_cred(self):
        cred_filename = 'CredFile.ini'

        with open(cred_filename, 'a') as file_in:
            file_in.write("Local={}\nUsername={}\nPassword={}\n"
                          .format(self.__local, self.__username, self.__password))
            file_in.write("++" * 20 + "\n")


# TODO tinha todos itens aqui

# TODO colocar para salvar o local tbm no CredFile
# TODO ajustar para manusear tudo como dicionário de dicionários
#  {
#        'LOCALX':{
#         User: Y,
#         Senha: Z
#         },
#        'LocalX2':{
#         User: Y2,
#         Senha: Z2
#         }
#  }

def main():
    # Creating an object for Credentials class
    creds = Credentials()

    # Accepting credentials
    creds.local = input("Enter Local:")
    creds.username = input("Enter UserName:")
    creds.password = input("Enter Password:")

    # calling the Credit
    creds.create_cred()
    print("**" * 20)
    print("Cred file created successfully at {}"
          .format(time.ctime()))

    print("**" * 20)


if __name__ == "__main__":
    main()
