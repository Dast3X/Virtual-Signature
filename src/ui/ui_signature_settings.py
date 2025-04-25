from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QSlider, QCheckBox, QFrame, QToolButton
)

from src.ui.styles.signature_styles import SignatureStyles
from src.ui.utils import get_assets_path
from src.video_thread import VideoThread


class SignatureSettingsDock(QDockWidget):
    def __init__(self, parent=None):
        super().__init__("Signature Settings", parent)
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

    def apply_styles(self):
        """Apply styles from the SignatureStyles class"""
        self.setStyleSheet(SignatureStyles.DOCK_STYLE)
        self.inner_widget.setStyleSheet(SignatureStyles.WIDGET_STYLE)

    def create_components(self):
        """Create and initialize all UI components"""
        # Dev mode checkbox
        self.dev_mode_checkbox = QCheckBox("Developer Mode")
        self.dev_mode_checkbox.setChecked(self.VideoThread.dev_mode)
        self.dev_mode_checkbox.setStyleSheet(SignatureStyles.CHECKBOX_STYLE)
        self.dev_mode_checkbox.stateChanged.connect(self.on_dev_mode_changed)

        # Min distance slider
        self.min_distance_label = QLabel("Minimum Distance:")
        self.min_distance_label.setStyleSheet(SignatureStyles.LABEL_STYLE)
        self.min_distance_slider = QSlider(Qt.Horizontal)
        self.min_distance_slider.setRange(80, 97)
        self.min_distance_slider.setValue(self.VideoThread.min_distance)
        self.min_distance_slider.setStyleSheet(SignatureStyles.SLIDER_STYLE)
        self.min_distance_slider.valueChanged.connect(self.on_min_distance_changed)
        self.min_distance_value = QLabel(f"{self.VideoThread.min_distance}")
        self.min_distance_value.setAlignment(Qt.AlignCenter)
        self.min_distance_value.setStyleSheet(SignatureStyles.VALUE_LABEL_STYLE)

        # Max distance slider
        self.max_distance_label = QLabel("Maximum Distance:")
        self.max_distance_label.setStyleSheet(SignatureStyles.LABEL_STYLE)
        self.max_distance_slider = QSlider(Qt.Horizontal)
        self.max_distance_slider.setRange(95, 100)
        self.max_distance_slider.setValue(int(self.VideoThread.max_distance))
        self.max_distance_slider.setStyleSheet(SignatureStyles.SLIDER_STYLE)
        self.max_distance_slider.valueChanged.connect(self.on_max_distance_changed)
        self.max_distance_value = QLabel(f"{self.VideoThread.max_distance}")
        self.max_distance_value.setAlignment(Qt.AlignCenter)
        self.max_distance_value.setStyleSheet(SignatureStyles.VALUE_LABEL_STYLE)

        # Min signature points - converted to slider
        self.min_points_label = QLabel("Min Signature Points:")
        self.min_points_label.setStyleSheet(SignatureStyles.LABEL_STYLE)
        self.min_points_slider = QSlider(Qt.Horizontal)
        self.min_points_slider.setRange(50, 500)
        self.min_points_slider.setValue(self.VideoThread.min_signature_points)
        self.min_points_slider.setSingleStep(10)
        self.min_points_slider.setPageStep(50)
        self.min_points_slider.setStyleSheet(SignatureStyles.SLIDER_STYLE)
        self.min_points_slider.valueChanged.connect(self.on_min_points_changed)
        self.min_points_value = QLabel(f"{self.VideoThread.min_signature_points}")
        self.min_points_value.setAlignment(Qt.AlignCenter)
        self.min_points_value.setStyleSheet(SignatureStyles.VALUE_LABEL_STYLE)

        # Save duration - converted to slider
        self.save_duration_label = QLabel("Save Duration (s):")
        self.save_duration_label.setStyleSheet(SignatureStyles.LABEL_STYLE)
        self.save_duration_slider = QSlider(Qt.Horizontal)
        self.save_duration_slider.setRange(1, 10)
        self.save_duration_slider.setValue(int(self.VideoThread.thumb_up_duration))
        self.save_duration_slider.setSingleStep(1)
        self.save_duration_slider.setStyleSheet(SignatureStyles.SLIDER_STYLE)
        self.save_duration_slider.valueChanged.connect(self.on_save_duration_changed)
        self.save_duration_value = QLabel(f"{int(self.VideoThread.thumb_up_duration)}s")
        self.save_duration_value.setAlignment(Qt.AlignCenter)
        self.save_duration_value.setStyleSheet(SignatureStyles.VALUE_LABEL_STYLE)

        # Save signature button
        self.save_button = QToolButton()
        self.save_button.setIcon(QIcon(get_assets_path("save.png")))
        self.save_button.setToolTip("Save Signature")
        self.save_button.setIconSize(QSize(*SignatureStyles.BUTTON_ICON_SIZE))
        self.save_button.setMinimumSize(QSize(*SignatureStyles.BUTTON_SIZE))
        self.save_button.setStyleSheet(SignatureStyles.BUTTON_STYLE)
        self.save_button.clicked.connect(self.on_save_signature)

        # Clear signature button
        self.clear_button = QToolButton()
        self.clear_button.setIcon(QIcon(get_assets_path("eraser.png")))
        self.clear_button.setToolTip("Clear Signature")
        self.clear_button.setIconSize(QSize(*SignatureStyles.BUTTON_ICON_SIZE))
        self.clear_button.setMinimumSize(QSize(*SignatureStyles.BUTTON_SIZE))
        self.clear_button.setStyleSheet(SignatureStyles.BUTTON_STYLE)
        self.clear_button.clicked.connect(self.on_clear_signature)

        # Reset settings button
        self.reset_button = QToolButton()
        self.reset_button.setIcon(QIcon(get_assets_path("reset.png")))
        self.reset_button.setToolTip("Reset Settings")
        self.reset_button.setIconSize(QSize(*SignatureStyles.BUTTON_ICON_SIZE))
        self.reset_button.setMinimumSize(QSize(*SignatureStyles.BUTTON_SIZE))
        self.reset_button.setStyleSheet(SignatureStyles.BUTTON_STYLE)
        self.reset_button.clicked.connect(self.on_reset_settings)

        # Separators
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.separator.setStyleSheet(SignatureStyles.SEPARATOR_STYLE)
        self.separator.setMaximumHeight(1)

        self.bottom_separator = QFrame()
        self.bottom_separator.setFrameShape(QFrame.HLine)
        self.bottom_separator.setFrameShadow(QFrame.Sunken)
        self.bottom_separator.setStyleSheet(SignatureStyles.SEPARATOR_STYLE)
        self.bottom_separator.setMaximumHeight(1)

    def create_layout(self):
        """Create and set up the UI layout"""
        # Main layout
        self.main_layout = QVBoxLayout(self.inner_widget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Form layout for settings
        self.form_layout = QVBoxLayout()
        self.form_layout.setSpacing(SignatureStyles.FORM_SPACING)
        self.form_layout.setContentsMargins(*SignatureStyles.FORM_MARGINS)

        # Min distance layout - vertical arrangement
        min_distance_layout = QVBoxLayout()
        min_distance_layout.addWidget(self.min_distance_label)
        min_distance_layout.addWidget(self.min_distance_slider)
        min_distance_layout.addWidget(self.min_distance_value)

        # Max distance layout - vertical arrangement
        max_distance_layout = QVBoxLayout()
        max_distance_layout.addWidget(self.max_distance_label)
        max_distance_layout.addWidget(self.max_distance_slider)
        max_distance_layout.addWidget(self.max_distance_value)

        # Min signature points layout - vertical arrangement
        min_points_layout = QVBoxLayout()
        min_points_layout.addWidget(self.min_points_label)
        min_points_layout.addWidget(self.min_points_slider)
        min_points_layout.addWidget(self.min_points_value)

        # Save duration layout - vertical arrangement
        save_duration_layout = QVBoxLayout()
        save_duration_layout.addWidget(self.save_duration_label)
        save_duration_layout.addWidget(self.save_duration_slider)
        save_duration_layout.addWidget(self.save_duration_value)

        # Add components to form layout
        self.form_layout.addLayout(min_distance_layout)
        self.form_layout.addSpacing(10)
        self.form_layout.addLayout(max_distance_layout)
        self.form_layout.addSpacing(10)
        self.form_layout.addLayout(min_points_layout)
        self.form_layout.addSpacing(10)
        self.form_layout.addLayout(save_duration_layout)
        self.form_layout.addSpacing(10)
        self.form_layout.addWidget(self.dev_mode_checkbox)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addStretch(1)
        button_layout.setSpacing(8)
        button_layout.setContentsMargins(*SignatureStyles.BUTTON_MARGINS)

        # Add layouts to main layout
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.separator)
        self.main_layout.addLayout(button_layout)
        self.main_layout.addStretch(1)

    def on_dev_mode_changed(self, state):
        """Handle dev mode checkbox state change"""
        self.VideoThread.dev_mode = state

    def on_min_distance_changed(self, value):
        """Handle minimum distance slider value change"""
        self.VideoThread.min_distance = value
        self.min_distance_value.setText(f"{value}")

        # Make sure min is always less than max
        if value >= self.max_distance_slider.value():
            self.max_distance_slider.setValue(value + 5)

    def on_max_distance_changed(self, value):
        """Handle maximum distance slider value change"""
        self.VideoThread.max_distance = value
        self.max_distance_value.setText(f"{value}")

        # Make sure max is always greater than min
        if value <= self.min_distance_slider.value():
            self.min_distance_slider.setValue(value - 0 / 5)

    def on_min_points_changed(self, value):
        """Handle minimum signature points slider value change"""
        self.VideoThread.min_signature_points = value
        self.min_points_value.setText(f"{value}")

    def on_save_duration_changed(self, value):
        """Handle save duration slider value change"""
        self.VideoThread.thumb_up_duration = value
        self.save_duration_value.setText(f"{value}s")

    def on_save_signature(self):
        """Handle save signature button click"""
        if self.VideoThread.drawing_board is not None and self.VideoThread.is_signature_valid():
            self.VideoThread.save_signature()
            print("[INFO] Signature saved")

    def on_clear_signature(self):
        """Handle clear signature button click"""
        if self.VideoThread.drawing_board is not None:
            self.VideoThread.clear_drawing_board()

    def on_reset_settings(self):
        """Reset all settings to default values"""
        # Default values
        dev_mode_default = False
        min_distance_default = 90
        max_distance_default = 99.5
        min_points_default = 200
        save_duration_default = 3.0

        # Update UI
        self.dev_mode_checkbox.setChecked(dev_mode_default)
        self.min_distance_slider.setValue(min_distance_default)
        self.max_distance_slider.setValue(int(max_distance_default))
        self.min_points_slider.setValue(min_points_default)
        self.save_duration_slider.setValue(int(save_duration_default))

        # Update VideoThread
        self.VideoThread.dev_mode = dev_mode_default
        self.VideoThread.min_distance = min_distance_default
        self.VideoThread.max_distance = max_distance_default
        self.VideoThread.min_signature_points = min_points_default
        self.VideoThread.thumb_up_duration = save_duration_default
