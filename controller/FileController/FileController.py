import os
from PyQt5.QtWidgets import QApplication, QFileDialog
from moviepy.editor import VideoFileClip, AudioFileClip
from controller.FileController.ExportController import ExportController

class FileController:
    def __init__(self):
        self.video_clip = None
        self.audio_clip = None

    @staticmethod
    def _file_picker(file_types, caption):
        app = QApplication.instance()
        if not app:
            app = QApplication([])

        filepath, _ = QFileDialog.getOpenFileName(
            caption=caption,
            filter=file_types
        )

        return filepath

    def upload_video(self, filepath=None):
        if filepath is None:
            filepath = FileController._file_picker("Video Files (*.mp4 *.avi *.mov *.mkv);;All Files (*)", "Open a Video")
            if not filepath:
                raise ValueError("[FileController] No video file was selected.")

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"[FileController] The video file '{filepath}' does not exist.")

        try:
            self.video_clip = VideoFileClip(filepath)
            print(f"[FileController] Video file '{filepath}' loaded successfully.")
        except Exception as e:
            raise ValueError(f"[FileController] An error occurred while loading the video file: {e}")

    def upload_audio(self, filepath=None):
        if filepath is None:
            filepath = FileController._file_picker("Audio Files (*.mp3 *.wav *.aac);;All Files (*)", "Open an Audio")
            if not filepath:
                raise ValueError("[FileController] No audio file was selected.")

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"[FileController] The audio file '{filepath}' does not exist.")

        try:
            self.audio_clip = AudioFileClip(filepath)
            print(f"[FileController] Audio file '{filepath}' loaded successfully.")
        except Exception as e:
            raise ValueError(f"[FileController] An error occurred while loading the audio file: {e}")
    def get_video_clip(self):
        if self.video_clip is None:
            self.upload_video()
        return self.video_clip

    def get_audio_clip(self):
        if self.audio_clip is None:
            self.upload_audio()
        return self.audio_clip

    def clear(self):
        if self.video_clip:
            self.video_clip.close()
        if self.audio_clip:
            self.audio_clip.close()
        self.video_clip = None
        self.audio_clip = None
        print("[FileController] FileController has been cleared.")


if __name__ == "__main__":
    file_controller = FileController()

    try:
        file_controller.upload_video()  # Opens file picker for video
        file_controller.upload_audio()  # Opens file picker for audio
    except ValueError as e:
        print(f"[FileController] Selection error: {e}")
    except FileNotFoundError as e:
        print(f"[FileController] File not found: {e}")
    except Exception as e:
        print(f"[FileController] Error: {e}")

    # Get the loaded video and audio clips
    try:
        video_clip = file_controller.get_video_clip()
        audio_clip = file_controller.get_audio_clip()

        # Add audio to the video clip (optional step)
        video_with_audio = video_clip.set_audio(audio_clip)

        # Open a save dialog and save the video using ExportController
        ExportController.save_video_with_dialog(video_with_audio)

        # Close the video clip
        video_with_audio.close()
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Clear the FileController
    file_controller.clear()