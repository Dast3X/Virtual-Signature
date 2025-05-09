import sys
import unittest
from unittest.mock import MagicMock, patch

from PySide6.QtWidgets import QApplication

from src.ui.dock.camera_setting_dock import CameraSettingsDock


class TestCameraSettingsDock(unittest.TestCase):
    """Test suite for the CameraSettingsDock class."""

    @classmethod
    def setUpClass(cls):
        """Set up the QApplication once for all tests."""
        cls.app = QApplication.instance() or QApplication(sys.argv)

    def setUp(self):
        """Set up each test by creating a CameraSettingsDock instance."""
        # Mock VideoThread
        self.video_thread_patcher = patch('src.ui.dock.camera_setting_dock.VideoThread')
        self.mock_video_thread_class = self.video_thread_patcher.start()
        self.mock_video_thread = MagicMock()
        self.mock_video_thread_class.return_value = self.mock_video_thread
        self.mock_video_thread.get_instance.return_value = self.mock_video_thread
        self.mock_video_thread.isRunning.return_value = False
        self.mock_video_thread.fps = 30.0

        # Mock QMediaDevices
        self.media_devices_patcher = patch('src.ui.dock.camera_setting_dock.QMediaDevices')
        self.mock_media_devices = self.media_devices_patcher.start()

        # Create dock widget
        self.dock = CameraSettingsDock()

        # Stop the timers to prevent unexpected behavior
        self.dock.cameraUpdateTimer.stop()
        self.dock.fpsUpdateTimer.stop()

    def tearDown(self):
        """Clean up after each test."""
        self.video_thread_patcher.stop()
        self.media_devices_patcher.stop()
        self.dock.close()

    def test_initial_state(self):
        """Test the initial state of the dock widget."""
        self.assertEqual(self.dock.windowTitle(), "Camera Settings")
        self.assertEqual(self.dock.fps_combobox.currentText(), "30")
        self.assertEqual(self.dock.resolution_combobox.currentText(), "640x480")
        self.assertEqual(self.dock.fps_counter.text(), "0 FPS")
        self.assertFalse(self.dock.advanced_settings_btn.isEnabled())

    def test_toggle_capture(self):
        """Test toggling the camera capture."""
        # Test starting the capture
        self.mock_video_thread.isRunning.return_value = False
        self.dock.onToggleCapture()

        # Check that the video thread was started
        self.mock_video_thread.start_th.assert_called_once()
        self.assertTrue(self.dock.advanced_settings_btn.isEnabled())

        # Test stopping the capture
        self.mock_video_thread.isRunning.return_value = True
        self.dock.onToggleCapture()

        # Check that the video thread was stopped
        self.mock_video_thread.stop.assert_called_once()
        self.assertFalse(self.dock.advanced_settings_btn.isEnabled())
        self.assertEqual(self.dock.fps_counter.text(), "0 FPS")

    def test_fps_changed(self):
        """Test changing the FPS setting."""
        # Select a different FPS
        self.dock.fps_combobox.setCurrentText("60")

        # Check that change_settings was called with the correct FPS
        self.mock_video_thread.change_settings.assert_called_with(fps_cap=60)

    def test_resolution_changed(self):
        """Test changing the resolution setting."""
        # Select a different resolution
        self.dock.resolution_combobox.setCurrentText("1280x720")

        # Check that change_settings was called with the correct resolution
        self.mock_video_thread.change_settings.assert_called_with(resolution=(1280, 720))

    def test_camera_changed(self):
        """Test changing the camera."""
        # Add a camera to the combobox
        self.dock.camera_combobox.addItem("Test Camera")

        # Select the camera
        self.dock.camera_combobox.setCurrentIndex(0)

        # Check that change_settings was called with the correct camera index
        self.mock_video_thread.change_settings.assert_called_with(camera_index=0)

    def test_update_fps_counter(self):
        """Test updating the FPS counter."""
        # Set up the video thread to be running
        self.mock_video_thread.isRunning.return_value = True
        self.mock_video_thread.prev_frame_time = 1.0

        # Test good FPS (>= 25)
        self.mock_video_thread.fps = 30.0
        self.dock.updateFpsCounter()
        self.assertEqual(self.dock.fps_counter.text(), "30 FPS")

        # Test medium FPS (>= 15 and < 25)
        self.mock_video_thread.fps = 20.0
        self.dock.updateFpsCounter()
        self.assertEqual(self.dock.fps_counter.text(), "20 FPS")

        # Test low FPS (< 15)
        self.mock_video_thread.fps = 10.0
        self.dock.updateFpsCounter()
        self.assertEqual(self.dock.fps_counter.text(), "10 FPS")

        # Test video thread not running
        self.mock_video_thread.isRunning.return_value = False
        self.dock.updateFpsCounter()
        self.assertEqual(self.dock.fps_counter.text(), "0 FPS")

    def test_advanced_settings(self):
        """Test advanced settings button."""
        # Test when video thread is running
        self.mock_video_thread.isRunning.return_value = True
        self.dock.onClickAdvancedSettings()
        self.mock_video_thread.run_camera_setting.assert_called_once()

        # Test when video thread is not running
        self.mock_video_thread.reset_mock()
        self.mock_video_thread.isRunning.return_value = False
        self.dock.onClickAdvancedSettings()
        self.mock_video_thread.run_camera_setting.assert_not_called()

    def test_update_cameras(self):
        """Test updating the camera list."""
        # Create mock camera devices
        mock_camera1 = MagicMock()
        mock_camera1.description.return_value = "Camera 1"
        mock_camera2 = MagicMock()
        mock_camera2.description.return_value = "Camera 2"

        # Test with cameras available
        self.dock.updateCameras([mock_camera1, mock_camera2])
        self.assertTrue(self.dock.camera_combobox.isEnabled())
        self.assertEqual(self.dock.camera_combobox.count(), 2)
        self.assertEqual(self.dock.camera_combobox.itemText(0), "Camera 1")
        self.assertEqual(self.dock.camera_combobox.itemText(1), "Camera 2")

        # Test with no cameras available
        self.dock.updateCameras([])
        self.assertFalse(self.dock.camera_combobox.isEnabled())
        self.assertEqual(self.dock.camera_combobox.count(), 0)

    def test_get_available_cameras(self):
        """Test getting available cameras."""
        # Create mock camera devices
        mock_camera = MagicMock()
        self.mock_media_devices.videoInputs = MagicMock(return_value=[mock_camera])

        # Patch the updateCameras method
        self.dock.updateCameras = MagicMock()

        # Call getAvailableCameras
        self.dock.getAvailableCameras()

        # Check that videoInputs was called
        self.mock_media_devices.videoInputs.assert_called_once()

        # Check that updateCameras was called with the result of videoInputs
        self.dock.updateCameras.assert_called_once_with([mock_camera])


if __name__ == '__main__':
    unittest.main()
