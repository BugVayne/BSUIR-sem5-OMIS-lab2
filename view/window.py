import sys
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QMenu, QAction, QPushButton,
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QMessageBox, QDialog, QComboBox, QSlider
)
from PyQt5.QtMultimediaWidgets import QVideoWidget
from Platform import Platform
from view.button_actions import (
    show_effects_dialog,
    show_trim_video_dialog,
    show_add_audio_dialog,
    show_text_overlay_dialog,
    show_concatenate_video_dialog,
    create_project_dialog,
    load_video_dialog,
    save_project,
    export_video,
    show_fast_video_dialog,
    show_slow_video_dialog
)

class VideoEditorUI(QMainWindow):
    def __init__(self, platform):
        super().__init__()
        self.platform = platform
        self.setWindowTitle("Video Editor")
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        main_layout = QHBoxLayout(self.central_widget)

        self.create_left_panel(main_layout)

        self.create_video_player(main_layout)

        self.create_top_bar()



    def create_left_panel(self, main_layout):
        left_panel = QFrame(self)
        left_panel.setStyleSheet("background-color: #2E2E2E; padding: 10px;")
        left_panel.setFixedWidth(200)

        left_layout = QVBoxLayout(left_panel)

        import_button = QPushButton("Import Media", self)
        import_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 10px;")
        import_button.clicked.connect(lambda: load_video_dialog(self))
        left_layout.addWidget(import_button)

        left_layout.addSpacing(20)

        effects_button = QPushButton("Effects", self)
        effects_button.setStyleSheet("color: white; font-size: 14px;")
        effects_button.clicked.connect(lambda: show_effects_dialog(self))
        left_layout.addWidget(effects_button)

        trim_video_button = QPushButton("Trim Video", self)
        trim_video_button.setStyleSheet("color: white; font-size: 14px;")
        trim_video_button.clicked.connect(lambda:show_trim_video_dialog(self))
        left_layout.addWidget(trim_video_button)

        add_audio_button = QPushButton("Add Audio", self)
        add_audio_button.setStyleSheet("color: white; font-size: 14px;")
        add_audio_button.clicked.connect(lambda:show_add_audio_dialog(self))
        left_layout.addWidget(add_audio_button)

        text_overlay_button = QPushButton("Text Overlay", self)
        text_overlay_button.setStyleSheet("color: white; font-size: 14px;")
        text_overlay_button.clicked.connect(lambda:show_text_overlay_dialog(self))
        left_layout.addWidget(text_overlay_button)

        # concat_video_button = QPushButton("Concatenate Video", self)
        # concat_video_button.setStyleSheet("color: white; font-size: 14px;")
        # concat_video_button.clicked.connect(lambda:show_concatenate_video_dialog(self))
        # left_layout.addWidget(concat_video_button)


        slow_button = QPushButton("Slow Video", self)
        slow_button.setStyleSheet("color: white; font-size: 14px;")
        slow_button.clicked.connect(lambda:show_slow_video_dialog(self))
        left_layout.addWidget(slow_button)


        fast_video = QPushButton("Fast Video", self)
        fast_video.setStyleSheet("color: white; font-size: 14px;")
        fast_video.clicked.connect(lambda:show_fast_video_dialog(self))
        left_layout.addWidget(fast_video)

        left_layout.addStretch()

        main_layout.addWidget(left_panel)

    def create_video_player(self, main_layout):

        center_widget = QFrame(self)
        center_widget.setStyleSheet("background-color: #1E1E1E;")

        center_layout = QVBoxLayout(center_widget)

        self.video_widget = QVideoWidget(center_widget)
        self.video_widget.setStyleSheet("background-color: gray;")
        center_layout.addWidget(self.video_widget)

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)

        playback_controls = QHBoxLayout()
        playback_controls.setContentsMargins(350, 10, 350, 10)  # Set margins

        play_button = QPushButton(">", self)
        play_button.setStyleSheet("color: white;")
        play_button.setFixedSize(80, 30)
        play_button.clicked.connect(self.play_video)

        pause_button = QPushButton("||", self)
        pause_button.setStyleSheet("color: white;")
        pause_button.setFixedSize(80, 30)
        pause_button.clicked.connect(self.pause_video)

        stop_button = QPushButton("■", self)
        stop_button.setStyleSheet("color: white;")
        stop_button.setFixedSize(80, 30)
        stop_button.clicked.connect(self.stop_video)


        playback_controls.addWidget(play_button)
        playback_controls.addWidget(pause_button)
        playback_controls.addWidget(stop_button)
        center_layout.addLayout(playback_controls)

        # Create a slider for video navigation
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(0, 0)  # Initially set range to 0
        self.slider.setStyleSheet("QSlider::groove:horizontal { background: #555; }"
                                  "QSlider::handle:horizontal { background: #888; }")
        self.slider.valueChanged.connect(self.seek_video)  # Connect slider to seek_video method
        center_layout.addWidget(self.slider)

        # Connect media player signals to update the slider
        self.media_player.durationChanged.connect(self.update_slider_range)
        self.media_player.positionChanged.connect(self.update_slider_value)

        main_layout.addWidget(center_widget)

    def seek_video(self, position):
        self.media_player.setPosition(position)

    def update_slider_range(self, duration):
        self.slider.setRange(0, duration)

    def update_slider_value(self, position):
        self.slider.setValue(position)

    def create_top_bar(self):
        # Menu bar
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        file_menu = QMenu("project", self)
        menu_bar.addMenu(file_menu)

        open_action = QAction("Create Project", self)
        open_action.triggered.connect(lambda: create_project_dialog(self))
        file_menu.addAction(open_action)

        save_action = QAction("Save Project", self)
        save_action.triggered.connect(lambda: save_project(self))
        file_menu.addAction(save_action)

        export_button = QPushButton("Export", self)
        export_button.clicked.connect(lambda: export_video(self))
        export_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px;")
        export_button.setFixedHeight(30)
        export_button.setFixedWidth(80)


        menu_bar.setCornerWidget(export_button, Qt.TopRightCorner)

    def play_video(self):
        self.media_player.play()

    def pause_video(self):
        self.media_player.pause()

    def stop_video(self):
        self.media_player.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    platform = Platform()
    ui = VideoEditorUI(platform)
    ui.show()
    sys.exit(app.exec_())