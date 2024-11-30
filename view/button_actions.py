import os
import sys

from PyQt5.QtGui import QIntValidator

from config import TEMP_VIDEO_FILE
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QMenu, QAction, QPushButton,
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QMessageBox, QDialog, QComboBox, QLineEdit
)
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


def show_trim_video_dialog(self):
    trim_dialog = QDialog(self)
    trim_dialog.setWindowTitle("Trim your video")
    trim_dialog.setFixedSize(400, 200)


    layout = QVBoxLayout(trim_dialog)

    label = QLabel("Choose a start time:")
    layout.addWidget(label)
    start_time = QLineEdit()
    start_time.size()
    int_validator = QIntValidator()
    start_time.setValidator(int_validator)
    layout.addWidget(start_time, stretch=2)


    label = QLabel("Choose an end time:")
    layout.addWidget(label)
    end_time = QLineEdit()
    int_validator = QIntValidator()
    end_time.setValidator(int_validator)
    layout.addWidget(end_time, stretch=2)

    apply_button = QPushButton("Trim")
    apply_button.clicked.connect(
        lambda: handle_and_close_dialog(trim_dialog,
                                        apply_trim,
                                        self,
                                        start_time=start_time.text(),
                                        end_time=end_time.text()))
    layout.addWidget(apply_button, stretch=1)
    trim_dialog.exec_()


def apply_trim(self, start_time, end_time):
        self.platform.apply_effect("trim_video", start_time=start_time, end_time=end_time)
        self.platform.main_controller.export_controller.save_video(
                        self.platform.main_controller.edit_controller.get_current_video())
        if os.path.exists(TEMP_VIDEO_FILE):  # Ensure the file exists
            self.media_player.stop()
            self.media_player.setMedia(QMediaContent(None))
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(TEMP_VIDEO_FILE)))

def show_add_audio_dialog(self):
    audio_dialog = QDialog(self)
    audio_dialog.setWindowTitle("Add audio")
    audio_dialog.setFixedSize(400, 200)


    layout = QVBoxLayout(audio_dialog)

    label = QLabel("Choose a start time:")
    layout.addWidget(label)
    start_time = QLineEdit()

    start_time.setText("0")
    int_validator = QIntValidator()
    start_time.setValidator(int_validator)
    layout.addWidget(start_time)

    apply_button = QPushButton("Open a video")
    apply_button.clicked.connect(
        lambda: handle_and_close_dialog(audio_dialog,
                                        apply_audio,
                                        self,
                                        start_time=start_time.text()))
    layout.addWidget(apply_button, stretch=1)
    audio_dialog.exec_()


def apply_audio(self, start_time):
    audio = self.platform.main_controller.file_controller.get_audio_clip()
    self.platform.apply_effect(choice="add_audio", audio_clip=audio, start_time=start_time)
    self.platform.main_controller.export_controller.save_video(
        self.platform.main_controller.edit_controller.get_current_video())
    if os.path.exists(TEMP_VIDEO_FILE):  # Ensure the file exists
        self.media_player.stop()
        self.media_player.setMedia(QMediaContent(None))
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(TEMP_VIDEO_FILE)))
    self.platform.project_service.update_current_project_videos([audio.filename])


def show_text_overlay_dialog(self):
    text_dialog = QDialog(self)
    text_dialog.setWindowTitle("Trim your video")
    text_dialog.setFixedSize(400, 200)

    layout = QVBoxLayout(text_dialog)

    label = QLabel("Choose duration:")
    layout.addWidget(label)
    duration = QLineEdit()
    duration.size()
    int_validator = QIntValidator()
    duration.setValidator(int_validator)
    layout.addWidget(duration, stretch=2)

    label = QLabel("Choose position:")
    layout.addWidget(label)
    position = QLineEdit()
    layout.addWidget(position, stretch=2)

    label = QLabel("Enter text to overlay")
    layout.addWidget(label)
    text = QLineEdit()
    layout.addWidget(text, stretch=2)

    apply_button = QPushButton("Overlay")
    apply_button.clicked.connect(
        lambda: handle_and_close_dialog(text_dialog,
                                        apply_text_overlay,
                                        self,
                                        text = text.text(),
                                        position = position.text(),
                                        duration = duration.text()))
    layout.addWidget(apply_button, stretch=1)
    text_dialog.exec_()


def apply_text_overlay(self, text, position, duration):
    self.platform.apply_effect("text_overlay", text = text, position = position, duration = duration)
    self.platform.main_controller.export_controller.save_video(
        self.platform.main_controller.edit_controller.get_current_video())
    if os.path.exists(TEMP_VIDEO_FILE):  # Ensure the file exists
        self.media_player.stop()
        self.media_player.setMedia(QMediaContent(None))
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(TEMP_VIDEO_FILE)))


def show_concatenate_video_dialog(self):
    self.platform.main_controller.file_controller.clear()
    self.platform.apply_effect(choice="concatenate_videos")
    self.platform.main_controller.export_controller.save_video(
        self.platform.main_controller.edit_controller.get_current_video())
    if os.path.exists(TEMP_VIDEO_FILE):
        self.media_player.stop()
        self.media_player.setMedia(QMediaContent(None))
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(TEMP_VIDEO_FILE)))
    video = self.platform.main_controller.file_controller.get_video_clip()
    self.platform.project_service.update_current_project_videos([video.filename])


def show_effects_dialog(self):
    effects_dialog = QDialog(self)
    effects_dialog.setWindowTitle("Choose an Effect")
    effects_dialog.setFixedSize(400, 200)

    layout = QVBoxLayout(effects_dialog)
    label = QLabel("Choose an effect to apply:")
    layout.addWidget(label, stretch=1)

    effects_combobox = QComboBox()
    effects_combobox.addItems(["grayscale", "invert", "my_custom_filter", "brightness_increase", "contrast_increase"])
    effects_combobox.setFixedHeight(40)
    effects_combobox.setStyleSheet("""
        QComboBox {
            font-size: 16px;
            padding: 10px;    
        }
        QComboBox QAbstractItemView {
            font-size: 16px;  
            padding: 10px;   
        }
    """)

    layout.addWidget(effects_combobox)

    apply_button = QPushButton("Apply")
    apply_button.clicked.connect(lambda : handle_and_close_dialog(
                                            effects_dialog,
                                            apply_effect,
                                            self,
                                             filter_type_ = effects_combobox.currentText()))
    layout.addWidget(apply_button, stretch=2)

    effects_dialog.exec_()

def apply_effect(self, filter_type_):
    self.platform.apply_effect("add_filter", filter_type=filter_type_)

    # Save the video and wait for the process to complete
    self.platform.main_controller.export_controller.save_video(
        self.platform.main_controller.edit_controller.get_current_video()
    )

    # Add a delay or check to ensure the file is saved before reloading
    if os.path.exists(TEMP_VIDEO_FILE):  # Ensure the file exists
        self.media_player.stop()
        self.media_player.setMedia(QMediaContent(None))
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(TEMP_VIDEO_FILE)))

def create_project_dialog(self):

    create_dialog = QDialog(self)
    create_dialog.setWindowTitle("Create a Project")
    create_dialog.setFixedSize(400, 200)

    layout = QVBoxLayout(create_dialog)
    label = QLabel("Choose a name for your project:")
    layout.addWidget(label)

    text = QLineEdit()
    layout.addWidget(text)

    apply_button = QPushButton("Apply")
    apply_button.clicked.connect(lambda: handle_and_close_dialog(create_dialog, self.platform.create_project, text.text()))
    layout.addWidget(apply_button)

    create_dialog.exec_()

def load_video_dialog(self):
    try:
        if not self.platform.main_controller.edit_controller.get_current_video():
            self.platform.load_video()
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.platform.main_controller.edit_controller.
                                                                        get_current_video().filename)))
            QMessageBox.information(self, "Success", "the operation executed successfully.")
        else:
            QMessageBox.information(self, "Error", "the video already loaded")
    except Exception as e:
        QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

def save_project(self):
    self.platform.save_project()
    QMessageBox.information(self, "Project Saved", "Your project has been saved successfully.")


def handle_and_close_dialog(dialog, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
        dialog.accept()
        QMessageBox.information(dialog, "Success", "the operation executed successfully.")
    except Exception as e:
        QMessageBox.critical(dialog, "Error", f"An error occurred: {str(e)}")

def export_video(self):
    try:
        self.platform.save_project()
        self.platform.main_controller.export_video()
        self.media_player.stop()
        self.media_player.setMedia(QMediaContent(None))
        self.platform.main_controller.clear_resources()
        self.platform.project_service.current_project = None

        QMessageBox.information(self, "Success", "the operation executed successfully.")
    except Exception as e:
        QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

def show_slow_video_dialog(self):
    slow_dialog = QDialog(self)
    slow_dialog.setWindowTitle("slow motion")
    slow_dialog.setFixedSize(400, 200)

    layout = QVBoxLayout(slow_dialog)

    label = QLabel("Enter speed factor")
    layout.addWidget(label)
    speed_factor = QLineEdit()

    int_validator = QIntValidator()
    speed_factor.setValidator(int_validator)
    layout.addWidget(speed_factor)

    apply_button = QPushButton("Slow your video")
    apply_button.clicked.connect(
        lambda: handle_and_close_dialog(slow_dialog,
                                        apply_slow_motion,
                                        self,
                                        speed_factor=speed_factor.text()))
    layout.addWidget(apply_button, stretch=1)
    slow_dialog.exec_()

def apply_slow_motion(self, speed_factor):
    speed_factor = float(speed_factor)
    self.platform.apply_effect("slow_motion", speed_factor=speed_factor)

    self.platform.main_controller.export_controller.save_video(
        self.platform.main_controller.edit_controller.get_current_video()
    )

    if os.path.exists(TEMP_VIDEO_FILE):
        self.media_player.stop()
        self.media_player.setMedia(QMediaContent(None))
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(TEMP_VIDEO_FILE)))


def show_fast_video_dialog(self):
    slow_dialog = QDialog(self)
    slow_dialog.setWindowTitle("fast motion")
    slow_dialog.setFixedSize(400, 200)

    layout = QVBoxLayout(slow_dialog)

    label = QLabel("Enter speed factor")
    layout.addWidget(label)
    speed_factor = QLineEdit()

    int_validator = QIntValidator()
    speed_factor.setValidator(int_validator)
    layout.addWidget(speed_factor)

    apply_button = QPushButton("fast your video")
    apply_button.clicked.connect(
        lambda: handle_and_close_dialog(slow_dialog,
                                        apply_fast_motion,
                                        self,
                                        speed_factor=speed_factor.text()))
    layout.addWidget(apply_button, stretch=1)
    slow_dialog.exec_()


def apply_fast_motion(self, speed_factor):
    speed_factor = float(speed_factor)
    self.platform.apply_effect("fast_motion", speed_factor=speed_factor)

    self.platform.main_controller.export_controller.save_video(
        self.platform.main_controller.edit_controller.get_current_video()
    )

    if os.path.exists(TEMP_VIDEO_FILE):
        self.media_player.stop()
        self.media_player.setMedia(QMediaContent(None))
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(TEMP_VIDEO_FILE)))