import random
import string
import json
import cryptography
from cryptography.fernet import Fernet, InvalidToken
import os

charset = string.ascii_letters + string.digits + string.punctuation

def checkFiles():
    if os.path.exists("key.key"):
        with open('key.key', 'rb') as keyfile:
            global key
            key = keyfile.read()
    else:
        with open('key.key', 'wb') as keyfile:
            key = Fernet.generate_key()
            keyfile.write(key)

    if os.path.exists('passfile.dat') == False:
        with open('passfile.dat', 'w') as passfile:
            passfile.write("{ }")

def generatePassword(length, name):
    try:
        test = length + 1
    except TypeError:
        print("Inputed length is not a number!")
        return 2
    
    passdata = loadPasswords()
    
    if name in passdata.keys():
        return 1
    else:
        passdata[name] = (''.join(random.choice(charset) for i in range(length)))
        writePasswords(passdata)
        return 0

def loadPasswords():
    with open('passfile.dat', 'r') as passfile:
        fernet = Fernet(key)
        encrypted = passfile.read()
        try:
            decrypted = fernet.decrypt(bytes(encrypted, 'utf-8'))
            
            # I truly have no idea why you have to run json.loads twice but it works so I roll with it

            decryptedpart2 = json.loads(decrypted.decode('utf-8'))
            return json.loads(decryptedpart2)
        except cryptography.fernet.InvalidToken:
            return json.loads(encrypted)

def writePasswords(passdata):
    with open('passfile.dat', 'w') as passfile:
        fernet = Fernet(key)
        passdatas = json.dumps(passdata)
        encrypted = fernet.encrypt(bytes(json.dumps(passdatas), 'utf-8'))
        passfile.write(encrypted.decode())