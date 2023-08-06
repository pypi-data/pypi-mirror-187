import os
from logging import getLogger

from PyQt5.QtCore import Qt, QSettings, QTimer, QSize, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QCloseEvent, QCursor
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QStatusBar,
    QScrollArea,
    QScroller,
    QComboBox,
    QMessageBox,
)

from rare.components.tabs import TabWidget
from rare.components.tray_icon import TrayIcon
from rare.shared import LegendaryCoreSingleton, GlobalSignalsSingleton, ArgumentsSingleton
from rare.utils.paths import lock_file

logger = getLogger("MainWindow")


class MainWindow(QMainWindow):
    # int: exit code
    exit_app: pyqtSignal = pyqtSignal(int)

    def __init__(self, parent=None):
        self._exit_code = 0
        self._accept_close = False
        self._window_launched = False
        super(MainWindow, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.core = LegendaryCoreSingleton()
        self.signals = GlobalSignalsSingleton()
        self.args = ArgumentsSingleton()

        self.settings = QSettings()

        self.setWindowTitle("Rare - GUI for legendary")
        self.tab_widget = TabWidget(self)
        self.tab_widget.exit_app.connect(self.on_exit_app)
        self.setCentralWidget(self.tab_widget)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        width, height = 1280, 720
        if self.settings.value("save_size", False, bool):
            width, height = self.settings.value("window_size", (width, height), tuple)

        self.resize(width, height)

        if not self.args.offline:
            try:
                from rare.utils.rpc import DiscordRPC

                self.rpc = DiscordRPC()
            except ModuleNotFoundError:
                logger.warning("Discord RPC module not found")

        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_finished)
        self.timer.start(1000)

        self.tray_icon: TrayIcon = TrayIcon(self)
        self.tray_icon.exit_app.connect(self.on_exit_app)
        self.tray_icon.show_app.connect(self.show)
        self.tray_icon.activated.connect(lambda r: self.toggle() if r == self.tray_icon.DoubleClick else None)

        self.signals.send_notification.connect(
            lambda title: self.tray_icon.showMessage(
                self.tr("Download finished"),
                self.tr("Download finished. {} is playable now").format(title),
                self.tray_icon.Information,
                4000,
            )
            if self.settings.value("notification", True, bool)
            else None
        )

        # enable kinetic scrolling
        for scroll_area in self.findChildren(QScrollArea):
            if not scroll_area.property("no_kinetic_scroll"):
                QScroller.grabGesture(scroll_area.viewport(), QScroller.LeftMouseButtonGesture)

            # fix scrolling
            for combo_box in scroll_area.findChildren(QComboBox):
                combo_box.wheelEvent = lambda e: e.ignore()

    def center_window(self):
        # get the margins of the decorated window
        margins = self.windowHandle().frameMargins()
        # get the screen the cursor is on
        current_screen = QApplication.screenAt(QCursor.pos())
        if not current_screen:
            current_screen = QApplication.primaryScreen()
        # get the available screen geometry (excludes panels/docks)
        screen_rect = current_screen.availableGeometry()
        decor_width = margins.left() + margins.right()
        decor_height = margins.top() + margins.bottom()
        window_size = QSize(self.width(), self.height()).boundedTo(
            screen_rect.size() - QSize(decor_width, decor_height)
        )

        self.resize(window_size)
        self.move(screen_rect.center() - self.rect().adjusted(0, 0, decor_width, decor_height).center())

    @pyqtSlot()
    def show(self) -> None:
        super(MainWindow, self).show()
        if not self._window_launched:
            self.center_window()
        self._window_launched = True

    def hide(self) -> None:
        if self.settings.value("save_size", False, bool):
            size = self.size().width(), self.size().height()
            self.settings.setValue("window_size", size)
        super(MainWindow, self).hide()

    def toggle(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()

    def timer_finished(self):
        file_path = lock_file()
        if os.path.exists(file_path):
            file = open(file_path, "r")
            action = file.read()
            file.close()
            if action.startswith("show"):
                self.show()
            os.remove(file_path)
        self.timer.start(1000)

    @pyqtSlot()
    @pyqtSlot(int)
    def on_exit_app(self, exit_code=0) -> None:
        self._exit_code = exit_code
        self.close()

    def close(self) -> bool:
        self._accept_close = True
        return super(MainWindow, self).close()

    def closeEvent(self, e: QCloseEvent) -> None:
        # lk: `accept_close` is set to `True` by the `close()` method, overrides exiting to tray in `closeEvent()`
        # lk: ensures exiting instead of hiding when `close()` is called programmatically
        if not self._accept_close:
            if self.settings.value("sys_tray", False, bool):
                self.hide()
                e.ignore()
                return
        # FIXME: Fix this with the download tab redesign
        if not self.args.offline and self.tab_widget.downloads_tab.is_download_active:
            reply = QMessageBox.question(
                self,
                self.tr("Quit {}?").format(QApplication.applicationName()),
                self.tr("There are active downloads. Are you sure you want to quit?"),
                buttons=(QMessageBox.Yes | QMessageBox.No),
                defaultButton=QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                # clear queue
                self.tab_widget.downloads_tab.queue_widget.update_queue([])
                self.tab_widget.downloads_tab.stop_download()
            else:
                e.ignore()
                return
        # FIXME: End of FIXME
        self.timer.stop()
        self.tray_icon.deleteLater()
        self.hide()
        self.exit_app.emit(self._exit_code)
        super(MainWindow, self).closeEvent(e)

