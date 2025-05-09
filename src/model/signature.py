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
        """Get absolute path to resource with fallbacks"""
        possible_paths = []

        # PyInstaller path
        if hasattr(sys, '_MEIPASS'):
            possible_paths.append(os.path.join(sys._MEIPASS, relative_path))

        # Development paths - try multiple options
        script_dir = os.path.dirname(__file__)
        possible_paths.extend([
            os.path.abspath(os.path.join(script_dir, '..', '..', relative_path)),
            os.path.abspath(os.path.join(script_dir, '..', relative_path)),
            os.path.abspath(os.path.join(os.getcwd(), relative_path))
        ])

        # Try each path
        for path in possible_paths:
            print(f"Checking path: {path}")
            if os.path.exists(path):
                print(f"Found model at: {path}")
                return path

        # If we get here, we couldn't find the file
        print(f"ERROR: Could not find {relative_path} in any of the expected locations")
        return possible_paths[0]  # Return the first path anyway as a fallback

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

    def is_pointing_up(self):
        """
        Check if only index finger is up (pointing up gesture).
        Returns 'pointing_up' if the condition is met, None otherwise.
        """
        result = self.get_result()

        if not result or not result.gestures or not result.hand_landmarks or not result.gestures[0][
                                                                                     0].category_name == "None":
            return None

        if len(result.hand_landmarks) == 1:

            landmarks = result.hand_landmarks[0]

            index_tip = landmarks[8]
            index_base = landmarks[5]

            if index_tip.y < index_base.y:
                middle_tip = landmarks[12]  # Middle finger tip
                middle_base = landmarks[9]  # Middle finger base

                ring_tip = landmarks[16]  # Ring finger tip
                ring_base = landmarks[13]  # Ring finger base

                pinky_tip = landmarks[20]  # Pinky tip
                pinky_base = landmarks[17]  # Pinky base

                # Check if other fingers are bent (not extended)
                if (middle_tip.y > middle_base.y and
                        ring_tip.y > ring_base.y and
                        pinky_tip.y > pinky_base.y):
                    return True
        return False

    def recognizer_context_manager(self):
        """Return the recognizer as context manager for use in with statement"""
        return self.setup_recognizer()
