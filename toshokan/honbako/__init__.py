from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from comel.wrapper import ComelMainWindowWrapper

from toshokan.honbako.widgets.view import ShelfView, ShelfIconSize


class Honbako(ComelMainWindowWrapper):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Honbako")
        self.setWindowIcon(QPixmap("honbako/icons/book_booktrack.png"))

        self.settings = QSettings("settings.ini", QSettings.IniFormat)
        self.settings.setFallbacksEnabled(False)

        self.setup_ui()
        self.setup_ui_menu_bar()

        self.post_setup_ui()

    def post_setup_ui(self):
        shelf_icon_size = self.settings.value(
            "shelf/icon_size",
            ShelfIconSize.MEDIUM,
        )
        self.shelf_view.set_shelf_icon_size(
            int(shelf_icon_size)
        )
        self.shelf_view.setViewMode(
            self.settings.value("shelf/view_mode", QListView.IconMode)
        )
        self.resize(
            self.settings.value("size", QSize(640, 480))
        )
        self.move(
            self.settings.value("pos", QPoint(50, 50))
        )

        dark_mode = self.settings.value("dark_mode", 0)
        self.is_light = int(dark_mode)
        self.run_toggle_theme()

    def closeEvent(self, event):
        self.settings.setValue("shelf/icon_size", self.shelf_view.icon_size)
        self.settings.setValue("shelf/view_mode", self.shelf_view.viewMode())
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        self.settings.setValue("dark_mode", 0 if self.is_light else 1)
        event.accept()

    def setup_ui(self):
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        layout = QVBoxLayout()
        self.main_widget.setLayout(layout)

        self.theme_label = QLabel("Light Theme" if self.is_light else "Dark Theme")
        self.theme_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.theme_label)

        toggle_theme_btn = QPushButton("Toggle Theme")
        toggle_theme_btn.clicked.connect(self.run_toggle_theme)
        layout.addWidget(toggle_theme_btn)

        self.shelf_view = ShelfView()
        layout.addWidget(self.shelf_view)

    def setup_ui_menu_bar(self):
        self.menu_bar = QMenuBar()
        self.setMenuBar(self.menu_bar)

        file_menu = QMenu("&File", self.menu_bar)
        self.menu_bar.addMenu(file_menu)
        self.exit_action = QAction("E&xit", file_menu)
        self.exit_action.triggered.connect(self.close)
        file_menu.addAction(self.exit_action)

        view_menu = self.menu_bar.addMenu("&View")
        toggle_shelf_mode_action = view_menu.addAction("Toggle Shelf &Mode")
        toggle_shelf_mode_action.triggered.connect(self.shelf_view.toggle_view_mode)
        thumbs_size_menu = view_menu.addMenu("Thumbnails &Size")
        thumbs_small_action = thumbs_size_menu.addAction("Small")
        thumbs_small_action.triggered.connect(
            lambda: self.shelf_view.set_shelf_icon_size(ShelfIconSize.SMALL)
        )
        thumbs_medium_action = thumbs_size_menu.addAction("Medium")
        thumbs_medium_action.triggered.connect(
            lambda: self.shelf_view.set_shelf_icon_size(ShelfIconSize.MEDIUM)
        )
        thumbs_large_action = thumbs_size_menu.addAction("Large")
        thumbs_large_action.triggered.connect(
            lambda: self.shelf_view.set_shelf_icon_size(ShelfIconSize.LARGE)
        )
        thumbs_huge_action = thumbs_size_menu.addAction("Huge")
        thumbs_huge_action.triggered.connect(
            lambda: self.shelf_view.set_shelf_icon_size(ShelfIconSize.HUGE)
        )

        help_menu = QMenu("&Help", self.menu_bar)
        self.menu_bar.addMenu(help_menu)
        about_action = QAction(f"&About {QApplication.applicationName()}", help_menu)
        help_menu.addAction(about_action)

    def run_toggle_theme(self):
        self.toggle_theme()
        text = "Light Theme" if self.is_light else "Dark Theme"
        self.theme_label.setText(text)
