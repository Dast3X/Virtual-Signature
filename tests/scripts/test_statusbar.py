import unittest

from PySide6.QtCore import QTimer
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication

from src.ui.status.status_bar import StatusBar


class TestStatusBar(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create QApplication instance for the tests
        if not QApplication.instance():
            cls.app = QApplication([])
        else:
            cls.app = QApplication.instance()

    def setUp(self):
        self.status_bar = StatusBar()

    def test_initialization(self):
        """Test if StatusBar initializes properly"""
        # Check if it's a StatusBar instance
        self.assertIsInstance(self.status_bar, StatusBar)

        # Verify that labels exist
        self.assertTrue(hasattr(self.status_bar, 'points_label'))
        self.assertTrue(hasattr(self.status_bar, 'finger_label'))

        # Check initial values
        self.assertEqual(self.status_bar.points_label.text(), "🖊️ <b>Points:</b> 0")
        self.assertEqual(self.status_bar.finger_label.text(), "☝️ <b>Position:</b> X=0, Y=0")

    def test_update_status(self):
        """Test if update_status method updates labels correctly"""
        # Wait for the status bar to be fully initialized
        QTest.qWaitForWindowExposed(self.status_bar)

        # Update status with new values
        points = 42
        x_pos = 100
        y_pos = 200

        # Use a QTimer to execute the update on the main thread
        QTimer.singleShot(0, lambda: self.status_bar.update_status(points, x_pos, y_pos))
        QTest.qWait(100)  # Wait for the update to process

        # Check if labels were updated
        self.assertEqual(self.status_bar.points_label.text(), f"🖊️ <b>Points:</b> {points}")
        self.assertEqual(self.status_bar.finger_label.text(), f"☝️ <b>X: {x_pos} Y: {y_pos}</b> ")

        # Update with different values
        points = 0
        x_pos = -5
        y_pos = 10

        # Use a QTimer to execute the update on the main thread
        QTimer.singleShot(0, lambda: self.status_bar.update_status(points, x_pos, y_pos))
        QTest.qWait(100)  # Wait for the update to process

        self.assertEqual(self.status_bar.points_label.text(), f"🖊️ <b>Points:</b> {points}")
        self.assertEqual(self.status_bar.finger_label.text(), f"☝️ <b>X: {x_pos} Y: {y_pos}</b> ")


if __name__ == '__main__':
    unittest.main()
