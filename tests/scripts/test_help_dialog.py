import os
import sys
import unittest
# Mock the get_assets_path function
import unittest.mock as mock

from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QTabWidget, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout

# Apply the mock
from src.ui.help.help_dialog import HelpDialog


def mock_get_assets_path(path):
    return os.path.join("assets", path)


class TestHelpDialog(unittest.TestCase):
    """Test case for the HelpDialog class."""

    @classmethod
    def setUpClass(cls):
        """Set up the application once for all tests."""
        if not QApplication.instance():
            cls.app = QApplication(sys.argv)
        else:
            cls.app = QApplication.instance()

    def setUp(self):
        """Set up a new dialog for each tests."""
        self.dialog = HelpDialog()

    def tearDown(self):
        """Clean up after each tests."""
        self.dialog.close()
        self.dialog = None

    def test_dialog_initialization(self):
        """Test that the dialog initializes correctly."""
        self.assertEqual(self.dialog.windowTitle(), "User Guide")
        self.assertEqual(self.dialog.size().width(), 800)
        self.assertEqual(self.dialog.size().height(), 600)
        self.assertFalse(self.dialog.windowFlags() & Qt.WindowContextHelpButtonHint)

    def test_tab_widget_structure(self):
        """Test that the tab widget has the correct structure."""
        tab_widget = self.dialog.findChild(QTabWidget)
        self.assertIsNotNone(tab_widget)

        # Check that we have exactly 6 tabs
        self.assertEqual(tab_widget.count(), 6)

        # Check that all tabs have the expected titles
        expected_tab_titles = [
            "Overview",
            "Camera Settings",
            "Signature Settings",
            "Usage Guide",
            "Gesture Guide",
            "Troubleshooting"
        ]

        for i, title in enumerate(expected_tab_titles):
            self.assertEqual(tab_widget.tabText(i), title)

    def test_close_button(self):
        """Test that the close button works."""
        close_button = self.dialog.findChild(QPushButton, "")
        self.assertIsNotNone(close_button)
        self.assertEqual(close_button.text(), "Close")

        # Using a spy to check if the dialog will be closed
        with mock.patch.object(self.dialog, 'accept') as mock_accept:
            QTest.mouseClick(close_button, Qt.LeftButton)
            mock_accept.assert_called_once()

    def test_overview_tab_content(self):
        """Test that the overview tab contains expected content."""
        tab_widget = self.dialog.findChild(QTabWidget)
        overview_widget = tab_widget.widget(0)

        # Find the QTextEdit within the scrollable area
        text_edit = overview_widget.findChild(QTextEdit)
        self.assertIsNotNone(text_edit)

        # Check for some key phrases that should be in the overview
        overview_content = text_edit.toHtml()
        self.assertIn("Application Overview", overview_content)
        self.assertIn("Main Features", overview_content)
        self.assertIn("Application Interface", overview_content)

    def test_camera_settings_tab_content(self):
        """Test that the camera settings tab contains expected content."""
        tab_widget = self.dialog.findChild(QTabWidget)
        camera_settings_widget = tab_widget.widget(1)

        text_edit = camera_settings_widget.findChild(QTextEdit)
        self.assertIsNotNone(text_edit)

        content = text_edit.toHtml()
        self.assertIn("Camera Settings", content)
        self.assertIn("Camera Selection", content)
        self.assertIn("Resolution", content)
        self.assertIn("FPS", content)

    def test_signature_settings_tab_content(self):
        """Test that the signature settings tab contains expected content."""
        tab_widget = self.dialog.findChild(QTabWidget)
        signature_settings_widget = tab_widget.widget(2)

        text_edit = signature_settings_widget.findChild(QTextEdit)
        self.assertIsNotNone(text_edit)

        content = text_edit.toHtml()
        self.assertIn("Signature Settings", content)
        self.assertIn("Minimum Distance", content)
        self.assertIn("Maximum Distance", content)
        self.assertIn("Minimum Points", content)

    def test_usage_guide_tab_content(self):
        """Test that the usage guide tab contains expected content."""
        tab_widget = self.dialog.findChild(QTabWidget)
        usage_guide_widget = tab_widget.widget(3)

        text_edit = usage_guide_widget.findChild(QTextEdit)
        self.assertIsNotNone(text_edit)

        content = text_edit.toHtml()
        self.assertIn("Usage Guide", content)
        self.assertIn("Getting Started", content)
        self.assertIn("Creating a Signature", content)
        self.assertIn("Gesture Controls", content)

    def test_gesture_guide_tab_content(self):
        """Test that the gesture guide tab contains expected content."""
        tab_widget = self.dialog.findChild(QTabWidget)
        gesture_guide_widget = tab_widget.widget(4)

        text_edit = gesture_guide_widget.findChild(QTextEdit)
        self.assertIsNotNone(text_edit)

        content = text_edit.toHtml()
        self.assertIn("Gesture Controls Guide", content)
        self.assertIn("Point Up", content)
        self.assertIn("Thumbs Down", content)
        self.assertIn("Thumbs Up", content)

    def test_troubleshooting_tab_content(self):
        """Test that the troubleshooting tab contains expected content."""
        tab_widget = self.dialog.findChild(QTabWidget)
        troubleshooting_widget = tab_widget.widget(5)

        text_edit = troubleshooting_widget.findChild(QTextEdit)
        self.assertIsNotNone(text_edit)

        content = text_edit.toHtml()
        self.assertIn("Troubleshooting Guide", content)
        self.assertIn("Camera Not Working", content)
        self.assertIn("Gesture Recognition Issues", content)
        self.assertIn("Drawing Issues", content)
        self.assertIn("Saving Issues", content)

    def test_layout_structure(self):
        """Test that the layout structure is correct."""
        main_layout = self.dialog.layout()
        self.assertIsInstance(main_layout, QVBoxLayout)

        # Check that we have a tab widget and a button layout
        self.assertEqual(main_layout.count(), 2)

        # First item should be the tab widget
        tab_widget_item = main_layout.itemAt(0)
        self.assertIsNotNone(tab_widget_item)
        self.assertIsInstance(tab_widget_item.widget(), QTabWidget)

        # Second item should be a layout containing the close button
        button_layout_item = main_layout.itemAt(1)
        self.assertIsNotNone(button_layout_item)
        self.assertIsInstance(button_layout_item.layout(), QHBoxLayout)


if __name__ == '__main__':
    unittest.main()
