import os
import sys


def get_assets_path(icon_name: str) -> str:
    """
    Get the path to an icon file in resources/icons directory.
    Works both in development and PyInstaller bundle.

    Args:
        icon_name (str): The name of the icon file.

    Returns:
        str: The full path to the icon file.
    """
    if hasattr(sys, '_MEIPASS'):  # Running in PyInstaller bundle
        base_path = sys._MEIPASS
    else:  # Running in normal Python environment
        # Navigate up to project root from current file location
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.abspath(os.path.join(current_dir, '..', '..'))

    icons_dir = os.path.join(base_path, "resources", "icons")
    return os.path.join(icons_dir, icon_name)