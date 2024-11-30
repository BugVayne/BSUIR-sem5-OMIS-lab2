import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QSlider
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, Qt
from moviepy.editor import VideoFileClip


class VideoPlayer(QMainWindow):
    def __init__(self, video_path = None):
        super().__init__()

        self.video_path = video_path
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.init_ui()

        # Load the video into the media player
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.video_path)))
        self.clip = VideoFileClip(video_path)

    def init_ui(self):
        # Create the central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create the video widget
        self.video_widget = QVideoWidget()
        self.media_player.setVideoOutput(self.video_widget)

        # Create playback buttons
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.toggle_play_pause)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.toggle_play_pause)

        self.forward_button = QPushButton(">> 10s")
        self.forward_button.clicked.connect(self.skip_forward)

        self.backward_button = QPushButton("<< 10s")
        self.backward_button.clicked.connect(self.skip_backward)

        # Create a slider for playback
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.sliderMoved.connect(self.set_position)

        # Layout for control buttons
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.pause_button)
        control_layout.addWidget(self.backward_button)
        control_layout.addWidget(self.forward_button)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)
        layout.addWidget(self.slider)
        layout.addLayout(control_layout)

        # Set the layout for the central widget
        central_widget.setLayout(layout)

        # Set up the window
        self.setWindowTitle("Video Playback Controller")
        self.resize(800, 600)

        # Connect the media player signals
        self.media_player.positionChanged.connect(self.update_slider)
        self.media_player.durationChanged.connect(self.set_slider_range)

    def toggle_play_pause(self):
        """Toggle between play and pause."""
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def skip_forward(self):
        """Skip 10 seconds forward."""
        new_position = self.media_player.position() + 10 * 1000
        if new_position < self.media_player.duration():
            self.media_player.setPosition(new_position)

    def skip_backward(self):
        """Skip 10 seconds backward."""
        new_position = self.media_player.position() - 10 * 1000
        if new_position > 0:
            self.media_player.setPosition(new_position)

    def set_position(self, position):
        """Set the playback position using the slider."""
        self.media_player.setPosition(position)

    def update_slider(self, position):
        """Update the slider as the video plays."""
        self.slider.setValue(position)

    def set_slider_range(self, duration):
        """Set the slider's range based on the duration of the video."""
        self.slider.setRange(0, duration)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Provide the path to your video file here
    video_path = "../temp_files/video.mp4"

    player = VideoPlayer(video_path)
    player.show()

    sys.exit(app.exec_())