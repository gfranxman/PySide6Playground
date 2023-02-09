import sys
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QFileDialog
from PySide6.QtGui import QAction, QIcon

app = QApplication(sys.argv)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Click File > Open to select a file", self)
        self.setCentralWidget(self.label)
        self.create_actions()
        self.create_menus()

    def create_actions(self):
        self.open_action = self.create_action("&Open", self.open_file, "Ctrl+O")

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

    def create_menus(self):
        self.file_menu = self.menuBar().addMenu("&File")
        self.file_menu.addAction(self.open_action)

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                    "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            with open(file_name, 'r') as f:
                text = f.read()
                self.label.setText(text)

window = MainWindow()
window.show()
sys.exit(app.exec_())

