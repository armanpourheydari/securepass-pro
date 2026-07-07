"""
tests/test_vault.py
Unit tests for check vault security
"""

import os
import unittest

from vault_manager import (
    create_vault,
    delete_card_from_vault,
    get_all_cards,
    save_card_to_vault,
    update_card_in_vault,
)


class TestCardVault(unittest.TestCase):

    def setUp(self):
        """Run before each test - create a test vault"""
        self.master_password = "test_master_123"
        create_vault(self.master_password)

    def tearDown(self):
        """Run after each test - clean up test files"""
        for file in ["passwords.vault", "vault.verify"]:
            if os.path.exists(file):
                os.remove(file)

    def test_save_and_get_card(self):
        """Test saving and retrieving a card"""
        result = save_card_to_vault(
            "Test Card",
            "1234567890123456",
            "John Doe",
            "12",
            "26",
            "123",
            "visa",
            self.master_password,
        )
        self.assertTrue(result)

        cards = get_all_cards(self.master_password)
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0]["name"], "Test Card")
        self.assertEqual(cards[0]["number"], "1234567890123456")

    def test_update_card(self):
        """Test updating a card"""
        save_card_to_vault(
            "Test Card",
            "1234567890123456",
            "John Doe",
            "12",
            "26",
            "123",
            "visa",
            self.master_password,
        )

        result = update_card_in_vault(
            1,
            "Updated Card",
            "9876543210987654",
            "Jane Doe",
            "01",
            "28",
            "456",
            "mastercard",
            self.master_password,
        )
        self.assertTrue(result)

        cards = get_all_cards(self.master_password)
        self.assertEqual(cards[0]["name"], "Updated Card")
        self.assertEqual(cards[0]["number"], "9876543210987654")

    def test_delete_card(self):
        """Test deleting a card"""
        save_card_to_vault(
            "Test Card",
            "1234567890123456",
            "John Doe",
            "12",
            "26",
            "123",
            "visa",
            self.master_password,
        )

        result = delete_card_from_vault(1, self.master_password)
        self.assertTrue(result)

        cards = get_all_cards(self.master_password)
        self.assertEqual(len(cards), 0)

    def test_wrong_password(self):
        """Test that wrong master password fails"""
        save_card_to_vault(
            "Test Card",
            "1234567890123456",
            "John Doe",
            "12",
            "26",
            "123",
            "visa",
            self.master_password,
        )

        # Try with wrong password
        cards = get_all_cards("wrong_password")
        self.assertEqual(len(cards), 0)


class TestNoteVault(unittest.TestCase):

    def setUp(self):
        self.master_password = "test_master_123"
        create_vault(self.master_password)

    def tearDown(self):
        for file in ["passwords.vault", "vault.verify"]:
            if os.path.exists(file):
                os.remove(file)

    def test_save_and_get_note(self):
        """Test saving and retrieving a note"""
        from vault_manager import get_all_notes, save_note_to_vault

        result = save_note_to_vault(
            "Test Note", "This is a secure note content.", self.master_password
        )
        self.assertTrue(result)

        notes = get_all_notes(self.master_password)
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["title"], "Test Note")
        self.assertEqual(notes[0]["content"], "This is a secure note content.")

    def test_update_note(self):
        """Test updating a note"""
        from vault_manager import (
            get_all_notes,
            save_note_to_vault,
            update_note_in_vault,
        )

        save_note_to_vault("Test Note", "Old content", self.master_password)

        result = update_note_in_vault(
            1, "Updated Note", "New content", self.master_password
        )
        self.assertTrue(result)

        notes = get_all_notes(self.master_password)
        self.assertEqual(notes[0]["title"], "Updated Note")
        self.assertEqual(notes[0]["content"], "New content")

    def test_delete_note(self):
        """Test deleting a note"""
        from vault_manager import (
            delete_note_from_vault,
            get_all_notes,
            save_note_to_vault,
        )

        save_note_to_vault("Test Note", "Content", self.master_password)

        result = delete_note_from_vault(1, self.master_password)
        self.assertTrue(result)

        notes = get_all_notes(self.master_password)
        self.assertEqual(len(notes), 0)
