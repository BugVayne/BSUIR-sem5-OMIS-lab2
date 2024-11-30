from PyQt5.QtWidgets import QApplication, QFileDialog

from config import TEMP_VIDEO_FILE


class ExportController:
    @staticmethod
    def choose_output_filename(default_name=TEMP_VIDEO_FILE, file_types="Video Files (*.mp4 *.avi *.mov *.mkv)"):
        """
        Opens a Qt file dialog to let the user choose the output filename and format.
        """
        app = QApplication.instance()
        if not app:  # If no QApplication exists, create one
            app = QApplication([])

        # Open the Save File dialog
        filepath, _ = QFileDialog.getSaveFileName(
            caption="Save Video As",
            directory=f"{default_name}",
            filter=file_types
        )

        return filepath

    @staticmethod
    def save_video(video_clip, output_filename = TEMP_VIDEO_FILE, output_format="mp4"):

        # Default codecs for supported formats
        format_codecs = {
            "mp4": {"codec": "libx264", "audio_codec": "aac"},
            "avi": {"codec": "mpeg4", "audio_codec": None},
            "mov": {"codec": "libx264", "audio_codec": "aac"},
            "mkv": {"codec": "libx264", "audio_codec": "aac"},
        }

        if output_format not in format_codecs:
            raise ValueError(f"Unsupported format: {output_format}")

        # Get codec settings for the chosen format
        codec = format_codecs[output_format]["codec"]
        audio_codec = format_codecs[output_format]["audio_codec"]

        print(f"Saving video as: {output_filename}")
        try:
            # Save the video file
            video_clip.write_videofile(output_filename, codec=codec, audio_codec=audio_codec)
            print(f"Video saved successfully as {output_filename}")
        except Exception as e:
            print(f"An error occurred while saving the video: {e}")

    @staticmethod
    def save_video_with_dialog(video_clip, output_path=None):
        """
        Opens a file dialog to choose the output filename and saves the video in the selected format.
        """
        path = output_path
        if not path:
            path = ExportController.choose_output_filename()
            if not path:
                print("No output file selected. Operation canceled.")
                return


        # Extract the desired format from the file extension
        output_format = path.split(".")[-1]  # Get file extension (e.g., "mp4", "avi", etc.)

        # Save the video
        ExportController.save_video(video_clip, path, output_format)
        return path