from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLineEdit, QPushButton

import pathlib

UI_PATH = "ui/newUserWidget.ui"

EMPTY_FIELD = ''

class AddNewUser(QWidget):
    def __init__(self):
        super().__init__()

        self.__load_ui_file(pathlib.Path(__file__).parent)
        self.__define_widgets()
        self._re_password.textChanged[str].connect(self.__highlight_unmatching_password)
        self._add_user_button.clicked.connect(self.__add_new_user)

        self.show()

    def __load_ui_file(self, path):
        uic.loadUi(path / UI_PATH, self)
    
    def __define_widgets(self) -> None:
        self._name = self.findChild(QLineEdit, "nameLineEdit")
        self._surname = self.findChild(QLineEdit, "surnameLineEdit")
        self._username = self.findChild(QLineEdit, "usernameLineEdit")
        self._password = self.findChild(QLineEdit, "passwordLineEdit")
        self._re_password = self.findChild(QLineEdit, "confirmPasswordLineEdit")
        self._add_user_button = self.findChild(QPushButton, "addUserPushButton")
    
    def __highlight_unmatching_password(self) -> None:
        red_highlight = """QLineEdit {
                        background-color: rgb(255, 255, 255);
                        border-width: 2px;
                        border-style: solid;
                        border-color: none;
                        border-bottom-color: rgb(235, 0, 0);
                        border-radius: 15px;
                    }"""
        green_highlight = """QLineEdit {
                        background-color: rgb(255, 255, 255);
                        border-width: 2px;
                        border-style: solid;
                        border-color: none;
                        border-bottom-color: rgb(0, 255, 8);
                        border-radius: 15px;
                    }"""
        if self._re_password.text() != self._password.text():
            self._re_password.setStyleSheet(red_highlight)
            self._password.setStyleSheet(red_highlight)
        else:
            self._re_password.setStyleSheet(green_highlight)
            self._password.setStyleSheet(green_highlight)

    def __verify_existing_user(self) -> None:
        pass

    def __verify_empty_fields(self) -> bool:
        if self._name.text() == EMPTY_FIELD or \
            self._surname.text() == EMPTY_FIELD or \
                self._username.text() == EMPTY_FIELD or \
                    self._password.text() == EMPTY_FIELD or \
                        self._re_password.text() == EMPTY_FIELD:
            return False
        else:
            return True

    def __add_new_user(self) -> None:
        if self.__verify_empty_fields():
            print("No empty fields")
        else:
            print("Empty fields")
