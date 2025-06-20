import unittest
from unittest.mock import patch
from pbd_security import StringEncryptionService

class TestStringEncryptionService(unittest.TestCase):
    def setUp(self):
        self.service = StringEncryptionService()

    @patch('os.urandom', return_value=b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b')
    def test_encrypt_happy_path(self, mock_urandom):
        plain_text = "Hello, World!"
        pass_phrase = "securepass"
        salt = "somesalt"
        encrypted_text = self.service.encrypt(plain_text, pass_phrase, salt)
        expected_nonce = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b'.hex()
        self.assertIsNotNone(encrypted_text)
        self.assertTrue(encrypted_text.startswith(expected_nonce))

    def test_encrypt_empty_plain_text(self):
        plain_text = ""
        pass_phrase = "securepass"
        salt = "somesalt"
        encrypted_text = self.service.encrypt(plain_text, pass_phrase, salt)
        self.assertIsNone(encrypted_text)

    def test_encrypt_none_plain_text(self):
        plain_text = None
        pass_phrase = "securepass"
        salt = "somesalt"
        encrypted_text = self.service.encrypt(plain_text, pass_phrase, salt)
        self.assertIsNone(encrypted_text)

    def test_encrypt_empty_pass_phrase(self):
        plain_text = "Hello, World!"
        pass_phrase = ""
        salt = "somesalt"
        encrypted_text = self.service.encrypt(plain_text, pass_phrase, salt)
        self.assertIsNone(encrypted_text)

    def test_encrypt_none_pass_phrase(self):
        plain_text = "Hello, World!"
        pass_phrase = None
        salt = "somesalt"
        encrypted_text = self.service.encrypt(plain_text, pass_phrase, salt)
        self.assertIsNone(encrypted_text)

    def test_encrypt_empty_salt(self):
        plain_text = "Hello, World!"
        pass_phrase = "securepass"
        salt = ""
        encrypted_text = self.service.encrypt(plain_text, pass_phrase, salt)
        self.assertIsNone(encrypted_text)

    def test_encrypt_none_salt(self):
        plain_text = "Hello, World!"
        pass_phrase = "securepass"
        salt = None
        encrypted_text = self.service.encrypt(plain_text, pass_phrase, salt)
        self.assertIsNone(encrypted_text)

    def test_decrypt_happy_path(self):
        plain_text = "Hello, World!"
        pass_phrase = "securepass"
        salt = "somesalt"
        encrypted_text = self.service.encrypt(plain_text, pass_phrase, salt)
        decrypted_text = self.service.decrypt(encrypted_text, pass_phrase, salt)
        self.assertEqual(decrypted_text, plain_text)

    def test_decrypt_empty_encrypted_text(self):
        encrypted_text = ""
        pass_phrase = "securepass"
        salt = "somesalt"
        decrypted_text = self.service.decrypt(encrypted_text, pass_phrase, salt)
        self.assertIsNone(decrypted_text)

    def test_decrypt_none_encrypted_text(self):
        encrypted_text = None
        pass_phrase = "securepass"
        salt = "somesalt"
        decrypted_text = self.service.decrypt(encrypted_text, pass_phrase, salt)
        self.assertIsNone(decrypted_text)

    def test_decrypt_empty_pass_phrase(self):
        plain_text = "Hello, World!"
        pass_phrase = "securepass"
        salt = "somesalt"
        encrypted_text = self.service.encrypt(plain_text, pass_phrase, salt)
        decrypted_text = self.service.decrypt(encrypted_text, "", salt)
        self.assertIsNone(decrypted_text)

    def test_decrypt_none_pass_phrase(self):
        plain_text = "Hello, World!"
        pass_phrase = "securepass"
        salt = "somesalt"
        encrypted_text = self.service.encrypt(plain_text, pass_phrase, salt)
        decrypted_text = self.service.decrypt(encrypted_text, None, salt)
        self.assertIsNone(decrypted_text)

    def test_decrypt_empty_salt(self):
        plain_text = "Hello, World!"
        pass_phrase = "securepass"
        salt = "somesalt"
        encrypted_text = self.service.encrypt(plain_text, pass_phrase, salt)
        decrypted_text = self.service.decrypt(encrypted_text, pass_phrase, "")
        self.assertIsNone(decrypted_text)

    def test_decrypt_none_salt(self):
        plain_text = "Hello, World!"
        pass_phrase = "securepass"
        salt = "somesalt"
        encrypted_text = self.service.encrypt(plain_text, pass_phrase, salt)
        decrypted_text = self.service.decrypt(encrypted_text, pass_phrase, None)
        self.assertIsNone(decrypted_text)

    def test_decrypt_invalid_encrypted_text(self):
        encrypted_text = "invalidhexstring"
        pass_phrase = "securepass"
        salt = "somesalt"
        with self.assertRaises(ValueError):
            self.service.decrypt(encrypted_text, pass_phrase, salt)

    def test_decrypt_tampered_encrypted_text(self):
        plain_text = "Hello, World!"
        pass_phrase = "securepass"
        salt = "somesalt"
        encrypted_text = self.service.encrypt(plain_text, pass_phrase, salt)
        # Tamper with the encrypted text by changing one character
        tampered_text = encrypted_text[:-1] + "0" if encrypted_text[-1] != "0" else "1"
        with self.assertRaises(Exception):  # This will likely raise an InvalidTag exception
            self.service.decrypt(tampered_text, pass_phrase, salt)


if __name__ == '__main__':
    unittest.main()