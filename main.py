import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import json


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
        

import sys
import time
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.statusBar().showMessage('Ready')
        
        self.setGeometry(300, 300, 900, 600)
        self.setWindowTitle('Hézuò')

        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        edit = menubar.addMenu("Edit")
        view = menubar.addMenu("View")
        help = menubar.addMenu("Help")

        new_file_action = QAction("New File")
        new_file_action.setShortcut("Ctrl+N")

        file_menu.addAction(new_file_action)

        self.setMenuBar(menubar)

        self.text_input = QTextEdit(self)
        self.setCentralWidget(self.text_input)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())