from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLineEdit, QPushButton
from PyQt5.QtWidgets import QMessageBox

import pathlib

from database import ControllDb, MultimediaDb, DatabaseThread, insert_db_thread_event

UI_PATH = "ui/newUserWidget.ui"

EMPTY_FIELD = ''
INVALID_FIELD_MSG_TITLE = "Invalid Field"
INVALID_FIELD_MSG = "Invalid data input.\nPlease verify the input data."
UNMATCHING_PASSWORDS_MSG_TITLE = "Unmatching passwords"
UNMATCHING_PASSWORDS_MSG = "The passwords do not match\nPlease verify them."
EXISTING_USER_MSG_TITLE = "Existing User"
EXISTING_USER_MSG = "The user already exist.\nPlease chose another."


class AddNewUser(QWidget):
    def __init__(self):
        super().__init__()

        self.__load_ui_file(pathlib.Path(__file__).parent)
        self.__define_widgets()
        self._password.textChanged[str].connect(self.__highlight_unmatching_password)
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

    def __add_new_user(self) -> None:
        if self.__verify_empty_fields():
            if self.__verify_matching_password():
                if self.__verify_existing_user():
                    print("All good!!!")
                else:
                    self.__existing_user_msg()
            else:
                self.__unmatching_password_msg()
        else:
            self.__highlight_empty_fields()
            self.__invalid_field_msg()

    def __verify_matching_password(self) -> bool:
        if self._password.text() == "" or \
                self._re_password.text() == "" or \
                    self._re_password.text() != self._password.text():
            return False
        else:
            return True

    def __verify_empty_fields(self) -> bool:
        if self._name.text() == EMPTY_FIELD or \
            self._surname.text() == EMPTY_FIELD or \
                self._username.text() == EMPTY_FIELD or \
                    self._password.text() == EMPTY_FIELD or \
                        self._re_password.text() == EMPTY_FIELD:
            return False
        else:
            return True

    def __verify_existing_user(self) -> bool:
        controll_db = ControllDb()
        db_thread = DatabaseThread(
            target=controll_db.get_username,
            args=(self._username.text(),)
        )
        db_thread.start()
        insert_db_thread_event(db_thread.native_id)
        data = db_thread.join()

        if data is None:
            return True
        else:
            return False

    def __highlight_unmatching_password(self) -> None:
        if self._password.text() == "" or \
                self._re_password.text() == "" or \
                    self._re_password.text() != self._password.text():
            self.__red_highlight_field(self._password)
            self.__red_highlight_field(self._re_password)
        else:
            self.__green_highlight_field(self._password)
            self.__green_highlight_field(self._re_password)

    def __highlight_empty_fields(self) -> None:
        if self._name.text() == EMPTY_FIELD:
            self.__red_highlight_field(self._name)
        else:
            self.__green_highlight_field(self._name)

        if self._surname.text() == EMPTY_FIELD:
            self.__red_highlight_field(self._surname)
        else:
            self.__green_highlight_field(self._surname)
                
        if self._username.text() == EMPTY_FIELD:
            self.__red_highlight_field(self._username)
        else:
            self.__green_highlight_field(self._username)
                    
        if self._password.text() == EMPTY_FIELD:
            self.__red_highlight_field(self._password)
        else:
            self.__green_highlight_field(self._password)
                        
        if self._re_password.text() == EMPTY_FIELD:
            self.__red_highlight_field(self._re_password)
        else:
            self.__green_highlight_field(self._re_password)
    
    def __red_highlight_field(self, field_name) -> None:
        red_highlight = """QLineEdit {
                        background-color: rgb(255, 255, 255);
                        border-width: 2px;
                        border-style: solid;
                        border-color: none;
                        border-bottom-color: rgb(235, 0, 0);
                        border-radius: 15px;
                    }"""
        field_name.setStyleSheet(red_highlight)
    
    def __green_highlight_field(self, field_name) -> None:
        green_highlight = """QLineEdit {
                        background-color: rgb(255, 255, 255);
                        border-width: 2px;
                        border-style: solid;
                        border-color: none;
                        border-bottom-color: rgb(0, 255, 8);
                        border-radius: 15px;
                    }"""
        field_name.setStyleSheet(green_highlight)

    def __insert_new_user(self) -> None:
        controll_db = ControllDb()
        db_thread = DatabaseThread(
            target=controll_db.get_username,
            args=(self._username.text(),)
        )
        db_thread.start()
        insert_db_thread_event(db_thread.native_id)
        data = db_thread.join()

    def __invalid_field_msg(self) -> None:
        msg = QMessageBox()
        msg.setWindowTitle(INVALID_FIELD_MSG_TITLE)
        msg.setText(INVALID_FIELD_MSG)
        msg.exec_()
    
    def __unmatching_password_msg(self) -> None:
        msg = QMessageBox()
        msg.setWindowTitle(UNMATCHING_PASSWORDS_MSG_TITLE)
        msg.setText(UNMATCHING_PASSWORDS_MSG)
        msg.exec_()

    def __existing_user_msg(self) -> None:
        msg = QMessageBox()
        msg.setWindowTitle(EXISTING_USER_MSG_TITLE)
        msg.setText(EXISTING_USER_MSG)
        msg.exec_()
