import unittest
from unittest.mock import patch, MagicMock, Mock
import os
import sys
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python.vision import GestureRecognizerResult

# Import the class to tests
from src.model.signature import SignatureRecognition


class TestSignatureRecognition(unittest.TestCase):
    """Test cases for the SignatureRecognition class."""

    def setUp(self):
        """Set up tests fixtures before each tests method."""
        self.signature_recognition = SignatureRecognition()

    def test_init(self):
        """Test initialization of SignatureRecognition class."""
        self.assertIsNone(self.signature_recognition.gesture_result)
        self.assertEqual(self.signature_recognition.hand_connections, mp.solutions.hands.HAND_CONNECTIONS)

    @patch('os.path.exists')
    def test_get_resource_path_exists(self, mock_exists):
        """Test get_resource_path when file exists."""
        mock_exists.return_value = True

        path = self.signature_recognition.get_resource_path('models/gesture_recognizer.task')

        # Check that the method returns a path that ends with the relative path
        # Use os.path.normpath to handle different path separators on different OSes
        expected_path = os.path.normpath('models/gesture_recognizer.task')
        self.assertTrue(path.endswith(expected_path), f"Path {path} does not end with {expected_path}")

    @patch('os.path.exists')
    def test_get_resource_path_not_exists(self, mock_exists):
        """Test get_resource_path when file doesn't exist."""
        mock_exists.return_value = False

        with patch('sys.stdout'):  # Suppress print statements
            path = self.signature_recognition.get_resource_path('models/gesture_recognizer.task')

        # Even when file doesn't exist, should return a path
        self.assertIsNotNone(path)

    def test_set_gesture_result(self):
        """Test setting gesture recognition result."""
        mock_result = MagicMock(spec=GestureRecognizerResult)
        mock_image = MagicMock(spec=mp.Image)
        timestamp = 123

        self.signature_recognition.set_gesture_result(mock_result, mock_image, timestamp)

        self.assertEqual(self.signature_recognition.gesture_result, mock_result)

    @patch('mediapipe.tasks.python.vision.GestureRecognizer.create_from_options')
    def test_setup_recognizer(self, mock_create):
        """Test setup of gesture recognizer."""
        mock_recognizer = MagicMock()
        mock_create.return_value = mock_recognizer

        result = self.signature_recognition.setup_recognizer()

        self.assertEqual(result, mock_recognizer)
        mock_create.assert_called_once()

    def test_convert_frame_to_mediapipe_image(self):
        """Test conversion of OpenCV frame to MediaPipe image."""
        # Create a mock frame (3x3 BGR image)
        frame = np.zeros((3, 3, 3), dtype=np.uint8)

        result = self.signature_recognition.convert_frame_to_mediapipe_image(frame)

        self.assertIsInstance(result, mp.Image)
        self.assertEqual(result.image_format, mp.ImageFormat.SRGB)

    def test_get_result(self):
        """Test getting gesture recognition result."""
        mock_result = MagicMock(spec=GestureRecognizerResult)
        self.signature_recognition.gesture_result = mock_result

        result = self.signature_recognition.get_result()

        self.assertEqual(result, mock_result)

    def test_is_pointing_up_no_result(self):
        """Test is_pointing_up when no result is available."""
        self.signature_recognition.gesture_result = None

        result = self.signature_recognition.is_pointing_up()

        self.assertIsNone(result)

    def test_is_pointing_up_no_gestures(self):
        """Test is_pointing_up when no gestures are detected."""
        mock_result = MagicMock(spec=GestureRecognizerResult)
        mock_result.gestures = []
        self.signature_recognition.gesture_result = mock_result

        result = self.signature_recognition.is_pointing_up()

        self.assertIsNone(result)

    def test_is_pointing_up_true(self):
        """Test is_pointing_up when index finger is up and others are down."""
        # Create a mock result with hand landmarks
        mock_result = MagicMock(spec=GestureRecognizerResult)

        # Create a gesture with category_name "None"
        mock_gesture = MagicMock()
        mock_gesture.category_name = "None"
        mock_result.gestures = [[mock_gesture]]

        # Create mock landmarks
        class MockLandmark:
            def __init__(self, x, y, z):
                self.x = x
                self.y = y
                self.z = z

        landmarks = [None] * 21  # MediaPipe has 21 hand landmarks

        # Set up index finger extended
        landmarks[5] = MockLandmark(0.5, 0.5, 0)  # index base
        landmarks[8] = MockLandmark(0.5, 0.2, 0)  # index tip (y < base.y means extended)

        # Set up other fingers closed
        landmarks[9] = MockLandmark(0.6, 0.5, 0)  # middle base
        landmarks[12] = MockLandmark(0.6, 0.7, 0)  # middle tip (y > base.y means bent)

        landmarks[13] = MockLandmark(0.7, 0.5, 0)  # ring base
        landmarks[16] = MockLandmark(0.7, 0.7, 0)  # ring tip

        landmarks[17] = MockLandmark(0.8, 0.5, 0)  # pinky base
        landmarks[20] = MockLandmark(0.8, 0.7, 0)  # pinky tip

        mock_result.hand_landmarks = [landmarks]

        self.signature_recognition.gesture_result = mock_result

        result = self.signature_recognition.is_pointing_up()

        self.assertTrue(result)

    def test_is_pointing_up_false_all_extended(self):
        """Test is_pointing_up when all fingers are extended."""
        # Create a mock result with hand landmarks
        mock_result = MagicMock(spec=GestureRecognizerResult)

        # Create a gesture with category_name "None"
        mock_gesture = MagicMock()
        mock_gesture.category_name = "None"
        mock_result.gestures = [[mock_gesture]]

        # Create mock landmarks
        class MockLandmark:
            def __init__(self, x, y, z):
                self.x = x
                self.y = y
                self.z = z

        landmarks = [None] * 21

        # Set up all fingers extended (tips above bases)
        landmarks[5] = MockLandmark(0.5, 0.5, 0)  # index base
        landmarks[8] = MockLandmark(0.5, 0.2, 0)  # index tip

        landmarks[9] = MockLandmark(0.6, 0.5, 0)  # middle base
        landmarks[12] = MockLandmark(0.6, 0.2, 0)  # middle tip (y < base.y means extended)

        landmarks[13] = MockLandmark(0.7, 0.5, 0)  # ring base
        landmarks[16] = MockLandmark(0.7, 0.2, 0)  # ring tip

        landmarks[17] = MockLandmark(0.8, 0.5, 0)  # pinky base
        landmarks[20] = MockLandmark(0.8, 0.2, 0)  # pinky tip

        mock_result.hand_landmarks = [landmarks]

        self.signature_recognition.gesture_result = mock_result

        result = self.signature_recognition.is_pointing_up()

        self.assertFalse(result)

    @patch('mediapipe.tasks.python.vision.GestureRecognizer.create_from_options')
    def test_recognizer_context_manager(self, mock_create):
        """Test recognizer_context_manager method."""
        mock_recognizer = MagicMock()
        mock_create.return_value = mock_recognizer

        result = self.signature_recognition.recognizer_context_manager()

        self.assertEqual(result, mock_recognizer)
        mock_create.assert_called_once()


if __name__ == '__main__':
    unittest.main()