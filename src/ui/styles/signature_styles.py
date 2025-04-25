class SignatureStyles:
    """
    Centralized styling for signature-related widgets
    """

    # Main dock widget style
    DOCK_STYLE = """
        QDockWidget {
            color: #1a202c;
            background-color: #f7fafc;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-weight: bold;
        }
        QDockWidget::title {
            background-color: #edf2f7;
            padding: 6px;
            text-align: center;
            border-bottom: 1px solid #e2e8f0;
        }
    """

    # Widget container style
    WIDGET_STYLE = """
        background-color: #f7fafc;
        font-family: 'Segoe UI', Arial, sans-serif;
    """

    # Label style
    LABEL_STYLE = """
        QLabel {
            color: #4a5568;
            font-weight: 500;
            font-size: 13px;
            margin-bottom: 2px;
        }
    """

    # Value label style
    VALUE_LABEL_STYLE = """
        QLabel {
            color: #3182ce;
            font-weight: 600;
            font-size: 13px;
            min-width: 30px;
            padding: 2px 5px;
            margin-top: 2px;
        }
    """

    # Checkbox style
    CHECKBOX_STYLE = """
        QCheckBox {
            color: #4a5568;
            font-weight: 500;
            font-size: 13px;
            padding: 2px;
            spacing: 5px;
            margin-top: 5px;
        }
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border: 1px solid #cbd5e0;
            border-radius: 3px;
            background-color: white;
        }
        QCheckBox::indicator:checked {
            background-color: #3182ce;
            border-color: #3182ce;
            image: url(icons/checkmark.png);
        }
        QCheckBox::indicator:hover {
            border-color: #3182ce;
        }
    """

    # Slider style
    SLIDER_STYLE = """
        QSlider {
            min-height: 24px;
        }
        QSlider::groove:horizontal {
            border: 1px solid #cbd5e0;
            height: 8px;
            background: white;
            border-radius: 4px;
            margin: 0px;
        }
        QSlider::handle:horizontal {
            background: #3182ce;
            border: 1px solid #2c5282;
            width: 18px;
            height: 18px;
            margin: -6px 0;
            border-radius: 9px;
        }
        QSlider::handle:horizontal:hover {
            background: #4299e1;
        }
        QSlider::add-page:horizontal {
            background: #edf2f7;
            border-radius: 4px;
        }
        QSlider::sub-page:horizontal {
            background: #90cdf4;
            border-radius: 4px;
        }
    """

    # Button style
    BUTTON_STYLE = """
        QToolButton {
            background-color: white;
            border: 1px solid #e2e8f0;
            border-radius: 21px;
            padding: 6px;
        }
        QToolButton:hover {
            background-color: #f7fafc;
            border: 1px solid #cbd5e0;
        }
        QToolButton:pressed {
            background-color: #edf2f7;
            border: 1px solid #cbd5e0;
        }
    """

    # Separator style
    SEPARATOR_STYLE = "background-color: #e2e8f0; margin: 0 8px;"

    # Layout constants
    FORM_SPACING = 10
    FORM_MARGINS = (14, 14, 14, 12)
    BUTTON_MARGINS = (0, 10, 0, 10)
    BUTTON_SIZE = (42, 42)
    BUTTON_ICON_SIZE = (24, 24)