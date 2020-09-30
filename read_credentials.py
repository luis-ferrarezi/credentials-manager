from cryptography.fernet import Fernet
import json

cred_filename = 'credentials.json'
key_file = 'key.key'

with open(cred_filename, 'r') as data_json:
    data = json.load(data_json)


def read_key():
    with open('key.key', 'r') as key_in:
        return key_in.read().encode()


def decrypt_password(local):
    key = read_key()
    f = Fernet(key)
    crypt_pass = data[local]['password']
    password = f.decrypt(crypt_pass.encode()).decode()
    return password


def read_username(local):
    return data[local]['login']

#TODO adicionar um 'check_local'
#TODO levar o read e decryp para as property
#TODO utilizando o 'check_local' antes deles
class ShowCredentials(object):
    def __init__(self, local):
        self.__username = read_username(local)
        self.__password = decrypt_password(local)

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password
