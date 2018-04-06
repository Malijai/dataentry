from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from base64 import b64encode, b64decode


class Encrypter(object):
    def __init__(self):
        self.key_pair = RSA.generate(2048)

    def save_key(self, key_filename):
        f = open(key_filename, 'wb')
        f.write(self.key_pair.exportKey('PEM'))
        f.close()

    def save_public_key(self, key_filename):
        f = open(key_filename, 'wb')
        f.write(self.key_pair.publickey().exportKey('PEM'))
        f.close()

    def read_key(self, key_filename):
        private_key = RSA.importKey(open(key_filename,"rb").read())
        return private_key

    def encrypt(self, message, public_key):
        cipher = PKCS1_OAEP.new(public_key)
        ciphertext = cipher.encrypt(message.encode('utf-8'))
        s = b64encode(ciphertext)
        return s.decode('utf-8')

    def decrypt(self, ciphertext, private_key):
        decript_cypher = PKCS1_OAEP.new(private_key)
        if ciphertext is None:
            return ''
        decripted = decript_cypher.decrypt(b64decode(ciphertext.encode('utf-8'))).decode('utf-8')
        return decripted
