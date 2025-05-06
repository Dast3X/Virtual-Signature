from PySide6.QtCore import QTimer, QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QMediaDevices
from PySide6.QtWidgets import (
    QComboBox, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QToolButton,
    QDockWidget, QFormLayout, QFrame
)

from src.ui.styles.camera_dock_styles import CameraStyles
from src.utils.utils import get_assets_path
from src.video_thread import VideoThread


class CameraSettingsDock(QDockWidget):
    def __init__(self, parent=None):
        super().__init__("Camera Settings", parent)
        self.VideoThread = VideoThread().get_instance()
        self.inner_widget = QWidget()
        self.setWidget(self.inner_widget)

        self.apply_styles()
        self.setFeatures(
            QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.setMaximumWidth(250)
        self.setMinimumWidth(200)

        # Initialize UI components
        self.create_components()
        self.create_layout()

        # Timer to update available cameras
        self.cameraUpdateTimer = QTimer(self)
        self.cameraUpdateTimer.timeout.connect(self.getAvailableCameras)
        self.cameraUpdateTimer.start(5000)

        # Timer to update FPS counter
        self.fpsUpdateTimer = QTimer(self)
        self.fpsUpdateTimer.timeout.connect(self.updateFpsCounter)
        self.fpsUpdateTimer.start(500)  # Update every 500ms

        # Initial camera detection
        self.getAvailableCameras()

    def apply_styles(self):
        """Apply styles from the CameraStyles class"""
        self.setStyleSheet(CameraStyles.DOCK_STYLE)
        self.inner_widget.setStyleSheet(CameraStyles.WIDGET_STYLE)

    def create_components(self):
        """Create and initialize all UI components"""

        # FPS combobox
        self.fps_combobox = QComboBox()
        self.fps_combobox.addItems(["30", "60"])
        self.fps_combobox.setCurrentText("30")
        self.fps_combobox.currentIndexChanged.connect(self.onFPSChanged)
        self.fps_combobox.setStyleSheet(CameraStyles.COMBOBOX_STYLE)
        self.fps_combobox.setFixedHeight(CameraStyles.COMBOBOX_HEIGHT)

        # Resolution combobox
        self.resolution_combobox = QComboBox()
        self.resolution_combobox.addItems(["640x480", "1280x720", "1920x1080"])
        self.resolution_combobox.currentIndexChanged.connect(self.onResolutionChanged)
        self.resolution_combobox.setStyleSheet(CameraStyles.COMBOBOX_STYLE)
        self.resolution_combobox.setFixedHeight(CameraStyles.COMBOBOX_HEIGHT)

        # Camera selection combobox
        self.camera_combobox = QComboBox()
        self.camera_combobox.currentIndexChanged.connect(self.onCameraChanged)
        self.camera_combobox.setStyleSheet(CameraStyles.COMBOBOX_STYLE)
        self.camera_combobox.setFixedHeight(CameraStyles.COMBOBOX_HEIGHT)

        # Toggle button
        self.toggle_btn = QToolButton()
        self.toggle_btn.setIcon(QIcon(get_assets_path("start.png")))
        self.toggle_btn.setToolTip("Start Capture")
        self.toggle_btn.setIconSize(QSize(*CameraStyles.TOGGLE_ICON_SIZE))
        self.toggle_btn.setMinimumSize(QSize(*CameraStyles.TOGGLE_BUTTON_SIZE))
        self.toggle_btn.setStyleSheet(CameraStyles.TOGGLE_BUTTON_STYLE)
        self.toggle_btn.clicked.connect(self.onToggleCapture)

        self.advanced_settings_btn = QToolButton()
        self.advanced_settings_btn.setIcon(QIcon(get_assets_path("setting.png")))
        self.advanced_settings_btn.setToolTip("Advanced Settings")
        self.advanced_settings_btn.setEnabled(False)
        self.advanced_settings_btn.setIconSize(QSize(*CameraStyles.TOGGLE_ICON_SIZE))
        self.advanced_settings_btn.setMinimumSize(QSize(*CameraStyles.TOGGLE_BUTTON_SIZE))
        self.advanced_settings_btn.setStyleSheet(CameraStyles.TOGGLE_BUTTON_STYLE)
        self.advanced_settings_btn.clicked.connect(self.onClickAdvancedSettings)

        # Labels
        self.fps_label = QLabel("FPS:")
        self.resolution_label = QLabel("Resolution:")
        self.camera_label = QLabel("Camera:")

        for label in [self.fps_label, self.resolution_label, self.camera_label]:
            label.setStyleSheet(CameraStyles.LABEL_STYLE)

        # FPS Counter
        self.fps_counter = QLabel("0 FPS")
        self.fps_counter.setAlignment(Qt.AlignCenter)
        self.fps_counter.setStyleSheet(CameraStyles.FPS_COUNTER_STYLE)

        # Separators
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.separator.setStyleSheet(CameraStyles.SEPARATOR_STYLE)
        self.separator.setMaximumHeight(1)

        self.bottom_separator = QFrame()
        self.bottom_separator.setFrameShape(QFrame.HLine)
        self.bottom_separator.setFrameShadow(QFrame.Sunken)
        self.bottom_separator.setStyleSheet(CameraStyles.SEPARATOR_STYLE)
        self.bottom_separator.setMaximumHeight(1)

    def onClickAdvancedSettings(self):
        """Handle advanced settings button click"""
        if self.VideoThread.isRunning():
            self.VideoThread.run_camera_setting()
        else:
            print("[ERROR] Camera is not running, cannot open advanced settings")

    def create_layout(self):
        """Create and set up the UI layout"""
        # Form layout for settings
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(CameraStyles.FORM_SPACING)
        self.form_layout.setContentsMargins(*CameraStyles.FORM_MARGINS)

        # Add form rows
        self.form_layout.addRow(self.fps_label, self.fps_combobox)
        self.form_layout.addRow(self.resolution_label, self.resolution_combobox)
        self.form_layout.addRow(self.camera_label, self.camera_combobox)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.advanced_settings_btn)
        button_layout.addWidget(self.toggle_btn)
        button_layout.addStretch(1)
        button_layout.setSpacing(4)
        button_layout.setContentsMargins(*CameraStyles.BUTTON_MARGINS)

        # FPS counter layout
        fps_counter_layout = QVBoxLayout()
        fps_counter_layout.addWidget(self.fps_counter)
        fps_counter_layout.setContentsMargins(*CameraStyles.FPS_COUNTER_MARGINS)

        # Main layout
        self.main_layout = QVBoxLayout(self.inner_widget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.separator)
        self.main_layout.addLayout(button_layout)
        self.main_layout.addStretch(0)
        self.main_layout.addWidget(self.bottom_separator)
        self.main_layout.addLayout(fps_counter_layout)

    def updateFpsCounter(self):
        """Update the FPS counter display with the current FPS value"""
        if self.VideoThread.isRunning():
            if self.VideoThread.prev_frame_time > 0:
                fps = self.VideoThread.fps
                self.fps_counter.setText(f"{fps:.0f} FPS")
                if fps >= 25:
                    self.fps_counter.setStyleSheet(CameraStyles.FPS_COUNTER_STYLE_GOOD)
                elif fps >= 15:
                    self.fps_counter.setStyleSheet(CameraStyles.FPS_COUNTER_STYLE_MEDIUM)
                else:
                    self.fps_counter.setStyleSheet(CameraStyles.FPS_COUNTER_STYLE_LOW)
            else:
                self.fps_counter.setText("0 FPS")
                self.fps_counter.setStyleSheet(CameraStyles.FPS_COUNTER_STYLE)
        else:
            self.fps_counter.setText("0 FPS")
            self.fps_counter.setStyleSheet(CameraStyles.FPS_COUNTER_STYLE)

    def onToggleCapture(self):
        """Handle camera capture toggle"""
        if self.VideoThread.isRunning():
            self.toggle_btn.setIcon(QIcon(get_assets_path('start.png')))
            self.toggle_btn.setToolTip("Start Capture")
            self.advanced_settings_btn.setEnabled(False)
            self.VideoThread.stop()
            self.fps_counter.setText("0 FPS")
            self.fps_counter.setStyleSheet(CameraStyles.FPS_COUNTER_STYLE)
        else:
            self.toggle_btn.setIcon(QIcon(get_assets_path('stop.png')))
            self.toggle_btn.setToolTip("Stop Capture")
            self.advanced_settings_btn.setEnabled(True)
            self.VideoThread.start_th()

    def onFPSChanged(self):
        """Handle FPS selection change"""
        fps = int(self.fps_combobox.currentText())
        print(f"[INFO] Selected FPS: {fps}")
        self.VideoThread.change_settings(fps_cap=fps)

    def getAvailableCameras(self):
        """Detect available camera devices"""
        available_cam = QMediaDevices.videoInputs()
        self.updateCameras(available_cam)

    def onResolutionChanged(self):
        """Handle resolution selection change"""
        resolution = self.resolution_combobox.currentText()
        width, height = map(int, resolution.split('x'))
        print(f"[INFO] Selected resolution: {width}x{height}")
        self.VideoThread.change_settings(resolution=(width, height))

    def onCameraChanged(self, index):
        """Handle camera selection change"""
        if index == -1:
            print("[ERROR] No camera selected")
            return
        print(f"[INFO] Selected camera index: {index}")
        self.VideoThread.change_settings(camera_index=index)

    def updateCameras(self, available_cam):
        """Update camera selection combobox with available cameras"""
        if not available_cam:
            self.camera_combobox.clear()
            self.camera_combobox.setEnabled(False)
        else:
            self.camera_combobox.setEnabled(True)
            camera_descriptions = [cam.description() for cam in available_cam]
            current_items = [self.camera_combobox.itemText(i) for i in range(self.camera_combobox.count())]
            if sorted(camera_descriptions) != sorted(current_items):
                self.camera_combobox.clear()
                self.camera_combobox.addItems(camera_descriptions)
