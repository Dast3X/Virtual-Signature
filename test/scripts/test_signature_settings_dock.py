import sys
import unittest
from unittest.mock import MagicMock, patch

from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication

from src.ui.dock.signature_settings_dock import SignatureSettingsDock


class TestSignatureSettingsDock(unittest.TestCase):
    """Test suite for the SignatureSettingsDock class."""

    @classmethod
    def setUpClass(cls):
        """Set up the QApplication once for all tests."""
        cls.app = QApplication.instance() or QApplication(sys.argv)

    def setUp(self):
        """Set up each test by creating a SignatureSettingsDock instance."""
        # Mock VideoThread
        self.video_thread_patcher = patch('src.ui.dock.signature_settings_dock.VideoThread')
        self.mock_video_thread_class = self.video_thread_patcher.start()
        self.mock_video_thread = MagicMock()
        self.mock_video_thread_class.return_value = self.mock_video_thread
        self.mock_video_thread.get_instance.return_value = self.mock_video_thread

        # Set default values for mock VideoThread
        self.mock_video_thread.dev_mode = False
        self.mock_video_thread.min_distance = 90
        self.mock_video_thread.max_distance = 99.5
        self.mock_video_thread.min_signature_points = 200
        self.mock_video_thread.thumb_up_duration = 3.0
        self.mock_video_thread.drawing_board = None

        # Create dock widget
        self.dock = SignatureSettingsDock()

    def tearDown(self):
        """Clean up after each test."""
        self.video_thread_patcher.stop()
        self.dock.close()

    def test_initial_state(self):
        """Test the initial state of the dock widget."""
        self.assertEqual(self.dock.windowTitle(), "Signature Settings")
        self.assertFalse(self.dock.dev_mode_checkbox.isChecked())
        self.assertEqual(self.dock.min_distance_slider.value(), 90)
        self.assertEqual(self.dock.max_distance_slider.value(), 99)
        self.assertEqual(self.dock.min_points_slider.value(), 200)
        self.assertEqual(self.dock.save_duration_slider.value(), 3)

    def test_dev_mode_changed(self):
        """Test changing the developer mode."""
        # Check initial state
        self.assertFalse(self.mock_video_thread.dev_mode)

        # Show the checkbox before clicking it

        # Change the checkbox state to checked
        self.dock.dev_mode_checkbox.setChecked(True)

        # Check that the VideoThread property was updated
        self.assertTrue(self.mock_video_thread.dev_mode)

        # Change the checkbox state to unchecked
        self.dock.dev_mode_checkbox.setChecked(False)

        # Check that the VideoThread property was updated
        self.assertFalse(self.mock_video_thread.dev_mode)

    def test_min_distance_changed(self):
        """Test changing the minimum distance."""
        # Check initial state
        self.assertEqual(self.mock_video_thread.min_distance, 90)

        # Change the slider value using QTest
        self.dock.min_distance_slider.setValue(85)
        QTest.mouseRelease(self.dock.min_distance_slider, Qt.LeftButton)

        # Check that the VideoThread property was updated
        self.assertEqual(self.mock_video_thread.min_distance, 85)

        # Check that the label was updated
        self.assertEqual(self.dock.min_distance_value.text(), "85")

        # Test auto-adjusting max distance if min is higher
        self.dock.max_distance_slider.setValue(84)
        self.dock.min_distance_slider.setValue(90)
        QTest.mouseRelease(self.dock.min_distance_slider, Qt.LeftButton)

        # Max should be automatically adjusted
        self.assertGreater(self.dock.max_distance_slider.value(), 90)

    def test_max_distance_changed(self):
        """Test changing the maximum distance."""
        # Check initial state
        self.assertEqual(self.mock_video_thread.max_distance, 99.5)

        # Change the slider value using QTest
        self.dock.max_distance_slider.setValue(98)
        QTest.mouseRelease(self.dock.max_distance_slider, Qt.LeftButton)

        # Check that the VideoThread property was updated
        self.assertEqual(self.mock_video_thread.max_distance, 98)

        # Check that the label was updated
        self.assertEqual(self.dock.max_distance_value.text(), "98")

    def test_min_points_changed(self):
        """Test changing the minimum signature points."""
        # Check initial state
        self.assertEqual(self.mock_video_thread.min_signature_points, 200)

        # Change the slider value using QTest
        self.dock.min_points_slider.setValue(250)
        QTest.mouseRelease(self.dock.min_points_slider, Qt.LeftButton)

        # Check that the VideoThread property was updated
        self.assertEqual(self.mock_video_thread.min_signature_points, 250)

        # Check that the label was updated
        self.assertEqual(self.dock.min_points_value.text(), "250")

    def test_save_duration_changed(self):
        """Test changing the save duration."""
        # Check initial state
        self.assertEqual(self.mock_video_thread.thumb_up_duration, 3.0)

        # Change the slider value using QTest
        self.dock.save_duration_slider.setValue(5)
        QTest.mouseRelease(self.dock.save_duration_slider, Qt.LeftButton)

        # Check that the VideoThread property was updated
        self.assertEqual(self.mock_video_thread.thumb_up_duration, 5)

        # Check that the label was updated
        self.assertEqual(self.dock.save_duration_value.text(), "5s")

    def test_save_signature(self):
        """Test saving a signature."""
        # Set up the mock VideoThread to have a valid drawing board
        self.mock_video_thread.drawing_board = MagicMock()
        self.mock_video_thread.is_signature_valid.return_value = True
        self.mock_video_thread.save_signature = MagicMock()

        # Call the save_signature method directly
        self.dock.on_save_signature()

        # Check that save_signature was called
        self.mock_video_thread.save_signature.assert_called_once()

        # Test with invalid signature
        self.mock_video_thread.save_signature.reset_mock()
        self.mock_video_thread.is_signature_valid.return_value = False

        # Call the save_signature method again
        self.dock.on_save_signature()

        # Check that save_signature was not called
        self.mock_video_thread.save_signature.assert_not_called()

    def test_clear_signature(self):
        """Test clearing a signature."""
        # Set up the mock VideoThread to have a valid drawing board
        self.mock_video_thread.drawing_board = MagicMock()
        self.mock_video_thread.clear_drawing_board = MagicMock()

        # Call the clear_signature method directly
        self.dock.on_clear_signature()

        # Check that clear_drawing_board was called
        self.mock_video_thread.clear_drawing_board.assert_called_once()

        # Test without drawing board
        self.mock_video_thread.clear_drawing_board.reset_mock()
        self.mock_video_thread.drawing_board = None

        # Call the clear_signature method again
        self.dock.on_clear_signature()

        # Check that clear_drawing_board was not called
        self.mock_video_thread.clear_drawing_board.assert_not_called()

    def test_reset_settings(self):
        """Test resetting all settings to default values."""
        # Change all settings from default
        self.mock_video_thread.dev_mode = True
        self.mock_video_thread.min_distance = 85
        self.mock_video_thread.max_distance = 97
        self.mock_video_thread.min_signature_points = 300
        self.mock_video_thread.thumb_up_duration = 5.0

        # Update UI elements to reflect changed settings
        self.dock.dev_mode_checkbox.setChecked(True)
        self.dock.min_distance_slider.setValue(85)
        self.dock.max_distance_slider.setValue(97)
        self.dock.min_points_slider.setValue(300)
        self.dock.save_duration_slider.setValue(5)

        # Call the reset_settings method directly
        self.dock.on_reset_settings()

        # Check that all settings were reset to default values
        self.assertFalse(self.mock_video_thread.dev_mode)
        self.assertEqual(self.mock_video_thread.min_distance, 90)
        self.assertEqual(self.mock_video_thread.max_distance, 99.5)
        self.assertEqual(self.mock_video_thread.min_signature_points, 200)
        self.assertEqual(self.mock_video_thread.thumb_up_duration, 3.0)

        # Check that UI elements were updated
        self.assertFalse(self.dock.dev_mode_checkbox.isChecked())
        self.assertEqual(self.dock.min_distance_slider.value(), 90)
        self.assertEqual(self.dock.max_distance_slider.value(), 99)
        self.assertEqual(self.dock.min_points_slider.value(), 200)
        self.assertEqual(self.dock.save_duration_slider.value(), 3)

    def test_component_creation(self):
        """Test that all UI components are created correctly."""
        # Check if all essential components exist
        self.assertIsNotNone(self.dock.dev_mode_checkbox)
        self.assertIsNotNone(self.dock.min_distance_label)
        self.assertIsNotNone(self.dock.min_distance_slider)
        self.assertIsNotNone(self.dock.min_distance_value)
        self.assertIsNotNone(self.dock.max_distance_label)
        self.assertIsNotNone(self.dock.max_distance_slider)
        self.assertIsNotNone(self.dock.max_distance_value)
        self.assertIsNotNone(self.dock.min_points_label)
        self.assertIsNotNone(self.dock.min_points_slider)
        self.assertIsNotNone(self.dock.min_points_value)
        self.assertIsNotNone(self.dock.save_duration_label)
        self.assertIsNotNone(self.dock.save_duration_slider)
        self.assertIsNotNone(self.dock.save_duration_value)
        self.assertIsNotNone(self.dock.save_button)
        self.assertIsNotNone(self.dock.clear_button)
        self.assertIsNotNone(self.dock.reset_button)

    def test_slider_ranges(self):
        """Test that all sliders have correct ranges."""
        # Check min/max values for all sliders
        self.assertEqual(self.dock.min_distance_slider.minimum(), 80)
        self.assertEqual(self.dock.min_distance_slider.maximum(), 97)
        self.assertEqual(self.dock.max_distance_slider.minimum(), 95)
        self.assertEqual(self.dock.max_distance_slider.maximum(), 100)
        self.assertEqual(self.dock.min_points_slider.minimum(), 50)
        self.assertEqual(self.dock.min_points_slider.maximum(), 500)
        self.assertEqual(self.dock.save_duration_slider.minimum(), 1)
        self.assertEqual(self.dock.save_duration_slider.maximum(), 10)


if __name__ == '__main__':
    unittest.main()
