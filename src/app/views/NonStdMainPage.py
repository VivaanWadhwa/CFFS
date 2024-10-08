from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMainWindow, QHBoxLayout, QApplication
import sys

class NonStdMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Non Standard Main Page")
        self.setGeometry(100, 100, 800, 600)  # Set window size and position

        # Set up the main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Apply a stylesheet to the entire window
        self.central_widget.setStyleSheet("""
            QWidget {
                background-color: #f2f2f2;
                font-family: Arial, sans-serif;
            }
            QLabel {
                font-size: 36px;
                font-weight: bold;
                color: #333;
                padding-left: 30px;
                margin-top: 20px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 20px;
                padding: 12px 24px;
                border-radius: 10px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # Create label and position it at the top-left
        self.label = QLabel("Non Standard Preps and Items")
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.main_layout.addWidget(self.label, alignment=Qt.AlignLeft | Qt.AlignTop)

        # Create a container for the buttons and center them
        self.button_layout = QHBoxLayout()
        self.main_layout.addLayout(self.button_layout)

        # Add 'Items' button
        self.itemButton = QPushButton("Items")
        self.button_layout.addWidget(self.itemButton)

        # Add 'Preps' button next to the 'Items' button
        self.prepButton = QPushButton("Preps")
        self.button_layout.addWidget(self.prepButton)

        # Center the button layout horizontally and add space above and below
        self.main_layout.addStretch(1)  # Pushes buttons down to the center
        self.button_layout.setAlignment(Qt.AlignVCenter)

        # Add stretch at the bottom to ensure buttons stay centered vertically
        self.main_layout.addStretch(1)

        # Maximize the window on startup
        self.showNormal()

    def showItems(self):
        pass

    def showPreps(self):
        self.hide()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NonStdMain()
    window.show()
    sys.exit(app.exec_())
