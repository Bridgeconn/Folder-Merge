import sys
import os
import time
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog, QMessageBox, QProgressDialog, QLineEdit, QLabel
from PyQt6.QtCore import QThread, pyqtSignal, Qt
import merge_all_books

# Thread class to handle folder merging
class FolderMergerThread(QThread):
    update_progress = pyqtSignal(int)
    task_completed = pyqtSignal(str)

    def __init__(self, base_dir, sub_folder, output_dir, username):
        super().__init__()
        self.base_dir = base_dir
        self.sub_folder = sub_folder
        self.output_dir = output_dir
        self.username = username

    def run(self):
        try:
            results = merge_all_books.merge_folders(self.base_dir, self.sub_folder, self.output_dir)
            merge_all_books.merge_json_files(self.base_dir, self.output_dir, self.username, "metadata.json")

            # Simulate progress update
            for i in range(1, 101):
                time.sleep(0.05)
                self.update_progress.emit(i)
                
            self.task_completed.emit("Folders and JSON merged successfully!\nThe merged folders can be found in the Output folder within the Source directory.\nReports are written in report.txt")
        
        except Exception as e:
            self.task_completed.emit(f"An error occurred: {e}")

# Thread class to handle conversion
class FileConversionThread(QThread):
    update_progress = pyqtSignal(int)
    task_completed = pyqtSignal(str)

    def __init__(self, output_dir):
        super().__init__()
        self.output_dir = output_dir

    def run(self):
        try:
            converted_result = merge_all_books.convert_to_mp3(self.output_dir)
            for i in range(1, 101):
                time.sleep(0.05)
                self.update_progress.emit(i)
            self.task_completed.emit("Files converted to MP3 successfully!")
        
        except Exception as e:
            self.task_completed.emit(f"An error occurred during conversion: {e}")

# Main application class
class FolderMergeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.source_folder = None  

    def initUI(self):
        # Create widgets
        self.username_label = QLabel("Username: ")
        self.username_input = QLineEdit(self)
        self.username_input.setText("all.pm")  # Set default value

        self.source_button = QPushButton('Source', self)
        self.merge_button = QPushButton('Merge', self)
        self.convert_button = QPushButton('Convert', self)

        # Set styles and sizes for the buttons
        self.source_button.setStyleSheet("background-color: lightblue;color: black; border: 2px solid transparent; border-radius: 5px;")
        self.merge_button.setStyleSheet("background-color: lightgreen; color: black;border: 2px solid transparent; border-radius: 5px;")
        self.convert_button.setStyleSheet("background-color: lightcoral;color: black; border: 2px solid transparent; border-radius: 5px;")

        self.source_button.setFixedSize(120, 30)
        self.merge_button.setFixedSize(120, 30)
        self.convert_button.setFixedSize(120, 30)

        # Connect button clicks to functions
        self.source_button.clicked.connect(self.select_source_folder)
        self.merge_button.clicked.connect(self.merge_folders)
        self.convert_button.clicked.connect(self.convert_files)

        # Create a horizontal layout for the username label and input
        username_layout = QHBoxLayout()
        username_layout.addWidget(self.username_label)
        username_layout.addWidget(self.username_input)

        # Layout setup
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.source_button)
        button_layout.addWidget(self.merge_button)
        button_layout.addWidget(self.convert_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(username_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.setWindowTitle('Folder Merge')
        self.setGeometry(500, 300, 400, 200)
        self.show()

    def select_source_folder(self):
        self.source_folder = QFileDialog.getExistingDirectory(self, 'Select Source Folder', os.path.expanduser("~"))
        if self.source_folder:
            msg = QMessageBox()
            msg.setWindowTitle("Folder Selected")
            msg.setText(f"Selected source folder: {self.source_folder}")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        else:
            print("No folder selected.")

    def merge_folders(self):
        if not self.source_folder:
            QMessageBox.warning(self, 'Error', 'Please select a source folder first.')
            return  

        username = self.username_input.text().strip()
        if not username:
            QMessageBox.warning(self, ' enter a username!!!.')
            return

        base_dir = self.source_folder
        subfolder_name = 'ingredients'
        output_dir = os.path.join(base_dir, 'output')

        if not os.path.exists(base_dir):
            QMessageBox.warning(self, 'Error', f'The selected source folder does not exist: {base_dir}')
            return

        # Setup and show the progress dialog
        self.progress_dialog = QProgressDialog("Merging Folders...", "Cancel", 0, 100, self)
        self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress_dialog.setAutoClose(True)
        self.progress_dialog.setValue(0)
        self.progress_dialog.show()

        # Start the folder merge thread
        self.merge_thread = FolderMergerThread(base_dir, subfolder_name, output_dir, username)
        self.merge_thread.update_progress.connect(self.progress_dialog.setValue)
        self.merge_thread.task_completed.connect(self.on_task_completed)
        self.merge_thread.start()
    
    def convert_files(self):
        if not self.source_folder:
            QMessageBox.warning(self, 'Error', 'Please select a source folder first')
            return 
        
        output_dir = os.path.join(self.source_folder, 'output')
        if not os.path.exists(output_dir):
            QMessageBox.warning(self, 'Error', 'The output directory does not exist')
            return

        self.progress_dialog = QProgressDialog("Converting files to MP3...", "Cancel", 0, 0, self)
        self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress_dialog.setAutoClose(True)
        self.progress_dialog.setValue(0)
        self.progress_dialog.show()

        self.progress_dialog.setStyleSheet("QProgressBar {min-height: 0px; max-height: 0px;}")

        self.convert_thread = FileConversionThread(output_dir)
        self.convert_thread.update_progress.connect(self.progress_dialog.setValue)
        self.convert_thread.task_completed.connect(self.on_task_completed)
        self.convert_thread.start()

    def on_task_completed(self, message):
        self.progress_dialog.close()
        QMessageBox.information(self, 'Success', message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FolderMergeApp()
    sys.exit(app.exec())
