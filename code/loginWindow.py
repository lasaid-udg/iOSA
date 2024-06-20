from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5.QtWidgets import  QLineEdit, QMessageBox
from PyQt5 import uic
import sys
import pathlib

from mainWindow import MainWindow
from add_new_user import AddNewUser
from log import Log

from doctor import Doctor
from database import ControllDb, MultimediaDb, DatabaseThread, insert_db_thread_event

UI_PATH = "ui/loginWindow.ui"
LOG_IN_EVENT = "User logged"
CONTROLLER_DB_CONNECTION_SUCCESFUL_EVENT = "Controller DB Status: ONLINE"
CONTROLLER_DB_CONNECTION_FAILED_EVENT = "Controller DB Status: OFFLINE"
MULTIMEDIA_DB_CONNECTION_SUCCESFUL_EVENT = "Multimedia DB Status: ONLINE"
MULTIMEDIA_DB_CONNECTION_FAILED_EVENT = "Multimedia DB Status: ONLINE"
FAILED_LOG_IN_EVENT = "Wrong credentiales"


INPUT_FIELD_DISABLED = False


class LogInWindow(QMainWindow):
    def __init__(self):
        super(LogInWindow, self).__init__()

        self.loadUiFile(pathlib.Path(__file__).parent)
        self.defineWidgets()
        self.show()

        self.database_connection_status()

    def loadUiFile(self, path: pathlib.Path) -> None:
        uic.loadUi(path / UI_PATH, self)

    def defineWidgets(self) -> None:
        self.username = self.findChild(QLineEdit, "username")
        self.password = self.findChild(QLineEdit, "password")
        self.loginButton = self.findChild(QPushButton, "loginButton")
        self._sign_in_button = self.findChild(QPushButton, "signInButton")
        self.loginButton.clicked.connect(self.login)
        self._sign_in_button.clicked.connect(self.__sign_in)
        self.username.returnPressed.connect(self.login)
        self.password.returnPressed.connect(self.login)
    
    def __sign_in(self) -> None:
        self._sign_in_wn = AddNewUser()
        self._sign_in_wn.show()

    def login(self) -> None:
        if (self.is_valid_user(self.username.text(), self.password.text())):
            self.insert_event_log(LOG_IN_EVENT)
            controll_db = ControllDb()
            doctor = Doctor()
            db_thread = DatabaseThread(
                target=controll_db.selectUserInformation,
                args=(self.docId,)
            )
            db_thread.start()
            insert_db_thread_event(db_thread.native_id)
            doctor.set_doctor(db_thread.join())
            # self.login_flag = True
            self.window = MainWindow(doctor)
            self.hide()
        else:
            self.insert_event_log(FAILED_LOG_IN_EVENT)
            self.invalid_user_pop_up()
            self.username.clear()
            self.password.clear()

    def is_valid_user(self, user: str, password: str) -> bool:
        try:
            controll_db = ControllDb()
            db_thread = DatabaseThread(
                target=controll_db.selectUserId,
                args=(user,)
            )
            db_thread.start()
            insert_db_thread_event(db_thread.native_id)
            data = db_thread.join()
            self.docId = data[0]
            return (data is not None and data[1] == password)
        except TypeError:
            self.insert_error_log()
            return False

    def invalid_user_pop_up(self) -> None:
        msg = QMessageBox()
        msg.setWindowTitle("Inicio de Sesión Erroneo")
        msg.setText("Usuario y/o Contraseña Invalida.\n\nIntente de nuevo.")
        msg.exec_()

    def database_connection_status(self) -> None:
        controll_db = ControllDb()
        multimedia_db = MultimediaDb()
        if not controll_db.isConnected:
            msg = QMessageBox()
            msg.setWindowTitle("Error de Conexion")
            msg.setText("Error al contectar con la base de datos Controller.\n"
                        + "Contacte al supervisor del sistema.")
            msg.exec_()

            self.set_input_fields_disabled()
            self.insert_event_log(CONTROLLER_DB_CONNECTION_FAILED_EVENT)
        else:
            self.insert_event_log(CONTROLLER_DB_CONNECTION_SUCCESFUL_EVENT)

        if not multimedia_db.is_connected:
            msg = QMessageBox()
            msg.setWindowTitle("Error de Conexion")
            msg.setText("Error al contectar con la base de datos Multimedia.\n"
                        + "Contacte al supervisor del sistema.")
            msg.exec_()

            self.set_input_fields_disabled()
            self.insert_event_log(MULTIMEDIA_DB_CONNECTION_FAILED_EVENT)
        else:
            self.insert_event_log(MULTIMEDIA_DB_CONNECTION_SUCCESFUL_EVENT)

    def set_input_fields_disabled(self) -> None:
        self.loginButton.setEnabled(INPUT_FIELD_DISABLED)
        self.username.setEnabled(INPUT_FIELD_DISABLED)
        self.password.setEnabled(INPUT_FIELD_DISABLED)

    def insert_event_log(self, event: str) -> None:
        log = Log()
        log.insert_log_info(event)
    
    def insert_error_log(self) -> None:
        log = Log()
        log.insert_log_error()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    logInWindow = QMainWindow()
    ui = LogInWindow()
    sys.exit(app.exec_())
