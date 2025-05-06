from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from src.ui.styles.about_styles import AboutDialogStyles
from src.ui.utils import get_assets_path


class AboutDialog(QDialog):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.resize(320, 280)
        self.setStyleSheet(AboutDialogStyles.DIALOG_STYLE)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        pixmap = QPixmap(get_assets_path("logo.png")) \
            .scaled(96, 96, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        # Logo with spacing
        logo = QLabel(self)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setContentsMargins(0, 10, 0, 10)

        # Title
        title = QLabel("DeepSign", self)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(AboutDialogStyles.TITLE_STYLE)

        # Version and copyright
        version = "1.0.0"
        copyright_text = QLabel(
            f"<p>Version {version}</p>"
            f"<p>Copyright &copy; 2025 Daniils Grammatikopulo</p>"
            f"<p>Software for remote signature</p>",
            self,
        )
        copyright_text.setWordWrap(True)
        copyright_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        copyright_text.setStyleSheet(AboutDialogStyles.TEXT_STYLE)
        copyright_text.setContentsMargins(20, 10, 20, 20)

        # OK button
        button = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button.accepted.connect(self.accept)
        button.button(QDialogButtonBox.StandardButton.Ok).setStyleSheet(AboutDialogStyles.BUTTON_STYLE)
        button.setCenterButtons(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addWidget(copyright_text)
        layout.addSpacing(10)
        layout.addWidget(button)
        layout.setSpacing(5)
        layout.setContentsMargins(15, 15, 15, 15)
        self.setLayout(layout)
