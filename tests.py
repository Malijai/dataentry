from unittest import TestCase
from encrypter import Encrypter


class TestCrypto(TestCase):
    def test_can_generate_two_key_encrypt_and_decrypt(self):
        e = Encrypter()

        e.save_key('myprivatekey.pem')
        e.save_public_key('mypublickey.pem')

        public_key = e.read_key('mypublickey.pem')
        private_key = e.read_key('myprivatekey.pem')

        message = 'un texte'
        ciphertext = e.encrypt(message, public_key)
        decripted = e.decrypt(ciphertext, private_key)

        self.assertEqual(decripted, message)

