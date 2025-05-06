import sys
import os
import traceback
from PySide6.QtWidgets import QApplication, QMessageBox

from src.ui.main_window import MainWindow


def exception_hook(exctype, value, tb):
    """Global function to catch unhandled exceptions."""
    message = ''.join(traceback.format_exception(exctype, value, tb))
    print(message)

    # Create a log file in a location accessible to the user
    log_path = os.path.join(os.path.expanduser("~"), "virtual_signature_error.log")
    with open(log_path, 'a') as f:
        f.write(message + '\n')

    # Show error dialog to user
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("An unexpected error occurred!")
    msg.setInformativeText(f"Details have been saved to: {log_path}")
    msg.setWindowTitle("Error")
    msg.setDetailedText(message)
    msg.exec()


def main():
    # Set up exception handling
    sys.excepthook = exception_hook

    try:
        print("[INFO] Starting application")
        app = QApplication(sys.argv)
        print("[INFO] QApplication created")
        window = MainWindow()
        print("[INFO] MainWindow created")
        window.show()
        print("[INFO] Window shown")
        sys.exit(app.exec())
    except Exception as e:
        print(f"[ERROR] Exception in main: {str(e)}")
        traceback.print_exc()
        # Show error to user
        if QApplication.instance():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Failed to start the application")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("Error")
            msg.setDetailedText(traceback.format_exc())
            msg.exec()


if __name__ == "__main__":
    main()