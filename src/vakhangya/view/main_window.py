from pathlib import Path
from typing import Optional

from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QDragMoveEvent
from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QFileDialog, QLabel
from natsort import natsorted
from qtanim import fade_in, fade_out
from qthandy import vbox, vspacer, incr_font, busy, italic, hbox, retain_when_hidden

from vakhangya.view.browser import AlbumDisplayWidget
from vakhangya.view.common import qta_icon, error_msg
from vakhangya.view.core import retrieve_album, collect_songs, generate_cue_file
from vakhangya.view.domain import Album


class VakhangyaMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Vakhangya')
        self.setWindowIcon(qta_icon('fa5s.skull'))
        self._centralWidget = QWidget()
        self.setCentralWidget(self._centralWidget)
        self.setAcceptDrops(True)
        self.setContentsMargins(40, 20, 40, 40)
        self.resize(640, 400)

        self._currentAlbum: Optional[Album] = None
        self._currentPath: Optional[Path] = None

        vbox(self._centralWidget)

        self._btnOpenFolder = QPushButton('')
        self._btnOpenFolder.setIconSize(QSize(22, 22))
        self._btnOpenFolder.setMaximumWidth(100)
        self._btnOpenFolder.setToolTip('Open folder...')
        self._btnOpenFolder.setIcon(qta_icon('fa5s.folder-open'))
        self._btnOpenFolder.clicked.connect(self._selectAlbum)

        self._btnSave = QPushButton('Save')
        self._btnSave.setIconSize(QSize(24, 24))
        self._btnSave.setMinimumWidth(120)
        self._btnSave.setMaximumWidth(200)
        self._btnSave.setIcon(qta_icon('fa5s.save'))
        self._btnSave.setDisabled(True)
        incr_font(self._btnSave, 6)
        self._btnSave.clicked.connect(self._saveCueFile)

        self._lblSaved = QLabel('Saved')
        italic(self._lblSaved)
        retain_when_hidden(self._lblSaved)
        self._lblSaved.setHidden(True)

        self._albumDisplay = AlbumDisplayWidget()
        self._albumDisplay.setDisabled(True)

        self._centralWidget.layout().addWidget(self._btnOpenFolder)
        self._centralWidget.layout().addWidget(vspacer(10))
        self._centralWidget.layout().addWidget(self._albumDisplay)
        self._centralWidget.layout().addWidget(vspacer(10))
        btnWidget = QWidget(self._centralWidget)
        hbox(btnWidget)
        btnWidget.layout().addWidget(self._lblSaved)
        btnWidget.layout().addWidget(self._btnSave)
        self._centralWidget.layout().addWidget(btnWidget, alignment=Qt.AlignmentFlag.AlignRight)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        self.raise_()
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            if url.isLocalFile():
                event.acceptProposedAction()
                path = Path(url.path())
                if path.is_file():
                    error_msg('Dropped item is not a directory', self._centralWidget)
                    return
                self._selectAlbum(path)

    @busy
    def _selectAlbum(self, path: Optional[Path] = None):
        if path is None:
            folder = QFileDialog.getExistingDirectory(self._centralWidget, 'Open folder', '~',
                                                      QFileDialog.Option.ShowDirsOnly)
            self._currentPath = Path(folder)
        else:
            self._currentPath = path
        try:
            self._currentAlbum = retrieve_album(self._currentPath)
        except Exception as ex:
            error_msg(str(ex), self._centralWidget)
            self._currentAlbum = None
            self._albumDisplay.clear()
            self._albumDisplay.setDisabled(True)
            self._btnSave.setDisabled(True)

        if self._currentAlbum:
            songs = collect_songs(self._currentPath)
            self._currentAlbum.songs.extend(natsorted(songs, key=lambda x: x.title))
            self._albumDisplay.setAlbum(self._currentAlbum)
            self._albumDisplay.setEnabled(True)
            self._btnSave.setEnabled(True)

    @busy
    def _saveCueFile(self):
        saved = generate_cue_file(self._currentAlbum, self._currentPath)
        if saved:
            fade_in(self._lblSaved)
            QTimer.singleShot(500, lambda: fade_out(self._lblSaved))
