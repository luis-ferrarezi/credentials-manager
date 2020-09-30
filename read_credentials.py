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


def read_login(local):
    return data[local]['login']


# TODO adicionar um 'check_local'
# TODO levar o read e decryp para as property
# TODO utilizando o 'check_local' antes deles


class ShowCredentials(object):
    def __init__(self, local):
        self.local = local
        self.msgKeyError = local + ' not available, use .check_locals'
        if self.local not in data:
            print(self.msgKeyError)
    @property
    def login(self):
        try:
            return read_login(self.local)
        except KeyError:
            print(self.msgKeyError)

    @property
    def password(self):
        try:
            return decrypt_password(self.local)
        except KeyError:
            print(self.msgKeyError)

    @property
    def check_locals(self):
        return data.keys()

# verificar users de um local → 'esse local contém 0 login'
