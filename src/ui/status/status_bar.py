from PySide6.QtWidgets import QStatusBar, QLabel, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy
from PySide6.QtGui import QFont


class StatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("""
            QStatusBar {
                background-color: #171717;
                color: #9b9fac;
                padding: 6px;
                border-top: 1px solid #171717;
            }
            QLabel {
                font-size: 12px;
            }
        """)

        container = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(15)

        font = QFont("Segoe UI", 13)
        font.setBold(False)

        self.points_label = QLabel("🖊️ <b>Points:</b> 0")
        self.points_label.setFont(font)
        self.points_label.setStyleSheet("color: #00d3ee;")

        self.finger_label = QLabel("☝️ <b>Position:</b> X=0, Y=0")
        self.finger_label.setFont(font)
        self.finger_label.setStyleSheet("color: #ffae00;")

        layout.addWidget(self.points_label)
        layout.addWidget(self.finger_label)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addItem(spacer)

        container.setLayout(layout)
        self.addPermanentWidget(container, 1)

    def update_status(self, points_count: int, finger_x: int, finger_y: int):
        self.points_label.setText(f"🖊️ <b>Points:</b> {points_count}")
        self.finger_label.setText(f"☝️ <b>X: {finger_x} Y: {finger_y}</b> ")
