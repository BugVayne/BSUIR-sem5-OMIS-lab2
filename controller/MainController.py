from controller.FileController.FileController import FileController
from controller.FileController.ExportController import ExportController
from controller.EditController.EditController import EditController
from controller.EditController.commands import *

class MainController:
    def __init__(self):
        self.file_controller = FileController()
        self.edit_controller = EditController()
        self.export_controller = ExportController()

    def choose_effect_to_apply(self, choice, **kwargs):
        effect_mapping = {
            'trim_video': self.edit_controller.apply_trim_video,
            'slow_motion': self.edit_controller.apply_slow_motion,
            'fast_motion': self.edit_controller.apply_fast_motion,
            'text_overlay': self.edit_controller.apply_text_overlay,
            'add_audio': self.edit_controller.apply_add_audio_to_video,
            'add_filter': self.edit_controller.apply_filter,
            'concatenate_videos': self.edit_controller.apply_concatenate_videos,
        }

        effect_function = effect_mapping.get(choice)

        if effect_function:
            effect_function(**kwargs)
        else:
            print(f"[MainController] Effect '{choice}' is not recognized.")

    def load_video(self, filepath=None):
        try:
            self.edit_controller.set_current_video(self.file_controller.get_video_clip())
            print("[MainController] Video successfully loaded and set in EditController.")
        except Exception as e:
            print(f"[MainController] Error while loading video: {e}")

    def load_audio(self, filepath=None):
        try:
            self.file_controller.upload_audio(filepath)
            print("[MainController] Audio successfully loaded.")
        except Exception as e:
            print(f"[MainController] Error while loading audio: {e}")

    def export_video(self, output_path=None):
        if self.edit_controller.get_current_video() is None:
            print("[MainController] Error: No video loaded in EditController.")
            return
        try:
            path = self.export_controller.save_video_with_dialog(self.edit_controller.get_current_video(), output_path)
            print(f"[MainController] Video successfully exported to {path}.")
        except Exception as e:
            print(f"[MainController] Error while exporting video: {e}")

    def clear_resources(self):
        try:
            self.file_controller.clear()
            self.edit_controller.set_current_video(None)
            print("[MainController] All resources cleared.")
        except Exception as e:
            print(f"[MainController] Error while clearing resources: {e}")


if __name__ == "__main__":
    main_controller = MainController()

    # Load video and audio files
    main_controller.load_video()
    main_controller.load_audio("temp_files/audio.mp3")

    # Apply effects

    # Apply effects with default values
    main_controller.choose_effect_to_apply("slow_motion", speed_factor=3)
    main_controller.choose_effect_to_apply("add_audio", start_time=2)
    main_controller.choose_effect_to_apply("add_filter", filter_type = 'my_filter')

    # Add audio and export
    # main_controller.export_video("final_output6.mp4")

    # Clear resources
    main_controller.clear_resources()