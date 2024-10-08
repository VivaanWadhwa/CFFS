from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMainWindow, QHBoxLayout
from PyQt5.QtCore import Qt

class NonStdPrepsPage(QMainWindow):

    def __init__(self, parent: QWidget | None = ..., flags: Qt.WindowFlags | Qt.WindowType = ...) -> None:
        super().__init__(parent, flags)
        self.setWindowTitle("Non Standard Preps")

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = QVBoxLayout()
        self.centralWidget.setLayout(self.mainLayout)