from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMainWindow, QComboBox
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CFFS Label Calculator")

        # Set up the main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Set a consistent background color for the entire app
        self.central_widget.setStyleSheet("""
            QWidget {
                background-color: #2d3436;  /* Darker background for modern look */
                color: white;
            }
            QLabel {
                font-size: 32px;  /* Larger, modern font size */
                font-family: 'Arial', sans-serif;
                color: #dfe6e9;  /* Lighter font color */
                padding: 20px;
                background-color: transparent;
            }
            QPushButton {
                background-color: #0984e3;  /* Blue button for contrast */
                color: white;
                font-size: 20px;  /* Larger font size for button */
                font-family: 'Arial', sans-serif;
                border-radius: 15px;  /* Rounded corners */
                padding: 15px 30px;  /* Extra padding for larger button size */
                margin: 10px;
                border: 2px solid #74b9ff;  /* Stylish border */
            }
            QPushButton:hover {
                background-color: #74b9ff;  /* Lighter blue on hover */
                color: black;
            }
            QComboBox {
                background-color: #00cec9;  /* Aqua combo box for variety */
                color: white;
                font-size: 18px;  /* Stylish font size */
                font-family: 'Arial', sans-serif;
                border-radius: 10px;
                padding: 10px;
                border: 2px solid #00b894;
            }
            QComboBox QAbstractItemView {
                background-color: #00cec9;  /* Same background for dropdown */
                color: white;
                selection-background-color: #0984e3;  /* Stylish highlight */
            }
        """)

        # Add label at the top with shadow effect
        self.label = QLabel("Welcome to the CFFS Label Calculator!")
        self.label.setAlignment(Qt.AlignCenter)
        self.apply_shadow(self.label)
        self.main_layout.addWidget(self.label)

        # Create a container for the button and dropdown to center them together
        self.center_widget = QWidget()
        self.center_layout = QVBoxLayout()
        self.center_widget.setLayout(self.center_layout)
        self.main_layout.addWidget(self.center_widget, alignment=Qt.AlignCenter)

        # Add button
        self.button = QPushButton("Upload Data")
        self.button.clicked.connect(self.start)
        self.center_layout.addWidget(self.button, alignment=Qt.AlignCenter)

        # Add dropdown (QComboBox)
        self.dropdown = QComboBox()
        self.dropdown.addItems(["Option 1", "Option 2", "Option 3"])
        self.center_layout.addWidget(self.dropdown, alignment=Qt.AlignCenter)

        # Maximize window on startup
        self.showMaximized()

    def apply_shadow(self, widget):
        """Apply a drop shadow to the given widget."""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setColor(QColor(0, 0, 0, 160))  # Black shadow with transparency
        shadow.setOffset(3, 3)
        widget.setGraphicsEffect(shadow)

    def start(self):
        self.hide()
        from app.views.UploadPage import UploadPage
        self.upload_page = UploadPage()
        self.upload_page.show()

    def closeEvent(self, event):
        self.close()

    def showEvent(self, event):
        self.show()

    def resizeEvent(self, event):
        self.showMaximized()


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
