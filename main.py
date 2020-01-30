import sys
import time
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

class ProtocolMessage():
    def __init__(self):
        self.cmd = ''
        self.start_row = 0
        self.end_row = 0
        self.start_col = 0
        self.end_col = 0
        self.string = 0

    def __str__(self):
        return f'{{"p":"{self.cmd}","r":"{self.start_row}","t":"{self.end_row}","c":"{self.start_col}","u":"{self.end_row}","s":"{self.string}"}}'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.statusBar().showMessage('Ready')
        
        self.setGeometry(300, 300, 900, 600)
        self.setWindowTitle('Hézuò')

        self.initMenuBar()

        self.text_input = QTextEdit(self)
        self.setCentralWidget(self.text_input)

    def initMenuBar(self):
        self.menubar = self.menuBar()

        file_menu = self.menubar.addMenu('File')
        edit_menu = self.menubar.addMenu('Edit')
        view_menu = self.menubar.addMenu('View')

        new_file_action = QAction('New File', self)
        new_file_action.setShortcut('Ctrl+N')
        new_file_action.triggered.connect(self.test)

        open_file_action = QAction('Open file', self)
        open_file_action.setShortcut('Ctrl+O')

        open_recents_action = QMenu('Open Recent', self)

        edit_preferences_action = QMenu('Preferences', self)

        file_menu.addAction(new_file_action)
        file_menu.addAction(open_file_action)
        file_menu.addSeparator()
        file_menu.addMenu(open_recents_action)
        file_menu.addMenu(edit_preferences_action)

        self.setMenuBar(self.menubar)

    def test(self):
        print('test')

    
if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())