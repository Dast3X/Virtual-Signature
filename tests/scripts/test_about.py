import unittest
from unittest.mock import patch, MagicMock

from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QLabel, QDialogButtonBox

from src.ui.about.about_dialog import AboutDialog


class TestAboutDialog(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create QApplication instance once for all tests
        cls.app = QApplication.instance() or QApplication([])

    @patch('src.utils.utils.get_assets_path')
    @patch('PySide6.QtGui.QPixmap')
    def setUp(self, mock_pixmap, mock_get_assets_path):
        # Mock the get_assets_path and QPixmap for testing without real assets
        mock_get_assets_path.return_value = "mock/path/to/logo.png"
        pix = MagicMock()
        pix.scaled.return_value = pix
        mock_pixmap.return_value = pix

        # Create AboutDialog instance
        self.dialog = AboutDialog()

    def test_initialization(self):
        """Test if the AboutDialog initializes with correct properties"""
        QTest.qWaitForWindowExposed(self.dialog)

        self.assertEqual(self.dialog.windowTitle(), "About")
        self.assertEqual(self.dialog.size().width(), 320)
        self.assertEqual(self.dialog.size().height(), 280)
        self.assertTrue(self.dialog.windowFlags() & Qt.WindowStaysOnTopHint)

    def test_dialog_content(self):
        """Test if the AboutDialog contains expected labels and buttons"""
        QTest.qWaitForWindowExposed(self.dialog)

        # Find all QLabel widgets recursively
        labels: list[QLabel] = self.dialog.findChildren(QLabel)
        all_text = " ".join(lbl.text() for lbl in labels)

        # Assert that key text elements are present
        self.assertIn("DeepSignus", all_text, "Title label not found")
        self.assertIn("Version 1.0.0", all_text, "Version information not found")
        self.assertIn("Grammatikopulo", all_text, "Copyright information not found")

        # Check if OK button exists
        ok_box = self.dialog.findChild(QDialogButtonBox)
        self.assertIsNotNone(ok_box, "QDialogButtonBox not found")
        self.assertIsNotNone(
            ok_box.button(QDialogButtonBox.StandardButton.Ok),
            "OK button not found"
        )

    def test_ok_button_closes_dialog(self):
        """Test if clicking the OK button triggers dialog.accept()"""
        self.dialog.show()
        QTest.qWaitForWindowExposed(self.dialog)

        ok_button = self.dialog.findChild(QDialogButtonBox).button(
            QDialogButtonBox.StandardButton.Ok
        )
        self.assertIsNotNone(ok_button, "OK button not found")

        with patch.object(self.dialog, "accept") as mock_accept:
            QTest.mouseClick(ok_button, Qt.LeftButton)
            QTest.qWait(50)
            mock_accept.assert_called_once()


if __name__ == "__main__":
    unittest.main()
