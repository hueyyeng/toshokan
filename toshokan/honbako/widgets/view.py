import glob
import os.path

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class ShelfIconSize:
    SMALL = 64
    MEDIUM = 128
    LARGE = 256
    HUGE = 512


class ShelfView(QListView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)

        self.icon_size = ShelfIconSize.MEDIUM

        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.populate_model()

    def populate_model(self):
        pics = glob.glob(r"E:\YengKF\Documents\Huey\Artworks\Thumbs\*.jpg")
        for pic in pics:
            item = QStandardItem()
            icon = QIcon(pic)
            item.setIcon(icon)
            filename = os.path.basename(pic)
            item.setText(filename)
            self.model.appendRow(item)

    def toggle_view_mode(self):
        if self.viewMode() == QListView.IconMode:
            self.setViewMode(QListView.ListMode)
        else:
            self.setViewMode(QListView.IconMode)

    def set_shelf_icon_size(self, icon_size: int):
        self.icon_size = icon_size
        self.setIconSize(QSize(icon_size, icon_size))
