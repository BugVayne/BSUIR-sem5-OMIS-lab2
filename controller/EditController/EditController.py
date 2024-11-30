from controller.EditController.commands import *
from controller.FileController.FileController import FileController


class EditController:
    def __init__(self, video_clip_=None, audio_clip__=None):
        self.file_controller = FileController()
        self.current_video = video_clip_
        self.current_audio = audio_clip__

    def execute_command(self, command=None):
        if command is None:
            print("\033[91m[EditController] Error: No command provided.\033[0m")
            return
        if self.current_video is None:
            print("\033[91m[EditController] Error: No current video to process.\033[0m")
            return
        if command.video_clip is None:
            print("\033[91m[EditController] Error: No video in command.\033[0m")
            return

        try:
            result = command.execute()
            if result is not None:
                self.current_video = result  # Update current video with the result
        except Exception as e:
            print(f"\033[91m[EditController] Error while executing command: {e}\033[0m")

    def set_current_video(self, video_:VideoFileClip):
        self.current_video = video_

    def get_current_video(self):
        return self.current_video

    def apply_slow_motion(self, speed_factor=2):
        print("[EditController] Applying slow motion...")
        command = SlowMotionCommand(self.current_video, speed_factor)
        self.execute_command(command)

    def apply_text_overlay(self, text="Default Text", position="center", duration=5):
        print("[EditController] Applying text overlay...")
        command = TextOverlayCommand(self.current_video, text, position, duration)
        self.execute_command(command)

    def apply_filter(self, filter_type="grayscale"):
        print("[EditController] Applying filter...")
        try:
            command = ApplyFilterCommand(self.current_video, filter_type)
            self.execute_command(command)
        except Exception as e:
            print(f"[EditController] Error while applying filter: {e}")

    def apply_add_audio_to_video(self, start_time=0, audio_clip=None):
        print("[EditController] Adding audio to video...")
        if audio_clip is None:
            audio_clip = self.file_controller.get_audio_clip()
        command = AddAudioCommand(self.current_video, audio_clip, start_time)
        self.execute_command(command)

    def apply_trim_video(self, start_time=0, end_time=5):
        print("[EditController] Trimming video...")
        if start_time > end_time:
            raise ValueError("Start time must be less than end time.")
        command = TrimVideoCommand(self.current_video, start_time, end_time)
        self.execute_command(command)

    def apply_concatenate_videos(self, videofile = None):
        print("[EditController] Concatenating videos...")
        if videofile is None:
            self.file_controller.upload_video()
            videofile = self.file_controller.get_video_clip()
        if self.current_video is None:
            print("\033[91m[EditController] Error: No current video to concatenate.\033[0m")
            return
        if videofile is None:
            print("\033[91m[EditController] Error: The uploaded video file is invalid or None.\033[0m")
            return
        command = ConcatenateVideosCommand(self.current_video, VideoFileClip(videofile.filename))
        self.execute_command(command)

    def apply_fast_motion(self, speed_factor=2):
        print("[EditController] Applying fast motion...")
        command = FastMotionCommand(self.current_video, speed_factor)
        self.execute_command(command)

if __name__ == '__main__':
    original_video = "../temp_files/video.mp4"
    background_audio = "../temp_files/audio.mp3"
    video = VideoFileClip(original_video)

    edit_controller = EditController(video_clip_=video)

    edit_controller.apply_filter("invert")
    edit_controller.apply_trim_video(2, 3)
