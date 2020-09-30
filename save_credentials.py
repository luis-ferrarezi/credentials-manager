from cryptography.fernet import Fernet
import ctypes
import os
import time
import sys
import json


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
        f = Fernet(self.__key)
        self.__password = f.encrypt(password.encode()).decode()
        del f

    def save_to_json(self):
        cred_filename = 'credentials.json'
        data = {}
        if os.path.exists(cred_filename):
            with open(cred_filename, 'r') as old_file:
                data = json.load(old_file)

        data[self.local] = {
            'login': self.__username,
            'password': self.__password
        }

        with open(cred_filename, 'w') as save_file:
            json.dump(data, save_file, indent=4)


def main():
    # Creating an object for Credentials class
    creds = Credentials()

    # Accepting credentials
    creds.local = input("Enter Local:")
    creds.username = input("Enter UserName:")
    creds.password = input("Enter Password:")

    creds.save_to_json()
    print("**" * 20)
    print("Cred file created successfully at {}"
          .format(time.ctime()))
    print("**" * 20)


if __name__ == "__main__":
    main()
