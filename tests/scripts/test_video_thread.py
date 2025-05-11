import sys
import unittest
from unittest.mock import MagicMock, patch

import numpy as np
from PySide6.QtWidgets import QApplication

from src.video_thread import VideoThread


class TestVideoThread(unittest.TestCase):
    """Test suite for the VideoThread class."""

    @classmethod
    def setUpClass(cls):
        """Set up the QApplication once for all tests."""
        cls.app = QApplication.instance() or QApplication(sys.argv)

    def setUp(self):
        """Set up each tests by creating a VideoThread instance."""
        # Since VideoThread is a singleton, we need to reset it
        VideoThread._instance = None

        # Mock cv2.VideoCapture to avoid actual camera access
        self.patcher = patch('src.video_thread.cv2.VideoCapture')
        self.mock_capture = self.patcher.start()

        # Configure mock capture
        mock_cap_instance = MagicMock()
        self.mock_capture.return_value = mock_cap_instance
        mock_cap_instance.isOpened.return_value = True
        mock_cap_instance.get.return_value = 640  # Width and height

        # Create VideoThread instance
        self.video_thread = VideoThread()

        # Mock SignatureRecognition
        self.sign_model_patcher = patch('src.video_thread.SignatureRecognition')
        self.mock_sign_model = self.sign_model_patcher.start()

    def tearDown(self):
        """Clean up after each tests."""
        self.patcher.stop()
        self.sign_model_patcher.stop()

        # Stop the thread if it's running
        if self.video_thread.isRunning():
            self.video_thread.stop()

    def test_singleton(self):
        """Test that VideoThread is a singleton."""
        video_thread_2 = VideoThread()
        self.assertIs(self.video_thread, video_thread_2)

    def test_change_settings(self):
        """Test changing settings in the VideoThread."""
        # Initial values
        original_camera_index = self.video_thread.camera_index
        original_fps_cap = self.video_thread.fps_cap
        original_resolution = self.video_thread.resolution

        # Change settings
        new_camera_index = original_camera_index + 1
        new_fps_cap = original_fps_cap + 10
        new_resolution = (1280, 720)

        self.video_thread.change_settings(
            camera_index=new_camera_index,
            fps_cap=new_fps_cap,
            resolution=new_resolution
        )

        # Check that settings were changed
        self.assertEqual(self.video_thread.camera_index, new_camera_index)
        self.assertEqual(self.video_thread.fps_cap, new_fps_cap)
        self.assertEqual(self.video_thread.resolution, new_resolution)

    def test_camera_init(self):
        """Test camera initialization."""
        # Call camera_init
        self.video_thread.camera_init()

        # Check that VideoCapture was called with correct parameters
        self.mock_capture.assert_called()

        # Check that drawing board was initialized
        self.assertIsNotNone(self.video_thread.drawing_board)
        self.assertEqual(self.video_thread.drawing_board.shape, (640, 640, 3))

    def test_clear_drawing_board(self):
        """Test clearing the drawing board."""
        # Initialize drawing board
        self.video_thread.window_width = 640
        self.video_thread.window_height = 480
        self.video_thread.drawing_board = np.ones((480, 640, 3), dtype=np.uint8)
        self.video_thread.previous_x = 100
        self.video_thread.previous_y = 100
        self.video_thread.signature_points = [(10, 10), (20, 20)]

        # Set up a mock for StatusUpdate.emit
        self.video_thread.StatusUpdate = MagicMock()

        # Clear drawing board
        self.video_thread.clear_drawing_board()

        # Check that drawing board was cleared
        self.assertTrue(np.all(self.video_thread.drawing_board == 0))
        self.assertIsNone(self.video_thread.previous_x)
        self.assertIsNone(self.video_thread.previous_y)
        self.assertEqual(self.video_thread.signature_points, [])
        self.assertEqual(self.video_thread.current_finger_position, (0, 0))

        # Check that StatusUpdate was emitted
        self.video_thread.StatusUpdate.emit.assert_called_once()

    def test_is_signature_valid(self):
        """Test signature validation."""
        # Set minimum signature points
        self.video_thread.min_signature_points = 5

        # Test with not enough points
        self.video_thread.signature_points = [(10, 10), (20, 20)]
        self.assertFalse(self.video_thread.is_signature_valid())

        # Test with enough points
        self.video_thread.signature_points = [(i * 10, i * 10) for i in range(10)]
        self.assertTrue(self.video_thread.is_signature_valid())

    @patch('src.video_thread.os.path.exists')
    @patch('src.video_thread.os.makedirs')
    @patch('src.video_thread.cv2.cvtColor')
    @patch('src.video_thread.cv2.threshold')
    @patch('src.video_thread.cv2.imwrite')
    @patch('src.video_thread.datetime')
    def test_save_signature(self, mock_datetime, mock_imwrite, mock_threshold,
                            mock_cvtColor, mock_makedirs, mock_exists):
        """Test saving the signature."""
        # Set up mocks
        mock_exists.return_value = False
        mock_cvtColor.return_value = np.zeros((480, 640), dtype=np.uint8)
        mock_threshold.return_value = (None, np.ones((480, 640), dtype=np.uint8))
        mock_datetime.now.return_value.strftime.return_value = "20250509_121212"

        # Initialize drawing board
        self.video_thread.window_width = 640
        self.video_thread.window_height = 480
        self.video_thread.drawing_board = np.ones((480, 640, 3), dtype=np.uint8)

        # Mock clear_drawing_board to avoid issues
        self.video_thread.clear_drawing_board = MagicMock()

        # Save signature
        filename = self.video_thread.save_signature()

        # Check that directory was created if it didn't exist
        mock_makedirs.assert_called_once_with("../signatures")

        # Check that image was saved
        mock_imwrite.assert_called_once()
        self.assertEqual(filename, "../signatures/signature_20250509_121212.png")

        # Check that drawing board was cleared
        self.video_thread.clear_drawing_board.assert_called_once()

    def test_check_distance(self):
        """Test distance checking."""
        # Set distance limits
        self.video_thread.min_distance = 90
        self.video_thread.max_distance = 95

        # Mock a hand landmark
        class MockLandmark:
            def __init__(self, z):
                self.z = z

        # Test with no landmarks
        self.assertFalse(self.video_thread.check_distance(None))

        # Test with empty landmarks
        self.assertFalse(self.video_thread.check_distance([]))

        # Test with hand too close (z coordinate makes index_finger_z < min_distance)
        hand_landmarks = [[MockLandmark(1) for _ in range(21)]]
        self.assertFalse(self.video_thread.check_distance(hand_landmarks))
        self.assertIsNotNone(self.video_thread.distance_warning)
        self.assertIn("Too close to camera! Please move back.", self.video_thread.distance_warning)

        # Test with hand too far (z coordinate makes index_finger_z > max_distance)
        hand_landmarks = [[MockLandmark(0) for _ in range(21)]]
        self.assertFalse(self.video_thread.check_distance(hand_landmarks))
        self.assertIsNotNone(self.video_thread.distance_warning)
        self.assertIn("Too far from camera! Please move closer.", self.video_thread.distance_warning)

        # Test with hand at correct distance
        hand_landmarks = [[MockLandmark(0.07) for _ in range(21)]]
        self.assertTrue(self.video_thread.check_distance(hand_landmarks))

    @patch('src.video_thread.time.time')
    def test_thread_active_state(self, mock_time):
        """Test starting and stopping the thread."""
        mock_time.return_value = 123.45

        # Start the thread
        self.video_thread.start_th()
        self.assertTrue(self.video_thread.ThreadActive)

        # Stop the thread
        self.video_thread.stop()
        self.assertFalse(self.video_thread.ThreadActive)


if __name__ == '__main__':
    unittest.main()
