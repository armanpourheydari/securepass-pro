"""
tests/test_crypto.py
Unit tests for encryption and decryption functions
"""

import unittest

from crypto_utils import decrypt_password, encrypt_password


class TestCrypto(unittest.TestCase):
    """Test encryption and decryption functionality"""

    def setUp(self):
        """Run before each test"""
        self.master_password = "test_master_123"
        self.test_password = "MySecretPassword123"

    def test_encrypt_decrypt_success(self):
        """Test that encryption and decryption work correctly"""
        # Encrypt
        encrypted = encrypt_password(self.test_password, self.master_password)

        # Check that encrypted is different from original
        self.assertNotEqual(encrypted, self.test_password)

        # Decrypt
        decrypted = decrypt_password(encrypted, self.master_password)

        # Check that decrypted matches original
        self.assertEqual(decrypted, self.test_password)

    def test_encrypt_returns_string(self):
        """Test that encrypt returns a base64 string"""
        encrypted = encrypt_password(self.test_password, self.master_password)
        self.assertIsInstance(encrypted, str)

    def test_encrypt_different_each_time(self):
        """Test that same password encrypts differently each time (nonce)"""
        enc1 = encrypt_password(self.test_password, self.master_password)
        enc2 = encrypt_password(self.test_password, self.master_password)

        # They should be different because of random nonce
        self.assertNotEqual(enc1, enc2)

        # But both should decrypt correctly
        self.assertEqual(
            decrypt_password(enc1, self.master_password), self.test_password
        )
        self.assertEqual(
            decrypt_password(enc2, self.master_password), self.test_password
        )

    def test_decrypt_wrong_password(self):
        """Test that wrong master password raises error"""
        encrypted = encrypt_password(self.test_password, self.master_password)

        # Try to decrypt with wrong password
        with self.assertRaises(ValueError):
            decrypt_password(encrypted, "wrong_password")

    def test_decrypt_corrupted_data(self):
        """Test that corrupted encrypted data raises error"""
        encrypted = encrypt_password(self.test_password, self.master_password)

        # Corrupt the data (change one character)
        corrupted = encrypted[:-1] + "A"

        with self.assertRaises(ValueError):
            decrypt_password(corrupted, self.master_password)

    def test_empty_password(self):
        """Test encryption of empty password"""
        encrypted = encrypt_password("", self.master_password)
        decrypted = decrypt_password(encrypted, self.master_password)
        self.assertEqual(decrypted, "")

    def test_special_characters(self):
        """Test encryption with special characters"""
        special = "!@#$%^&*()_+-=[]{}|;':,.<>?/~`"
        encrypted = encrypt_password(special, self.master_password)
        decrypted = decrypt_password(encrypted, self.master_password)
        self.assertEqual(decrypted, special)

    def test_long_password(self):
        """Test encryption with long password (256 characters)"""
        long_pwd = "A" * 256
        encrypted = encrypt_password(long_pwd, self.master_password)
        decrypted = decrypt_password(encrypted, self.master_password)
        self.assertEqual(decrypted, long_pwd)

    def test_multiple_passwords(self):
        """Test encrypting and decrypting multiple passwords"""
        passwords = ["pass1", "pass2", "pass3"]

        for pwd in passwords:
            encrypted = encrypt_password(pwd, self.master_password)
            decrypted = decrypt_password(encrypted, self.master_password)
            self.assertEqual(decrypted, pwd)

    def test_unicode_characters(self):
        """Test encryption with Persian/Unicode characters"""
        persian = "سلام دنیا"
        encrypted = encrypt_password(persian, self.master_password)
        decrypted = decrypt_password(encrypted, self.master_password)
        self.assertEqual(decrypted, persian)


if __name__ == "__main__":
    unittest.main()
