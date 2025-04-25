class MainWindowStyles:
    """
    Centralized styling for main window components
    """

    # Main window styling
    WINDOW_STYLE = """
        QMainWindow {
            background-color: #f8fafc;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
    """

    # Camera window styling
    CAMERA_WINDOW_STYLE = """
        QLabel {
            font-size: 20px;
            background-color: #e2e8f0;
            border: 1px solid #cbd5e0;
            border-radius: 4px;
            color: #4a5568;
        }
    """

    # No capture text styling
    NO_CAPTURE_TEXT_STYLE = """
        font-size: 20px;
        font-weight: bold;
        color: #ef4444;
    """

    # Loading text styling
    LOADING_TEXT_STYLE = """
        font-size: 18px;
        color: #3b82f6;
        font-weight: 500;
    """

    # Central widget styling
    CENTRAL_WIDGET_STYLE = """
        background-color: #f1f5f9;
        padding: 10px;
    """

    # Layout constants
    LOADING_GIF_SIZE = (128, 128)
    CAMERA_MIN_SIZE = (640, 480)
    WINDOW_TITLE = "DeepSign"