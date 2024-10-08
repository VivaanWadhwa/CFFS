from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMainWindow, QHBoxLayout

class UploadPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Upload Data")

        # Set up the main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Set background color and style
        self.central_widget.setStyleSheet("""
            QWidget {
                background-color: #2d3436;
                color: white;
            }
            QLabel {
                font-size: 20px;
                font-family: 'Arial', sans-serif;
                padding: 20px;
            }
            QPushButton {
                background-color: #0984e3;
                color: white;
                font-size: 18px;
                font-family: 'Arial', sans-serif;
                border-radius: 10px;
                padding: 10px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #74b9ff;
                color: black;
            }
        """)

        # Add label to guide the user
        self.label = QLabel("Please upload a folder or a ZIP file to continue.")
        self.label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.label)

        # Create a layout for the buttons (folder and zip selection)
        self.button_layout = QHBoxLayout()
        self.main_layout.addLayout(self.button_layout)

        # Button for selecting a folder
        self.folder_button = QPushButton("Select Folder")
        self.folder_button.clicked.connect(self.select_folder)
        self.button_layout.addWidget(self.folder_button)

        # Button for selecting a ZIP file
        self.zip_button = QPushButton("Select ZIP File")
        self.zip_button.clicked.connect(self.select_zip_file)
        self.button_layout.addWidget(self.zip_button)

        # Create a layout for the back button
        self.back_button_layout = QHBoxLayout()
        self.main_layout.addLayout(self.back_button_layout)

        # Back button
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)
        self.back_button_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)

        # Label to display the selected path
        self.path_label = QLabel("")
        self.path_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.path_label)

        # Maximize window on startup
        self.showMaximized()

    def select_folder(self):
        """Open file dialog to select a folder"""
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.path_label.setText(f"Selected Folder: {folder_path}")
            self.navigate_to_next_page(folder_path)

    def select_zip_file(self):
        """Open file dialog to select a ZIP file"""
        zip_file, _ = QFileDialog.getOpenFileName(self, "Select ZIP File", "", "ZIP Files (*.zip)")
        if zip_file:
            self.path_label.setText(f"Selected ZIP File: {zip_file}")
            self.navigate_to_next_page(zip_file)
    
    def navigate_to_next_page(self, selected_path):
        """Navigate to 1st step page"""
        self.hide()  # Hide the current page
        from app.views.overView import overviewPage
        self.overviewPage = overviewPage(selected_path)
        self.overviewPage.show()
            
    def go_back(self):
        self.hide()  # Hide the current page
        from app.views.MainWindow import MainWindow
        self.main_window = MainWindow()  # Recreate the MainWindow
        self.main_window.show()  # Show the MainWindow