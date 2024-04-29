from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QFileDialog, QWidget
from PyQt5.QtWidgets import QPushButton, QSlider, QMessageBox
from PyQt5 import uic

import pathlib
from shutil import copyfile, SameFileError
import os
from pydub import AudioSegment

from log import Log
from database import MultimediaDb, DatabaseThread, insert_db_thread_event

UI_PATH = "ui/videoWidget.ui"
VIDEO_PATH = r"multimedia\videos"
VIDEO_DB_PATH = r"multimedia\\videos"
AUDIO_PATH = r"multimedia\audios"
AUDIO_DB_PATH = r"multimedia\\audios"
VIDEO_EXTENSION = "mp4"
AUDIO_EXTENSION = "wav"
VIDEO_EXTENSION_EXPORT = ".mp4"
AUDIO_EXTENSION_EXPORT = ".wav"
AUDIO_BITRATE = "320k"
BLANK = ''


class VideoConvert(QWidget):
    def __init__(self, patient, is_edit):
        super(VideoConvert, self).__init__()
        self.is_edit = is_edit
        self._patient = patient
        self.path_video = BLANK
        self.path_dst = BLANK
        self.edit_flag = False

        self.__loadUiFile(pathlib.Path(__file__).parent)
        self.__os_dir()
        self.__define_widgets()
        self.__define_buttons()

        self.show()

    def __loadUiFile(self, path):
        uic.loadUi(path / UI_PATH, self)

    def __define_widgets(self):
        # QPushButton button
        self.select_video_button = self.findChild(
            QPushButton, "selectVideoButton")
        self.play_button = self.findChild(QPushButton, "playPushButton")
        self.next_page_button = self.findChild(QPushButton, "nextPageButton")
        self. previous_page_button = self.findChild(
            QPushButton, "previousPageButton")
        # QSlider slider
        self.video_progress_bar = self.findChild(
            QSlider, "videoProgressBarSlider")
        # QVideoWidget widget
        self.video_widget = self.findChild(QVideoWidget, "videoVideoWidget")

    def __define_buttons(self):
        self.previous_page_button.hide()
        self.select_video_button.clicked.connect(self.get_video_path)
        self.next_page_button.clicked.connect(self.save_or_update_video)
        if self.is_edit:
            self.next_page_button.setText("Guardar")

    def get_video_path(self):
        self.path_video = QFileDialog.getOpenFileName(self, "Seleccionar Video",
                                                      str(pathlib.Path().absolute()),
                                                      "MP4 Files (*.mp4)")

        if self.path_video[0] != "":
            # print("Video Selected: " + self.path_video[0])

            self.start_video_convertion()
        else:
            pass

    def start_video_convertion(self):
        try:
            self.open_video()
            self.view_video()
        except:
            log = Log()
            log.insert_log_error()
            self.error_on_open_video()

        # Copy video and convert it to mp3
        # self.copy_video()

    def open_video(self):
        # print("*** OPENNING VIDEO ***")
        print(self.path_video[0])
        self.video = AudioSegment.from_file(
            self.path_video[0], format=VIDEO_EXTENSION)
        self.video_total_length = len(self.video)

    def convert_video_to_audio(self, video_name):
        file_name = video_name + AUDIO_EXTENSION_EXPORT
        path_export = pathlib.Path(AUDIO_PATH) / file_name

        file_handle = self.video.export(
            path_export,
            format=AUDIO_EXTENSION,
            bitrate=AUDIO_BITRATE)

        # print("*** VIDEO EXPORTED TO MP3 ***")

    def copy_video(self):
        if not self.is_edit:
            file_name = str(self._patient.apnea_study.id) + \
                VIDEO_EXTENSION_EXPORT
        else:
            file_name = str(self._patient.apnea_study.id) + \
                VIDEO_EXTENSION_EXPORT

        self.path_dst = pathlib.Path(VIDEO_PATH) / file_name
        self.video_path = VIDEO_DB_PATH + r"\\" + file_name

        print("Video path dst:", self.path_dst)
        print("Selected Video Path:", self.path_video[0])
        # print(type(self.path_dst), self.path_dst)

        try:
            copyfile(self.path_video[0], self.path_dst)
            # print("*** VIDEO COPIED ***")
            self.convert_video_to_audio(str(self._patient.apnea_study.id))
        except SameFileError:
            log = Log()
            log.insert_log_error()

    def view_video(self):
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setMedia(QMediaContent(
            QUrl.fromLocalFile(self.path_video[0])))

        # print("Duration:", self.video_total_length)
        self.video_progress_bar.setMaximum(self.video_total_length)
        self.change_play_button_style()

        self.media_player.play()

        if self.is_edit and self.edit_flag:
            self.media_player.stop()
            self.change_stop_button_style()
            self.edit_flag = False

        self.media_player.positionChanged.connect(
            self.set_video_on_progress_bar)
        self.video_progress_bar.valueChanged.connect(self.set_position_video)

        self.play_button.clicked.connect(self.play)

    def play(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.change_stop_button_style()
        else:
            self.media_player.play()
            self.change_play_button_style()

    def set_video_on_progress_bar(self):
        self.video_progress_bar.blockSignals(True)
        self.video_progress_bar.setValue(self.media_player.position())
        self.video_progress_bar.blockSignals(False)
        if self.video_total_length == self.video_progress_bar.value():
            self.change_stop_button_style()

    def set_position_video(self):
        self.media_player.setPosition(self.video_progress_bar.value())

    def change_play_button_style(self):
        self.play_button.setStyleSheet("background-color: #ff0000;border:none")
        self.play_button.setText("Detener")

    def change_stop_button_style(self):
        self.play_button.setStyleSheet("background-color: #00ff00;border:none")
        self.play_button.setText("Reproducir")

    # -------------------- DATABASE --------------------

    def save_or_update_video(self):
        if self.path_video != "":
            self.procces_video()

            # Check if video path
            if self.path_video != "":
                # Edit flow variable. Operations on edit page
                if self.is_edit:
                    # Validate if the video id in patient object is not empty
                    if self.get_video_id() != "":
                        # If video id is not empty, then perform an update
                        self.update_video_in_database(self._patient)
                    else:
                        # If video id is empty, then perform an insert.
                        # If video id is empty, it means that in the lineal flow the user skipped load video step
                        self.insert_video_to_database()
                # Operation on load video lineal flow page
                else:
                    # Insert video to the database for the first time
                    self.insert_video_to_database()
            # If there is no image, but is edit, show image load error message
            elif self.is_edit:
                self.error_on_saving()

    def insert_video_to_database(self):

        tuple_data = (
            self._patient.apnea_study.id,
            self.video_path
        )
        multimedia_db = MultimediaDb()
        db_thread = DatabaseThread(
            target=multimedia_db.insert_video,
            args=(tuple_data,)
        )
        db_thread.start()
        insert_db_thread_event(db_thread.native_id)
        video_id = db_thread.join()

    def update_video_in_database(self, patient):
        apnea_study_id = self.get_video_id()
        tuple_data = (
            self.video_path,
        )

        db_multimedia = MultimediaDb()
        db_thread = DatabaseThread(
            target=db_multimedia.update_video,
            args=(apnea_study_id, tuple_data)
        )
        db_thread.start()
        insert_db_thread_event(db_thread.native_id)
        db_thread.join()

    def get_video_id(self):
        return self._patient.apnea_study.video.id

    def procces_video(self):
        self.copy_video()

    # -------------------- ERROR MESSAGES --------------------

    def error_on_saving(self) -> None:
        msg = QMessageBox()
        msg.setWindowTitle("Alerta!")
        msg.setText("Error en el guardado del video.")
        msg.exec_()

    def error_on_open_video(self) -> None:
        msg = QMessageBox()
        msg.setWindowTitle("Alerta!")
        msg.setText(
            "Error al intentar abrir el video.\nFavor de contactar administrador.")
        msg.exec_()

    def __os_dir(self):

        try:
            os.makedirs(os.path.normpath(AUDIO_PATH), exist_ok=False)
        except (FileExistsError, OSError):
            # print("Dirr already exist")
            self.insert_directory_error()

        try:
            os.makedirs(os.path.normpath(VIDEO_PATH), exist_ok=False)
        except (FileExistsError, OSError):
            # print("Dirr already exist")
            self.insert_directory_error()

    def insert_directory_error(self) -> None:
        log = Log()
        log.insert_log_error()
