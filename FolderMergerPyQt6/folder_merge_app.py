import sys
import os


from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QFileDialog, QMessageBox
import merge_luk
class FolderMergeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.source_folder = None  

    def initUI(self):
        self.source_button = QPushButton('Source', self)
        self.merge_button = QPushButton('Merge', self)


        self.source_button.setStyleSheet("background-color: lightblue; ; border: 2px solid transparent; border-radius: 5px;")
        self.merge_button.setStyleSheet("background-color: lightgreen; ; border: 2px solid transparent; border-radius: 5px;")

        self.source_button.setFixedSize(150, 30)  
        self.merge_button.setFixedSize(150, 30)
        
        
        self.source_button.clicked.connect(self.select_source_folder)
        self.merge_button.clicked.connect(self.merge_folders)



        hbox = QHBoxLayout()
        hbox.addWidget(self.source_button)
        hbox.addWidget(self.merge_button)

        self.setLayout(hbox)
        self.setWindowTitle('Folder Merge')
        self.setGeometry(500, 300, 400, 200)
        self.show()

    def select_source_folder(self):
        print("Opening folder selection dialog...") 
        self.source_folder = QFileDialog.getExistingDirectory(self, 'Select Source Folder', os.path.expanduser("~"))
        if self.source_folder:
            print(f"Selected source folder: {self.source_folder}")  
            msg = QMessageBox()
            msg.setWindowTitle("Folder Selected")
            msg.setText(f"Selected source folder: {self.source_folder}")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

        else:
            print("No folder selected.")  

    def merge_folders(self):
        QMessageBox.information(self, 'Success', 'Started the merging process')
        if not self.source_folder:
            QMessageBox.warning(self, 'Error', 'Please select a source folder first.')
            return  
        base_dir = self.source_folder  
        
        base_dir = self.source_folder
        subfolder_name = 'ingredients/LUK'
        output_dir = os.path.join(base_dir, 'output_luk')

        if not os.path.exists(base_dir):
            QMessageBox.warning(self, 'Error', f'The selected source folder does not exist: {base_dir}')
            return

        try:
      
            results=merge_luk.merge_folders(base_dir, subfolder_name, output_dir)
            
            QMessageBox.information(self, 'Success', 'Folders merged successfully!\nThe merged folders can be found in the Output folder within the Source directory.\nReports are written in report.txt')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred during merging: {e}')
            error_message = f"An error occurred during merging: {str(e)}\n"
           

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FolderMergeApp()
    sys.exit(app.exec())
