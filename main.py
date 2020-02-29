import sys
import os
import time
import asyncio
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QProcess
from lined_text_editor import LineTextWidget

class MainEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.event_loop = asyncio.get_event_loop()
        self.editors = {}
        self.terminals = []

    def initUI(self):
        self.main_window = QWidget(self)
        self.setCentralWidget(self.main_window)

        self.layout = QGridLayout()
        self.main_window.setLayout(self.layout)

        self.editor_tabs = QTabWidget()
        self.editor_tabs.setTabsClosable(True)
        self.editor_tabs.setMovable(True)
        self.editor_tabs.tabCloseRequested.connect(self.remove_tab)

        welcome_label = QLabel()
        welcome_label.setText('Hello!')

        self.editor_tabs.addTab(welcome_label, 'Welcome')

        self.terminal_tabs = QTabWidget()
        self.terminal_tabs.setTabsClosable(True)
        self.terminal_tabs.setMovable(True)

        new_terminal_button = QPushButton('+')
        new_terminal_button.clicked.connect(self.attach_new_terminal)

        self.editor_tabs.setCornerWidget(new_terminal_button)
        self.terminal_tabs.setCornerWidget(new_terminal_button)

        self.layout.addWidget(self.editor_tabs)
        self.layout.addWidget(self.terminal_tabs)

        self.statusBar().showMessage('Ready')

        self.setGeometry(300, 300, 900, 600)
        self.setWindowTitle('Hézuò')

        self.initMenuBar()

    def initMenuBar(self):
        self.menubar = self.menuBar()

        file_menu = self.menubar.addMenu('File')
        edit_menu = self.menubar.addMenu('Edit')
        view_menu = self.menubar.addMenu('View')
        setting_menu = self.menubar.addMenu('Setting')

        new_file_action = QAction('New File', self)
        new_file_action.setShortcut('Ctrl + N')
        new_file_action.triggered.connect(self.create_new_file)

        open_file_action = QAction('Open File', self)
        open_file_action.setShortcut('Ctrl + O')
        open_file_action.triggered.connect(self.open_file)

        open_folder_action = QAction('Open Folder', self)
        open_folder_action.triggered.connect(self.open_folder)

        open_recents_action = QMenu('Open Recent', self)

        edit_preferences_action = QMenu('Preferences', self)

        save_file_action = QAction('Save', self)
        save_file_action.setShortcut('Ctrl + S')
        save_file_action.triggered.connect(self.save_file)

        save_as_file_action = QAction('Save as...', self)
        save_as_file_action.setShortcut('Ctrl + Shift + S')
        save_as_file_action.triggered.connect(self.save_file_as)

        save_all_files_action = QAction('Save all', self)

        file_menu.addAction(new_file_action)
        file_menu.addSeparator()
        file_menu.addAction(open_file_action)
        file_menu.addMenu(open_recents_action)
        file_menu.addMenu(edit_preferences_action)
        file_menu.addSeparator()
        file_menu.addAction(save_file_action)
        file_menu.addAction(save_as_file_action)
        file_menu.addAction(save_all_files_action)

        self.setMenuBar(self.menubar)

    def attach_new_terminal(self):
        terminal_process = QProcess(self)
        terminal_window = QWidget(self)
        terminal_process.start('xterm',['-into', str(int(terminal_window.winId()))])

        self.terminals.append(terminal_process)
        self.terminal_tabs.addTab(terminal_window, 'Terminal')

    def create_editor(self, file_contents, file_path):
        text_editor = LineTextWidget(self)
        text_editor.getTextEdit().setText(file_contents)

        title = file_path.rsplit('/', 1)[-1]
        text_editor.setWindowTitle(title)

        self.editors[title] = [text_editor, file_path, False, True]
        self.editor_tabs.addTab(text_editor, title)

    def remove_editor(self):
        print('remove')

    def create_new_file(self):
        self.create_editor('', 'New File')

    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'All Files (*);;Python Files (*.py)', options=options)

        if file_name:
            if os.path.exists(file_name):
                with open(file_name, 'r') as file:
                    file_contents = file.readlines()

                self.create_editor(''.join(file_contents), file_name)
            else:
                print('Error saving file.')

    def open_folder(self):
        print('test')

    def save_file(self):
        current_tab = self.editor_tabs.currentWidget().windowTitle()
        file = open(self.editors[current_tab][1],'w')
        text = self.editors[current_tab][0].getTextEdit().toPlainText()

        file.write(text)
        file.close()

    def save_file_as(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save File As', '', 'All Files (*);;Text Files (*.txt)', options=options)

        if file_name:
            with open(file_name, 'w+') as file:
                current_tab = self.editor_tabs.currentWidget().windowTitle()

            if current_tab == 'New File':
                text_editor = LineTextWidget(self)
                title = file_name.rsplit('/', 1)[-1]
                text_editor.setWindowTitle(title)
                self.editors[title] = [text_editor, file_name, False, True]

            text = (self.editors[current_tab][0].getTextEdit().toPlainText())

            file.write(text)
            file.close()

    def save_all_files(self):
        print('test')

    def remove_tab(self, index):
        widget = self.editor_tabs.widget(index)

        if widget is not None:
            widget.deleteLater()

        self.editor_tabs.removeTab(index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    main_window = MainEditorWindow()
    main_window.show()

    sys.exit(app.exec_())