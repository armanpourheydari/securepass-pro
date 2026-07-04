# tests/test_logic.py
import unittest

from logic import check_password, generate_password


class TestLogic(unittest.TestCase):
    def test_generate_length(self):
        self.assertEqual(len(generate_password(16)), 16)

    def test_check_score(self):
        self.assertGreaterEqual(check_password("Hello@World123")["score"], 0)


if __name__ == "__main__":
    unittest.main()
