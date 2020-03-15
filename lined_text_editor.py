import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.Qt import QFrame, QWidget, QTextEdit, QHBoxLayout, QPainter

class NumberBar(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.edit = None
        self.highest_line = 0

    def setTextEdit(self, edit):
        self.edit = edit

    def update(self, *args):
        width = self.fontMetrics().width(str(self.highest_line)) + 25

        if self.width() != width:
            self.setFixedWidth(width)

        QWidget.update(self, *args)

    def paintEvent(self, event):
        contents_y = self.edit.verticalScrollBar().value()
        page_bottom = contents_y + self.edit.viewport().height()
        font_metrics = self.fontMetrics()
        current_block = self.edit.document().findBlock(self.edit.textCursor().position())

        painter = QPainter(self)

        line_count = 0
        block = self.edit.document().begin()

        while block.isValid():
            line_count += 1

            position = self.edit.document().documentLayout().blockBoundingRect(block).topLeft()

            if position.y() > page_bottom:
                break

            bold = False
            if block == current_block:
                bold = True
                font = painter.font()
                font.setBold(True)
                painter.setFont(font)

            painter.drawText(self.width() - font_metrics.width(str(line_count)) - 24, round(position.y()) - contents_y + font_metrics.ascent(), str(line_count))

            if bold:
                font = painter.font()
                font.setBold(False)
                painter.setFont(font)

            block = block.next()

        self.highest_line = line_count
        painter.end()

        QWidget.paintEvent(self, event)

class LineTextWidget(QFrame):
    def __init__(self, *args):
        QFrame.__init__(self, *args)

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)

        self.edit = QTextEdit()
        self.edit.setFrameStyle(QFrame.NoFrame)
        self.edit.setAcceptRichText(False)

        self.number_bar = NumberBar()
        self.number_bar.setTextEdit(self.edit)

        hbox = QHBoxLayout(self)
        hbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(self.number_bar)
        hbox.addWidget(self.edit)

        self.edit.installEventFilter(self)
        self.edit.viewport().installEventFilter(self)

    def eventFilter(self, object, event):
        if object in (self.edit, self.edit.viewport()):
            self.number_bar.update()
            return False
        
        return QFrame.eventFilter(object, event)

    def getTextEdit(self):
        return self.edit