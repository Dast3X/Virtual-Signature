# camera_styles.py

class CameraStyles:
    """
    Centralized styling for camera-related widgets
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

    # Combobox style
    COMBOBOX_STYLE = """
        QComboBox {
            border: 1px solid #cbd5e0;
            border-radius: 4px;
            padding: 5px 10px;
            background-color: white;
            min-height: 24px;
            selection-background-color: #3182ce;
            color: #2d3748;
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left: 1px solid #cbd5e0;
            border-top-right-radius: 4px;
            border-bottom-right-radius: 4px;
        }
        QComboBox::down-arrow {
            image: url(icons/dropdown_arrow.png);
            width: 12px;
            height: 12px;
        }
        QComboBox QAbstractItemView {
            border: 1px solid #cbd5e0;
            border-radius: 0px;
            background-color: white;
            selection-background-color: #3182ce;
            selection-color: white;
        }
    """

    # Label style
    LABEL_STYLE = """
        QLabel {
            color: #4a5568;
            font-weight: 500;
            font-size: 13px;
        }
    """

    # White circular button style
    TOGGLE_BUTTON_STYLE = """
        QToolButton {
            background-color: white;
            border: 1px solid #e2e8f0;
            border-radius: 21px;  /* Half of the width/height to make it circular */
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
        QToolButton:disabled {
            background-color: #f7fafc;
            border: 1px solid #e2e8f0;
        }
    """

    # Separator style
    SEPARATOR_STYLE = "background-color: #e2e8f0; margin: 0 8px;"

    # Enhanced FPS Counter styles with gradients, shadows and modern design
    FPS_COUNTER_STYLE = """
        QLabel {
            color: #64748b;
            font-weight: 800;
            font-size: 16px;
            letter-spacing: 0.5px;
            border-radius: 8px;
            padding: 8px 12px;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 #f8fafc, stop:1 #e2e8f0);
            border: 1px solid #e2e8f0;
            margin: 0px 12px;
            text-align: center;
        }
    """

    FPS_COUNTER_STYLE_GOOD = """
        QLabel {
            color: #16a34a;
            font-weight: 800;
            font-size: 16px;
            letter-spacing: 0.5px;
            border-radius: 8px;
            padding: 8px 12px;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 #f0fdf4, stop:1 #dcfce7);
            border: 1px solid #bbf7d0;
            margin: 0px 12px;
            text-align: center;
        }
    """

    FPS_COUNTER_STYLE_MEDIUM = """
        QLabel {
            color: #d97706;
            font-weight: 800;
            font-size: 16px;
            letter-spacing: 0.5px;
            border-radius: 8px;
            padding: 8px 12px;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 #fefce8, stop:1 #fef9c3);
            border: 1px solid #fde68a;
            margin: 0px 12px;
            text-align: center;
        }
    """

    FPS_COUNTER_STYLE_LOW = """
        QLabel {
            color: #dc2626;
            font-weight: 800;
            font-size: 16px;
            letter-spacing: 0.5px;
            border-radius: 8px;
            padding: 8px 12px;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 #fef2f2, stop:1 #fee2e2);
            border: 1px solid #fecaca;
            margin: 0px 12px;
            text-align: center;
        }
    """

    # Layout constants
    FORM_SPACING = 10
    FORM_MARGINS = (14, 14, 14, 12)
    BUTTON_MARGINS = (0, 10, 0, 0)
    FPS_COUNTER_MARGINS = (10, 14, 10, 14)
    COMBOBOX_HEIGHT = 30
    TOGGLE_BUTTON_SIZE = (42, 42)
    TOGGLE_ICON_SIZE = (24, 24)
