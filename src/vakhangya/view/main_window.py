from typing import Optional

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton
from qthandy import vbox, vspacer, incr_font

from vakhangya.view.browser import AlbumDisplayWidget
from vakhangya.view.common import qta_icon
from vakhangya.view.domain import Album, Song


class VakhangyaMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Vakhangya')
        self._centralWidget = QWidget()
        self.setCentralWidget(self._centralWidget)
        self.setContentsMargins(40, 20, 40, 40)
        self.resize(640, 400)

        self._currentAlbum: Optional[Album] = None

        vbox(self._centralWidget)

        self._btnOpenFolder = QPushButton('')
        self._btnOpenFolder.setIconSize(QSize(24, 24))
        self._btnOpenFolder.setMaximumWidth(100)
        self._btnOpenFolder.setToolTip('Open folder...')
        self._btnOpenFolder.setIcon(qta_icon('fa5s.folder-open'))
        self._btnOpenFolder.clicked.connect(self._selectAlbum)

        self._btnSave = QPushButton('Save')
        self._btnSave.setIconSize(QSize(24, 24))
        self._btnSave.setMinimumWidth(130)
        self._btnSave.setMaximumWidth(200)
        self._btnSave.setIcon(qta_icon('fa5s.save'))
        self._btnSave.setDisabled(True)
        incr_font(self._btnSave, 8)

        self._albumDisplay = AlbumDisplayWidget()
        self._albumDisplay.setDisabled(True)

        self._centralWidget.layout().addWidget(self._btnOpenFolder)
        self._centralWidget.layout().addWidget(vspacer(10))
        self._centralWidget.layout().addWidget(self._albumDisplay)
        self._centralWidget.layout().addWidget(vspacer(10))
        self._centralWidget.layout().addWidget(self._btnSave, alignment=Qt.AlignmentFlag.AlignRight)

    def _selectAlbum(self):
        self._currentAlbum = Album('Test band', 'Test Album', year=2002)
        for song in ['Song 1', 'Song 2', 'Song 3', 'Song 4', 'Song 5', 'Song 6']:
            self._currentAlbum.songs.append(Song(song))

        self._albumDisplay.setAlbum(self._currentAlbum)
        self._albumDisplay.setEnabled(True)
        self._btnSave.setEnabled(True)
