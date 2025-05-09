import sys
import unittest
from unittest.mock import MagicMock, patch

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QApplication

from src.ui.main_window import MainWindow


class TestMainWindow(unittest.TestCase):
    """Test suite for the MainWindow class."""

    @classmethod
    def setUpClass(cls):
        """Set up the QApplication once for all tests."""
        cls.app = QApplication.instance() or QApplication(sys.argv)

    def setUp(self):
        """Set up each test by creating a MainWindow instance."""
        # Mock the VideoThread to avoid actual camera access
        with patch('src.ui.main_window.VideoThread') as mock_video_thread:
            mock_thread_instance = MagicMock()
            mock_video_thread.return_value = mock_thread_instance
            mock_thread_instance.isRunning.return_value = False
            mock_thread_instance.signature_points = []
            mock_thread_instance.current_finger_position = (0, 0)
            self.window = MainWindow()

    def tearDown(self):
        """Clean up after each test."""
        self.window.close()

    def test_window_title(self):
        """Test that the window title is set correctly."""
        from src.ui.styles.main_dock_styles import MainWindowStyles
        self.assertEqual(self.window.windowTitle(), MainWindowStyles.WINDOW_TITLE)

    def test_dock_widgets(self):
        """Test that dock widgets are created and added."""
        self.assertIsNotNone(self.window.camera_dock)
        self.assertIsNotNone(self.window.signature_dock)

    def test_show_about_dialog(self):
        """Test that the about dialog is shown when requested."""
        with patch('src.ui.main_window.AboutDialog') as mock_dialog:
            mock_dialog_instance = MagicMock()
            mock_dialog.return_value = mock_dialog_instance

            self.window.showAboutDialog()

            mock_dialog.assert_called_once_with(self.window)
            mock_dialog_instance.exec.assert_called_once()

    def test_update_image(self):
        """Test the updateImage method."""
        # Create a mock QImage
        test_image = QImage(100, 100, QImage.Format_RGB888)
        test_image.fill(Qt.red)

        # Call updateImage with the mock image
        self.window.updateImage(test_image)

        # Check that the camera window now has a pixmap
        self.assertIsNotNone(self.window.camera_window.pixmap())

    def test_update_image_null(self):
        """Test the updateImage method with a null image."""
        # Create a null QImage
        null_image = QImage()

        # Set VideoThread is_changing_settings to True
        self.window.VideoThread.is_changing_settings = True

        # Call updateImage with the null image
        self.window.updateImage(null_image)

        # Check that the camera window has a movie (loading animation)
        self.assertIsNotNone(self.window.camera_window.movie())

    def test_close_event(self):
        """Test that closeEvent stops the video thread."""
        # Mock the isRunning and stop methods
        self.window.VideoThread.isRunning = MagicMock(return_value=True)
        self.window.VideoThread.stop = MagicMock()

        # Create a mock close event
        mock_event = MagicMock()

        # Call closeEvent
        self.window.closeEvent(mock_event)

        # Verify that stop was called and event was accepted
        self.window.VideoThread.stop.assert_called_once()
        mock_event.accept.assert_called_once()

    def test_update_status_bar(self):
        """Test that updateStatusBar updates the status bar."""
        # Set up test data
        self.window.VideoThread.signature_points = [(10, 10), (20, 20), (30, 30)]
        self.window.VideoThread.current_finger_position = (50, 60)

        # Mock the statusbar's update_status method
        self.window.statusbar.update_status = MagicMock()

        # Call updateStatusBar
        self.window.updateStatusBar()

        # Verify update_status was called with correct parameters
        self.window.statusbar.update_status.assert_called_once_with(3, 50, 60)


if __name__ == '__main__':
    unittest.main()
