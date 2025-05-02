import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QFileDialog
from PySide6.QtGui import QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notepad")
        self.editor = QTextEdit()
        self.setCentralWidget(self.editor)
        file_menu = self.menuBar().addMenu("File")
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)
        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self)
        if path:
            with open(path, 'r') as f:
                self.editor.setPlainText(f.read())

    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(self, filter="Text Files (*.txt)")
        if path:
            with open(path, 'w') as f:
                f.write(self.editor.toPlainText())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

