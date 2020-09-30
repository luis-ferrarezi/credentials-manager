from cryptography.fernet import Fernet
import json

cred_filename = 'CredFile.ini'
key_file = 'key.key'


with open('key.key', 'r') as key_in:
    key = key_in.read().encode()


# TODO colocar para selecionar o local/usuário e retornar o respectivo password

f = Fernet(key)

with open(cred_filename, 'r') as cred_in:
    lines = cred_in.readlines()
    dict_local = {}
    dict_creds_temp = {}
    for line in lines:
        tuples = line.rstrip('\n').split('=', 1)
        #print(tuples)
        if tuples[0] in ('Local', 'Username', 'Password'):
            dict_creds_temp[tuples[0]] = tuples[1]
            if len(dict_creds_temp) == 3:
                dict_local[dict_creds_temp['Local']] = {
                    'Username': dict_creds_temp['Username'],
                    'Password': dict_creds_temp['Password']
                }
    print(dict_local)
    with open('data.json', 'w') as outfile:
        json.dump(dict_local, outfile)
    passwd = f.decrypt(dict_creds_temp['Password'].encode()).decode()
    print("Password:", passwd)