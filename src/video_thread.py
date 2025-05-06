import os
import time
from datetime import datetime

import cv2
import numpy as np
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QImage

from src.model.signature import SignatureRecognition


class VideoThread(QThread):
    """
    VideoThread class for handling video capture and gesture recognition.
    This class is a singleton and is responsible for initializing the camera,
    processing frames, and handling gestures.
    """
    ImageUpdate = Signal(QImage)
    _instance = None

    # Color constants
    BLUE = (255, 0, 0)
    GREEN = (0, 255, 0)
    RED = (0, 0, 255)
    WHITE = (255, 255, 255)
    YELLOW = (0, 255, 255)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(VideoThread, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.fps = 0
        if not hasattr(self, 'initialized'):
            super().__init__()
            self.resolution = (640, 480)
            self.is_changing_settings = False
            self.fps_cap = 30
            self.camera_index = 0
            self.ThreadActive = False
            self.cap = None
            self.initialized = True

            # FPS calculation variables
            self.prev_frame_time = 0
            self.curr_frame_time = 0
            self.dev_mode = False

            # Drawing-related variables
            self.drawing_board = None
            self.window_height = None
            self.window_width = None
            self.previous_x, self.previous_y = None, None
            self.signature_points = []
            self.min_signature_points = 200
            self.is_drawing_active = False

            # Variables for tracking Thumb_Up gesture
            self.thumb_up_start_time = None
            self.thumb_up_duration = 3.0
            self.save_cooldown = 0

            # Variables for saved message display time
            self.saved_message_time = None
            self.saved_message_duration = 2.0
            self.signature_too_small = False

            # Distance validation variables
            self.min_distance = 90  # Closer than this is too close (negative z is closer)
            self.max_distance = 99.5  # Further than this is too far (positive z is further)
            self.distance_warning = None
            self.distance_warning_time = None
            self.distance_warning_duration = 2.0

    def get_instance(self):
        return self._instance

    def change_settings(self, camera_index: int = None, fps_cap: int = None, resolution: tuple[int, int] = None):
        # Store the current running state before stopping
        was_running = self.ThreadActive
        self.stop()
        self.is_changing_settings = True

        if camera_index is not None:
            self.camera_index = camera_index
        if fps_cap is not None:
            self.fps_cap = fps_cap
        if resolution is not None:
            self.resolution = resolution

        # Only restart if it was running before
        if was_running:
            self.start_th()

        self.is_changing_settings = False

    def run_camera_setting(self):
        self.cap.set(cv2.CAP_PROP_SETTINGS, 1)

    def camera_init(self):
        """Initialize the camera with the specified settings"""
        try:
            print(f"[INFO] Initializing camera {self.camera_index}")
            self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)

            if not self.cap.isOpened():
                print(
                    f"[ERROR] Failed to open camera {self.camera_index} with cv2.CAP_DSHOW, trying without specific API")
                self.cap = cv2.VideoCapture(self.camera_index)  # Try without specifying API

            if not self.cap.isOpened():
                print(f"[ERROR] Camera {self.camera_index} still not opening, trying index 0")
                self.cap = cv2.VideoCapture(0)  # Fall back to default camera

            if self.cap.isOpened():
                print("[INFO] Camera opened successfully")
                self.cap.set(cv2.CAP_PROP_FPS, self.fps_cap)
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
                self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

                # Initialize drawing board
                self.window_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                self.window_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                self.drawing_board = np.zeros((int(self.window_height), int(self.window_width), 3), dtype=np.uint8)
                print(f"[INFO] Drawing board initialized with size {self.window_width}x{self.window_height}")
            else:
                print("[ERROR] Failed to open any camera")
        except Exception as e:
            print(f"[ERROR] Exception in camera_init: {str(e)}")

    def is_signature_valid(self):
        """Check if signature has enough points to be valid"""
        return len(self.signature_points) >= self.min_signature_points

    def clear_drawing_board(self):
        """Clear the drawing board"""
        if self.drawing_board is not None:
            self.drawing_board = np.zeros((int(self.window_height), int(self.window_width), 3), dtype=np.uint8)
            self.previous_x, self.previous_y = None, None
            self.signature_points = []

    def save_signature(self):
        """Save the signature to a file"""
        if not os.path.exists("../signatures"):
            os.makedirs("../signatures")

        gray = cv2.cvtColor(self.drawing_board, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

        transparent_signature = np.zeros((int(self.window_height), int(self.window_width), 4), dtype=np.uint8)
        transparent_signature[:, :, 0:3] = self.drawing_board
        transparent_signature[:, :, 3] = mask

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"../signatures/signature_{timestamp}.png"

        cv2.imwrite(filename, transparent_signature)

        print(f"Signature saved to {filename}")
        self.saved_message_time = time.time()
        self.clear_drawing_board()
        return filename

    def check_distance(self, hand_landmarks):
        """Check if the hand is at an appropriate distance from the camera"""
        if hand_landmarks:
            # Get z-coordinate of index finger tip (landmark 8)
            index_finger_z = (1 - np.abs(hand_landmarks[0][8].z)) * 100
            if index_finger_z < self.min_distance:
                self.distance_warning = "Too close to camera! Please move back."
                self.distance_warning_time = time.time()
                return False
            elif index_finger_z > self.max_distance:
                self.distance_warning = "Too far from camera! Please move closer."
                self.distance_warning_time = time.time()
                return False
            else:
                return True
        return False  # If no landmarks, assume distance is not valid

    def show_wireframe(self, frame, gesture_result):
        """Draw hand landmarks and gesture information on the frame"""
        if gesture_result:
            if gesture_result.hand_landmarks and self.dev_mode:
                for hand_landmarks in gesture_result.hand_landmarks:
                    # Get hand landmark context from SignatureRecognition
                    hand_connections = self.sign_model.hand_connections

                    for point in hand_landmarks:
                        # Draw landmarks as circles
                        x, y = int(point.x * frame.shape[1]), int(point.y * frame.shape[0])
                        cv2.circle(frame, (x, y), 5, self.RED, -1)

                    # Draw connections between landmarks
                    for connection in hand_connections:
                        start_idx, end_idx = connection
                        x1, y1 = int(hand_landmarks[start_idx].x * frame.shape[1]), int(
                            hand_landmarks[start_idx].y * frame.shape[0])
                        x2, y2 = int(hand_landmarks[end_idx].x * frame.shape[1]), int(
                            hand_landmarks[end_idx].y * frame.shape[0])
                        cv2.line(frame, (x1, y1), (x2, y2), self.WHITE, 2)

                # Check distance if hand landmarks are detected
                self.check_distance(gesture_result.hand_landmarks)

            # Draw gesture information if gestures are detected
            if gesture_result.gestures:
                gesture_name = gesture_result.gestures[0][0].category_name

                # Display saving progress bar when Thumb_Up is detected
                if gesture_name == "Thumb_Up" and self.thumb_up_start_time is not None:
                    elapsed_time = time.time() - self.thumb_up_start_time
                    if elapsed_time < self.thumb_up_duration:
                        # Check if signature has enough points
                        if self.is_signature_valid():
                            progress = int((elapsed_time / self.thumb_up_duration) * 100)

                            # Calculate positions for centered progress bar
                            progress_bar_width = 300
                            progress_bar_height = 20
                            start_x = int((self.window_width - progress_bar_width) / 2)
                            end_x = start_x + progress_bar_width
                            bottom_y = int(self.window_height - 50)  # 50 pixels from bottom

                            # Draw the progress bar background
                            cv2.rectangle(frame, (start_x, bottom_y), (end_x, bottom_y + progress_bar_height),
                                          self.WHITE, 2)

                            # Draw the filled progress
                            progress_width = int((progress / 100) * progress_bar_width)
                            cv2.rectangle(frame, (start_x, bottom_y),
                                          (start_x + progress_width, bottom_y + progress_bar_height),
                                          self.YELLOW, -1)

                            # Display saving percentage text
                            text = f"Saving {progress}%"
                            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                            text_x = int((self.window_width - text_size[0]) / 2)
                            text_y = bottom_y - 10
                            cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.WHITE, 2)
                        else:
                            # Display not enough points message
                            text = f"Not enough points! Need {self.min_signature_points - len(self.signature_points)} more"
                            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
                            text_x = int((self.window_width - text_size[0]) / 2)
                            text_y = int(self.window_height - 80)
                            cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, self.YELLOW, 2)

        # Display signature progress bar at the bottom center when drawing is active
        if self.is_drawing_active or (gesture_result and gesture_result.gestures and
                                      gesture_result.gestures[0][0].category_name == "Pointing_Up"):
            progress = min(100, int((len(self.signature_points) / self.min_signature_points) * 100))
            progress_bar_width = 300
            progress_bar_height = 20

            # Calculate positions for centered progress bar
            start_x = int((self.window_width - progress_bar_width) / 2)
            end_x = start_x + progress_bar_width
            bottom_y = int(self.window_height - 50)  # 50 pixels from bottom

            # Draw the progress bar background
            cv2.rectangle(frame, (start_x, bottom_y), (end_x, bottom_y + progress_bar_height), self.WHITE, 2)

            # Draw the filled progress
            progress_width = int((progress / 100) * progress_bar_width)
            cv2.rectangle(frame, (start_x, bottom_y), (start_x + progress_width, bottom_y + progress_bar_height),
                          self.GREEN if progress >= 100 else self.BLUE, -1)

            # Display percentage text
            text = f"{progress}% / {self.min_signature_points} points"
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            text_x = int((self.window_width - text_size[0]) / 2)
            text_y = bottom_y - 10
            cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.WHITE, 2)

        # Display "Signature Saved!" message for 2 seconds after saving
        if self.saved_message_time is not None:
            elapsed_time = time.time() - self.saved_message_time
            if elapsed_time < self.saved_message_duration:
                # Calculate positions for centered message
                text = "Signature Saved!"
                text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
                text_x = int((self.window_width - text_size[0]) / 2)
                text_y = int(self.window_height / 2)

                cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, self.GREEN, 2)
            else:
                self.saved_message_time = None

        # Display distance warning if active
        if self.distance_warning_time is not None:
            elapsed_time = time.time() - self.distance_warning_time
            if elapsed_time < self.distance_warning_duration and self.distance_warning:
                # Calculate positions for centered message
                text_size = cv2.getTextSize(self.distance_warning, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
                text_x = int((self.window_width - text_size[0]) / 2)
                text_y = int(self.window_height / 4)  # Position in the upper part of the screen

                # Draw background rectangle
                padding = 10
                cv2.rectangle(frame,
                              (text_x - padding, text_y - text_size[1] - padding),
                              (text_x + text_size[0] + padding, text_y + padding),
                              (0, 0, 0), -1)

                # Draw text
                cv2.putText(frame, self.distance_warning, (text_x, text_y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, self.YELLOW, 2)
            else:
                self.distance_warning_time = None
                self.distance_warning = None

        return frame

    def handle_gestures(self, frame, gesture_result):
        """Handle different gestures and their drawing functions"""
        self.is_drawing_active = False

        if gesture_result and gesture_result.gestures:
            gesture_name = gesture_result.gestures[0][0].category_name

            # Check if the hand is at a valid distance before processing gestures
            is_distance_valid = self.check_distance(gesture_result.hand_landmarks)

            if gesture_name == "Pointing_Up" and is_distance_valid:
                self.is_drawing_active = True
                self.thumb_up_start_time = None

                index_finger = gesture_result.hand_landmarks[0][8]
                x, y = int(index_finger.x * frame.shape[1]), int(index_finger.y * frame.shape[0])

                if self.previous_x is not None and self.previous_y is not None:
                    cv2.line(self.drawing_board, (self.previous_x, self.previous_y), (x, y), self.GREEN, 5)
                    # Add points for signature size validation
                    self.signature_points.append((x, y))

                # Draw the current finger position
                cv2.circle(frame, (x, y), 5, self.BLUE, -1)

                # Update previous coordinates
                self.previous_x, self.previous_y = x, y

            elif gesture_name == "Thumb_Up" and is_distance_valid:
                self.previous_x, self.previous_y = None, None

                if self.thumb_up_start_time is None and self.save_cooldown <= 0:
                    self.thumb_up_start_time = time.time()
                elif self.thumb_up_start_time is not None:
                    elapsed_time = time.time() - self.thumb_up_start_time
                    if (elapsed_time >= self.thumb_up_duration and not self.saved_message_time
                            and self.is_signature_valid()):
                        filename = self.save_signature()
                        self.thumb_up_start_time = None
                        self.save_cooldown = 30

            elif gesture_name == "Thumb_Down":
                self.clear_drawing_board()
                self.thumb_up_start_time = None

            else:
                # Stop drawing for other gestures
                self.previous_x, self.previous_y = None, None
                self.thumb_up_start_time = None
        else:
            # Reset timer if no gestures are detected
            self.thumb_up_start_time = None

        return frame

    # Show FPS on the frame
    def show_fps(self, frame):
        self.curr_frame_time = cv2.getTickCount() / cv2.getTickFrequency()
        self.fps = 1 / (self.curr_frame_time - self.prev_frame_time) if self.prev_frame_time > 0 else 0
        self.prev_frame_time = self.curr_frame_time
        cv2.putText(frame, f"FPS: {self.fps:.0f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 2, cv2.LINE_AA)
        return frame

    def run(self):
        # Initialize the camera
        self.camera_init()

        # Signature Recognition
        self.sign_model = SignatureRecognition()

        # Initialize time for FPS calculation
        if self.dev_mode:
            self.prev_frame_time = 0

        # Initialize timestamp for MediaPipe
        self.timestamp_ms = 0

        # Initialize frame counter for frame skipping
        frame_counter = 0

        # Store the latest gesture result to use between processed frames
        last_gesture_result = None

        # Calculate frame skip based on fps_cap
        # If fps_cap is 30, skip_frames will be 0 (process all frames)
        # If fps_cap is 60, skip_frames will be 1 (process every other frame)
        skip_frames = max(0, int(self.fps_cap / 30) - 1)

        with self.sign_model.recognizer_context_manager() as recognizer:
            while self.ThreadActive:
                ret, frame = self.cap.read()

                if ret:
                    # Flip frame for better user experience
                    frame = cv2.flip(frame, 1)

                    # Process frame with MediaPipe only if not skipping this frame
                    process_this_frame = (frame_counter % (skip_frames + 1) == 0)

                    if process_this_frame:
                        # Process frame with MediaPipe
                        mp_image = self.sign_model.convert_frame_to_mediapipe_image(frame)
                        recognizer.recognize_async(mp_image, self.timestamp_ms)
                        self.timestamp_ms += 1

                        # Get gesture recognition results and update the last result
                        last_gesture_result = self.sign_model.get_result()

                    # This ensures wireframe isn't flickering between processed frames
                    gesture_result = last_gesture_result

                    # Handle gesture recognition and drawing for every frame
                    if gesture_result:
                        frame = self.show_wireframe(frame, gesture_result)
                        frame = self.handle_gestures(frame, gesture_result)

                    # Show FPS if dev mode is enabled
                    if self.dev_mode:
                        frame = self.show_fps(frame)

                    # Combine drawing board with camera frame
                    frame = cv2.addWeighted(frame, 1, self.drawing_board, 1, 0)

                    # Decrease cooldown counter
                    if self.save_cooldown > 0:
                        self.save_cooldown -= 1

                    # Convert to QImage and emit signal
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    qt_image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
                    pic = qt_image.scaled(640, 480, Qt.KeepAspectRatio)
                    self.ImageUpdate.emit(pic)

                    # Increment frame counter
                    frame_counter += 1

                    if frame_counter > 1000000:
                        frame_counter = 0

        self.cap.release()
        self.ImageUpdate.emit(QImage())

    def start_th(self):
        self.ThreadActive = True
        self.start()

    def stop(self):
        self.ThreadActive = False
        self.quit()
        self.wait()
