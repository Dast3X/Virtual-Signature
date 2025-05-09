from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QImage, QMovie, QIcon, QAction
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QApplication, QMenu

from src.ui.about.about_dialog import AboutDialog
from src.ui.dock.camera_setting_dock import CameraSettingsDock
from src.ui.dock.signature_settings_dock import SignatureSettingsDock
from src.ui.help.help_dialog import HelpDialog
from src.ui.status.status_bar import StatusBar
from src.ui.styles.main_dock_styles import MainWindowStyles
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
        self.VideoThread.ImageUpdate.disconnect(self.updateImage)
        self.VideoThread.StatusUpdate.disconnect(self.updateStatusBar)
        event.accept()

    def updateImage(self, image: QImage):
        if image and not image.isNull():
            self.stopLoading()
            self.camera_window.setPixmap(QPixmap.fromImage(image))
        else:
            self.camera_window.setPixmap(QPixmap())
            self.startLoading() if self.VideoThread.is_changing_settings or self.VideoThread.isRunning() else self.showNoCapture()

        self.updateStatusBar()

    def startLoading(self):
        self.camera_window.setText("")
        self.camera_window.setMovie(self.loading_movie)
        if self.loading_movie.state() != QMovie.Running:
            self.loading_movie.start()

    def stopLoading(self):
        if self.loading_movie.state() == QMovie.Running:
            self.loading_movie.stop()
        self.camera_window.setMovie(None)

    def showNoCapture(self):
        self.stopLoading()
        self.camera_window.setText("No capture 😠")

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

        # Help menu
        help_menu = QMenu("Help", self)

        # Help action
        help_action = QAction("User Guide", self)
        help_action.setShortcut("F1")
        help_action.triggered.connect(self.showHelpDialog)
        help_menu.addAction(help_action)

        # About action
        about_action = QAction("About", self)
        about_action.triggered.connect(self.showAboutDialog)
        help_menu.addAction(about_action)

        # Add Help menu to menu bar
        menu_bar.addMenu(help_menu)

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

    def showHelpDialog(self) -> None:
        dialog = HelpDialog(self)
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
