import sys
from PySide6.QtGui import (
    QImage,
    QPainter,
    QPen,
    QPixmap,
)
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMenu,
    QMenuBar,
    QSizePolicy,
)
from PySide6.QtGui import (
    QAction,
    QIcon,
)
from PySide6 import (
    Qt,
    QtCore,
    QtGui,
)

app = QApplication(sys.argv)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a label widget to display the image
        self.label = QLabel(self)
        self.label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.label.setScaledContents(True)
        self.setCentralWidget(self.label)

        # Create actions for the menu bar
        self.open_action = self.create_action("&Open", self.open_file, "Ctrl+O")
        self.exit_action = self.create_action("&Exit", self.close, "Ctrl+Q")

        # Create the menu bar
        self.file_menu = self.menuBar().addMenu("&File")
        self.file_menu.addAction(self.open_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)

        self.last_point = QtCore.QPoint(0, 0)

    def create_action(self, text, slot=None, shortcut=None, icon=None,
                      tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                   "Images (*.png *.xpm *.jpg *.bmp *.gif);;All Files (*)",
                                                   options=options)
        if file_name:
            image = QImage(file_name)
            pixmap =QPixmap.fromImage(image)
            self.label.setPixmap(pixmap)
            self.resize(image.width(), image.height())

    def mousePressEvent(self, event):
        self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.MouseButton.LeftButton:
            print(f"paint line from {self.last_point} to {event.pos()}")
            self.pen = QPen()
            self.pen.setColor("red") # QtGui.QColor.red)
            self.pen.setWidth(5)
            self.pen.setStyle(QtCore.Qt.PenStyle.SolidLine)

            # paint on off-screen pixmap, then set the pixmap back to the label
            pixmap =  self.label.pixmap()  # fresh copy

            painter = QPainter(pixmap)
            painter.setPen(self.pen)
            painter.drawLine(self.last_point, event.pos())
            painter.end()

            self.label.setPixmap(pixmap)  # write it back

            self.last_point = event.pos()


window = MainWindow()
window.show()
sys.exit(app.exec_())
