class AboutDialogStyles:
    """Updated modern styles for the About dialog."""

    DIALOG_STYLE = """
        QDialog {
            background-color: #FFFFFF;
            color: #333333;
            border: 1px solid #E0E0E0;
        }
    """

    TITLE_STYLE = """
        QLabel {
            color: #212121;
            font-size: 18pt;
            font-weight: 600;
        }
    """

    TEXT_STYLE = """
        QLabel {
            color: #555555;
            font-size: 10.5pt;
            line-height: 1.5em;
        }
    """

    BUTTON_STYLE = """
        QPushButton {
            background-color: #2196F3;
            color: #FFFFFF;
            border: none;
            padding: 8px 20px;
            font-size: 10pt;
            font-weight: 500;
            border-radius: 6px;
        }

        QPushButton:hover {
            background-color: #42A5F5;
        }

        QPushButton:pressed {
            background-color: #1E88E5;
        }
    """