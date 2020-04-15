import sys
import os
import time
import asyncio
import platform
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt, QProcess
from lined_text_editor import LineTextWidget
from lined_text_editor import NumberBar

# Rename tab code
# self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("self", "Tab 1"))
increment = 0
class MainEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.editors = {}
        self.terminals = []

    def initUI(self):
        self.setWindowTitle('Hézuò')
        self.setObjectName('MainEditorWindow')
        self.setGeometry(300, 300, 1200, 800)

        self.central_widget = QWidget(self)
        self.central_widget.setObjectName('CentralWidget')
        self.setCentralWidget(self.central_widget)

        self.central_horizontal_layout = QHBoxLayout(self.central_widget)
        self.central_horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.central_horizontal_layout.setSpacing(0)
        self.central_horizontal_layout.setObjectName('CentralHorizontalLayout')

        self.central_splitter = QSplitter(self.central_widget)
        self.central_splitter.setOrientation(Qt.Horizontal)
        self.central_splitter.setObjectName('CentralSplitter')

        self.file_scroll_area = QScrollArea(self.central_splitter)
        self.file_scroll_area.setWidgetResizable(True)
        self.file_scroll_area.setObjectName('FileScrollArea')

        self.file_area_widget = QWidget()
        self.file_area_widget.setGeometry(QtCore.QRect(0, 0, 99, 779))
        self.file_area_widget.setObjectName('FileAreaWidget')

        self.file_scroll_area.setWidget(self.file_area_widget)

        self.editor_splitter = QSplitter(self.central_splitter)
        self.editor_splitter.setOrientation(Qt.Vertical)
        self.editor_splitter.setObjectName('EditorSplitter')

        self.editor_tabs = QTabWidget(self.editor_splitter)
        self.editor_tabs.setObjectName('EditorTabs')
        self.editor_tabs.setTabsClosable(True)
        self.editor_tabs.setMovable(True)
        self.editor_tabs.tabCloseRequested.connect(self.remove_tab)

        welcome_label = QLabel()
        welcome_label.setText('Hello!')

        self.editor_tabs.addTab(welcome_label, 'Welcome')

        self.terminal_tabs = QTabWidget(self.editor_splitter)
        self.terminal_tabs.setObjectName('TerminalTabs')
        self.terminal_tabs.setTabsClosable(True)
        self.terminal_tabs.setMovable(True)

        new_terminal_button = QPushButton('+')
        new_terminal_button.clicked.connect(self.attach_new_terminal)

        self.central_horizontal_layout.addWidget(self.central_splitter)
        self.setCentralWidget(self.central_widget)

        self.initMenuBar()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.initStatusBar()

    def initMenuBar(self):
        self.menubar = self.menuBar()

        self.file_menu = self.menubar.addMenu('File')
        self.file_menu.setObjectName('FileMenu')

        self.new_file_action = QAction('New File', self)
        self.new_file_action.setShortcut('Ctrl + N')
        self.new_file_action.triggered.connect(self.create_new_file)

        self.new_window_action = QAction('New Window', self)
        self.new_window_action.setShortcut('Ctrl + Shift + N')

        self.open_file_action = QAction('Open File', self)
        self.open_file_action.setShortcut('Ctrl + O')
        self.open_file_action.triggered.connect(self.open_file)

        self.open_folder_action = QAction('Open Folder', self)
        self.open_folder_action.triggered.connect(self.open_folder)

        self.open_recent_action = QMenu('Open Recent', self)

        self.save_file_action = QAction('Save', self)
        self.save_file_action.setShortcut('Ctrl + S')
        self.save_file_action.triggered.connect(self.save_file)

        self.save_file_as_action = QAction('Save As', self)
        self.save_file_action.setShortcut('Ctrl + Shift + S')
        self.save_file_as_action.triggered.connect(self.save_file_as)

        self.save_all_files_action = QAction('Save All', self)

        self.view_preferences_action = QMenu('Preferences', self)

        self.file_menu.addAction(self.new_file_action)
        self.file_menu.addAction(self.new_window_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.open_file_action)
        self.file_menu.addAction(self.open_folder_action)
        self.file_menu.addMenu(self.open_recent_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.save_file_action)
        self.file_menu.addAction(self.save_file_as_action)
        self.file_menu.addAction(self.save_all_files_action)
        self.file_menu.addSeparator()
        self.file_menu.addMenu(self.view_preferences_action)

        self.edit_menu = self.menubar.addMenu('Edit')
        self.edit_menu.setObjectName('EditMenu')

        self.undo_action = QAction('Undo', self)
        self.undo_action.setShortcut('Ctrl + Z')

        self.redo_action = QAction('Redo', self)
        self.redo_action.setShortcut('Ctrl + Y')

        self.cut_action = QAction('Cut', self)
        self.cut_action.setShortcut('Ctrl + X')
       
        self.copy_action = QAction('Copy', self)
        self.copy_action.setShortcut('Ctrl + C')

        self.paste_action = QAction('Paste', self)
        self.paste_action.setShortcut('Ctrl + V')

        self.find_action = QAction('Find', self)
        self.find_action.setShortcut('Ctrl + F')

        self.edit_menu.addAction(self.undo_action)
        self.edit_menu.addAction(self.redo_action)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.cut_action)
        self.edit_menu.addAction(self.copy_action)
        self.edit_menu.addAction(self.paste_action)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.find_action)

        self.selection_menu = self.menubar.addMenu('Selection')
        self.selection_menu.setObjectName('SelectionMenu')

        self.select_all_action = QAction('Select All', self)
        self.select_all_action.setShortcut('Ctrl + A')

        self.selection_menu.addAction(self.select_all_action)

        self.view_menu = self.menubar.addMenu('View')
        self.view_menu.setObjectName('ViewMenu')

        self.go_menu = self.menubar.addMenu('Go')
        self.go_menu.setObjectName('GoMenu')

        self.terminal_menu = self.menubar.addMenu('Terminal')
        self.terminal_menu.setObjectName('TerminalMenu')

        self.new_terminal_action =  QAction('New Terminal', self)
        self.new_terminal_action.setShortcut('Ctrl + Shift + `')
        self.new_terminal_action.triggered.connect(self.attach_new_terminal)

        self.terminal_menu.addAction(self.new_terminal_action)

        self.setMenuBar(self.menubar)

    def initStatusBar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.cursor_pos_label = QLabel("test")
        self.status_bar.addPermanentWidget(self.cursor_pos_label)

    def attach_new_terminal(self):
        """
        if (sys.platform == 'linux1') or (sys.platform == 'linux2') or (sys.platform == 'darwin'):
            terminal_process = QProcess(self)
            terminal_window = QWidget(self)
            terminal_process.start('xterm',['-into', str(int(terminal_window.winId()))])
            self.terminals.append(terminal_process)
            self.terminal_tabs.addTab(terminal_window, 'Terminal')
        elif sys.platform == 'win32':
            os.system("cmd")
        else:
            terminal_process = QProcess(self)
            terminal_window = QWidget(self)
            terminal_process.start('xterm',['-into', str(int(terminal_window.winId()))])
            self.terminals.append(terminal_process)
            self.terminal_tabs.addTab(terminal_window, 'Terminal')
            """
        terminal_process = QProcess(self)
        terminal_window = QWidget(self)
        terminal_process.start('xterm',['-into', str(int(terminal_window.winId()))])
        self.terminals.append(terminal_process)
        self.terminal_tabs.addTab(terminal_window, 'Terminal')

    def create_editor(self, file_contents, file_path):
        text_editor = LineTextWidget(self.cursor_pos_label, self)
        text_editor.getTextEdit().setText(file_contents)

        title = file_path.rsplit('/', 1)[-1]
        text_editor.setWindowTitle(title)

        self.editors[title] = [text_editor, file_path, False, True]
        self.editor_tabs.addTab(text_editor, title)

    def remove_editor(self):
        print('remove')

    def create_new_file(self):
        global increment
        increment += 1
        self.create_editor('', 'New File ' + str(increment))
        return increment

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

    def save_file_as(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save File As', '', 'All Files (*);;Text Files (*.txt)', options=options)

        if file_name:
            with open(file_name, 'w+') as file:
                current_tab = self.editor_tabs.currentWidget().windowTitle()

                if current_tab[:8] == 'New File':
                    text_editor = LineTextWidget(self)
                    title = file_name.rsplit('/', 1)[-1]
                    text_editor.setWindowTitle(title)
                    self.editors[title] = [text_editor, file_name, False, True]

                text = (self.editors[current_tab][0].getTextEdit().toPlainText())

                file.write(text)
                file.close()

    def save_file(self):
        current_tab = self.editor_tabs.currentWidget().windowTitle()
        if current_tab[:8] == 'New File':
            self.save_file_as()
        else:
            file = open(self.editors[current_tab][1],'w')
            text = self.editors[current_tab][0].getTextEdit().toPlainText()
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