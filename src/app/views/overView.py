from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMainWindow, QListWidget, QHBoxLayout

class overviewPage(QMainWindow):
    def __init__(self, selected_path):
        super().__init__()
        self.setWindowTitle("Item List Page")
        self.setGeometry(100, 100, 800, 600)  # Set window size and position

        # Set up the main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Create the list widget
        self.list_widget = QListWidget()
        self.main_layout.addWidget(self.list_widget)

        # Create a layout for the buttons
        self.button_layout = QVBoxLayout()
        self.main_layout.addLayout(self.button_layout)

        # Create buttons and connect them to methods
        self.button1 = QPushButton("Show Category 1")
        self.button1.clicked.connect(lambda: self.update_list("Category 1"))
        self.button_layout.addWidget(self.button1)

        self.button2 = QPushButton("Show Category 2")
        self.button2.clicked.connect(lambda: self.update_list("Category 2"))
        self.button_layout.addWidget(self.button2)

        self.button3 = QPushButton("Show Category 3")
        self.button3.clicked.connect(lambda: self.update_list("Category 3"))
        self.button_layout.addWidget(self.button3)

        self.button4 = QPushButton("Show Category 4")
        self.button4.clicked.connect(lambda: self.update_list("Category 4"))
        self.button_layout.addWidget(self.button4)
        
        self.button5 = QPushButton("Next")
        self.button5.clicked.connect(self.navigate())
        self.button_layout.addWidget(self.button5)

        # Populate the list with initial items
        self.update_list("Category 1")  # Show initial items

    def navigate(self):
        self.hide()
        

    def update_list(self, category):
        """Update the list based on the selected category"""
        self.list_widget.clear()  # Clear the current items

        # Example items for each category
        if category == "Category 1":
            items = ["Item 1A", "Item 1B", "Item 1C"]
        elif category == "Category 2":
            items = ["Item 2A", "Item 2B", "Item 2C"]
        elif category == "Category 3":
            items = ["Item 3A", "Item 3B", "Item 3C"]
        elif category == "Category 4":
            items = ["Item 4A", "Item 4B", "Item 4C"]

        # Add the items to the list
        self.list_widget.addItems(items)
