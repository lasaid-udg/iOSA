from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPlainTextEdit

import pathlib

UI_PATH = "ui/detailsWidget.ui"


class DetailsWidget(QWidget):
    def __init__(self):
        super(DetailsWidget, self).__init__()
        self.load_ui_file(pathlib.Path(__file__).parent)
        self.define_widget()

    def load_ui_file(self, path):
        uic.loadUi(path / UI_PATH, self)

    def define_widget(self):
        self.details_field = self.findChild(QPlainTextEdit, "details_text_edit")
        
    def add_detail(self, detail):
        self.details_field.appendPlainText(detail)

    def show_details_window(self):
        self.show()
