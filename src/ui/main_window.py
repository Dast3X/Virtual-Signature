from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QImage, QMovie, QIcon, QAction
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QApplication

from src.ui.status.status_bar import StatusBar
from src.ui.styles.main_dock_styles import MainWindowStyles
from src.ui.dock.camera_setting_dock import CameraSettingsDock
from src.ui.dock.signature_settings import SignatureSettingsDock
from src.ui.about.about_dialog import AboutDialog
from src.utils.utils import get_assets_path
from src.video_thread import VideoThread


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.VideoThread = VideoThread()
        self.initUI()

    def closeEvent(self, event):
        if self.VideoThread.isRunning():
            self.VideoThread.stop()
        event.accept()

    def updateImage(self, image: QImage):
        if not image.isNull():
            # Stop any loading animation if it's playing
            if self.loading_movie.state() == QMovie.Running:
                self.loading_movie.stop()
            self.camera_window.setMovie(None)
            self.camera_window.setPixmap(QPixmap.fromImage(image))
        elif self.VideoThread.is_changing_settings:
            # Show loading animation
            self.camera_window.setText("")
            self.camera_window.setMovie(self.loading_movie)
            if self.loading_movie.state() != QMovie.Running:
                self.loading_movie.start()
        elif not self.VideoThread.isRunning():
            # Stop any loading animation
            if self.loading_movie.state() == QMovie.Running:
                self.loading_movie.stop()
            self.camera_window.setMovie(None)
            self.camera_window.setText("No capture 😠")
        else:
            # Show loading animation
            self.camera_window.setText("")
            self.camera_window.setMovie(self.loading_movie)
            if self.loading_movie.state() != QMovie.Running:
                self.loading_movie.start()

        # Update status bar with signature points count
        self.updateStatusBar()

    def initMainWindow(self) -> None:
        screen_rect = QApplication.primaryScreen().availableGeometry()
        window_width = screen_rect.width() // 2
        window_height = screen_rect.height() // 2
        self.setGeometry(
            screen_rect.x() + (screen_rect.width() - window_width) // 2,
            screen_rect.y() + (screen_rect.height() - window_height) // 2,
            window_width,
            window_height,
        )
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowTitle(MainWindowStyles.WINDOW_TITLE)
        self.setStyleSheet(MainWindowStyles.WINDOW_STYLE)

    def initVideoThread(self) -> None:
        self.VideoThread.ImageUpdate.connect(self.updateImage)
        self.VideoThread.StatusUpdate.connect(self.updateStatusBar)
        self.camera_dock = CameraSettingsDock(self)
        self.signature_dock = SignatureSettingsDock(self)

    def initMenuBar(self) -> None:
        # Create menu bar
        menu_bar = self.menuBar()

        # About action
        about_action = QAction("About", self)
        about_action.triggered.connect(self.showAboutDialog)
        menu_bar.addAction(about_action)

    def initStatusBar(self) -> None:
        self.statusbar = StatusBar(self)
        self.setStatusBar(self.statusbar)
        self.statusbar.update_status(0, 0, 0)

    def updateStatusBar(self):
        points_count = len(self.VideoThread.signature_points)
        finger_x, finger_y = self.VideoThread.current_finger_position
        self.statusbar.update_status(points_count, finger_x, finger_y)

    def showAboutDialog(self) -> None:
        dialog = AboutDialog(self)
        dialog.exec()

    def initUI(self):
        self.initMainWindow()
        central_widget = QWidget()
        central_widget.setStyleSheet(MainWindowStyles.CENTRAL_WIDGET_STYLE)
        self.setCentralWidget(central_widget)
        self.setWindowIcon(QIcon(get_assets_path("logo.png")))
        self.initVideoThread()
        self.initMenuBar()
        self.initStatusBar()  # Initialize the status bar
        flags = self.windowFlags()
        flags &= ~Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.setWindowFlags(Qt.Window)

        self.VBL = QVBoxLayout()
        self.camera_window = QLabel()
        self.camera_window.setStyleSheet(MainWindowStyles.CAMERA_WINDOW_STYLE)
        self.camera_window.setMinimumSize(*MainWindowStyles.CAMERA_MIN_SIZE)
        self.camera_window.setAlignment(Qt.AlignCenter)

        # Create the loading animation using a GIF
        self.loading_movie = QMovie(get_assets_path("loading.gif"))
        self.loading_movie.setScaledSize(QSize(*MainWindowStyles.LOADING_GIF_SIZE))

        self.VBL.addWidget(self.camera_window)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.camera_dock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.signature_dock)
        central_widget.setLayout(self.VBL)
