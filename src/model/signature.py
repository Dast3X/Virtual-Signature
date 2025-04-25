import cv2
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.components.processors import ClassifierOptions
from mediapipe.tasks.python.vision import GestureRecognizerResult, GestureRecognizerOptions, GestureRecognizer, \
    RunningMode as VisionRunningMode
import os
import sys


class SignatureRecognition:
    """
    Class responsible for hand gesture recognition using MediaPipe.
    This class only handles the gesture recognition functionality.
    """

    def __init__(self):
        """Initialize the SignatureRecognition class."""
        self.model_path = self.get_resource_path('models/gesture_recognizer.task')
        self.gesture_result = None
        self.hand_connections = mp.solutions.hands.HAND_CONNECTIONS

    def get_resource_path(self, relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller"""
        if hasattr(sys, '_MEIPASS'):  # Running as bundled exe
            base_path = sys._MEIPASS
        else:  # Running in normal Python environment
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

        return os.path.join(base_path, relative_path)

    def set_gesture_result(self, result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
        """Callback function for the gesture recognizer"""
        self.gesture_result = result

    def setup_recognizer(self):
        """Setup the gesture recognizer with options"""
        options = GestureRecognizerOptions(
            base_options=BaseOptions(model_asset_path=self.model_path),
            running_mode=VisionRunningMode.LIVE_STREAM,
            result_callback=self.set_gesture_result,
            num_hands=1,
            min_hand_detection_confidence=0.1,
            canned_gesture_classifier_options=ClassifierOptions(
                category_allowlist=["Pointing_Up", "Thumb_Up", "Thumb_Down", "None"]
            )
        )

        return GestureRecognizer.create_from_options(options)

    @staticmethod
    def convert_frame_to_mediapipe_image(frame):
        """Convert OpenCV frame to MediaPipe image format"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        return mp_image

    def get_result(self):
        """Return the current gesture recognition result"""
        return self.gesture_result

    def recognizer_context_manager(self):
        """Return the recognizer as context manager for use in with statement"""
        return self.setup_recognizer()
