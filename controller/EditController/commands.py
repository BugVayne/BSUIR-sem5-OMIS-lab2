from types import NoneType

from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip
import moviepy.video.fx.all as vfx
from moviepy.video.fx.speedx import speedx
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
class Command:
    def execute(self):
        pass


class FastMotionCommand(Command):
    def __init__(self, video_clip, speed_factor):
        self.video_clip = video_clip
        self.speed_factor = speed_factor

    def execute(self):
        if self.video_clip is None:
            print("\033[91m[FastMotionCommand] Error: video_clip is None.\033[0m")
            raise ValueError("FastMotionCommand received a None video_clip.")
        try:
            result = speedx(self.video_clip, self.speed_factor)
            print(f"[FastMotionCommand] Success: Applied fast motion with speed factor {self.speed_factor}.")
            return result
        except Exception as e:
            print(f"\033[91m[FastMotionCommand] Error: Failed to apply fast motion. Exception: {e}\033[0m")
            raise


class SlowMotionCommand(Command):
    def __init__(self, video_clip, speed_factor):
        self.video_clip = video_clip
        self.speed_factor = speed_factor

    def execute(self):
        if self.video_clip is None:
            print("\033[91m[SlowMotionCommand] Error: video_clip is None.\033[0m")
            raise ValueError("SlowMotionCommand received a None video_clip.")
        try:
            result = speedx(self.video_clip, 1/self.speed_factor)
            print(f"[SlowMotionCommand] Success: Applied slow motion with speed factor {self.speed_factor}.")
            return result
        except Exception as e:
            print(f"\033[91m[SlowMotionCommand] Error: Failed to apply slow motion. Exception: {e}\033[0m")
            raise


class TextOverlayCommand(Command):
    def __init__(self, video_clip, text, position, duration):
        if video_clip is None:
            print("\033[91m[TextOverlayCommand] Error: video_clip is None.\033[0m")
            raise ValueError("TextOverlayCommand received a None video_clip.")
        self.video_clip = video_clip
        self.text = text
        self.position = position
        self.duration = duration

    def execute(self):
        if self.video_clip is None:
            print("\033[91m[TextOverlayCommand] Error: video_clip is None.\033[0m")
            raise ValueError("TextOverlayCommand received a None video_clip.")
        try:
            # Create a TextClip
            text_clip = TextClip(self.text, fontsize=70, color='white')
            text_clip = text_clip.set_pos(self.position).set_duration(self.duration)

            # Overlay the text onto the video using CompositeVideoClip
            video_with_text = CompositeVideoClip([self.video_clip, text_clip])
            print(f"[TextOverlayCommand] Success: Added text overlay '{self.text}' at position '{self.position}' for duration {self.duration}s.")
            return video_with_text
        except Exception as e:
            print(f"\033[91m[TextOverlayCommand] Error: Failed to apply text overlay. Exception: {e}\033[0m")
            raise


class AddAudioCommand(Command):
    def __init__(self, video_clip, audio_clip, start_time=0):
        self.video_clip = video_clip
        self.audio_clip = audio_clip
        self.start_time = start_time

    def execute(self):
        if self.video_clip is None:
            print("\033[91m[AddAudioCommand] Error: video_clip is None.\033[0m")
            raise ValueError("AddAudioCommand received a None video_clip.")
        if self.audio_clip is None:
            print("\033[91m[AddAudioCommand] Error: audio_clip is None.\033[0m")
            raise ValueError("AddAudioCommand received a None audio_clip.")
        try:
            audio_with_start = self.audio_clip.set_start(self.start_time)
            result = self.video_clip.set_audio(audio_with_start)
            print(f"[AddAudioCommand] Success: Added audio starting at {self.start_time}s.")
            return result
        except Exception as e:
            print(f"\033[91m[AddAudioCommand] Error: Failed to add audio. Exception: {e}\033[0m")
            raise


class ApplyFilterCommand(Command):
    def __init__(self, video_clip, filter_type):
        self.video_clip = video_clip
        self.filter_type = filter_type

    def execute(self):
        if self.video_clip is None:
            print("\033[91m[ApplyFilterCommand] Error: video_clip is None.\033[0m")
            raise ValueError("ApplyFilterCommand received a None video_clip.")
        try:
            if self.filter_type == 'grayscale':
                result = self.video_clip.fx(vfx.blackwhite)
            elif self.filter_type == 'invert':
                result = self.video_clip.fx(vfx.invert_colors)  # Use invert_colors instead of colorx
            elif self.filter_type == 'my_custom_filter':
                result = self.video_clip.fx(vfx.colorx, 0.9).fx(vfx.lum_contrast, 0, 10, 100)
            elif self.filter_type == 'brightness_increase':
                result = self.video_clip.fx(vfx.colorx, 1.2)  # Increase brightness
            elif self.filter_type == 'contrast_increase':
                result = self.video_clip.fx(vfx.lum_contrast, 0, 1.1, 0)  # Increase contrast
            else:
                print(f"\033[91m[ApplyFilterCommand] Error: Unsupported filter type '{self.filter_type}'.\033[0m")
                raise ValueError(f"Unsupported filter type: {self.filter_type}")

            print(f"[ApplyFilterCommand] Success: Applied filter '{self.filter_type}'.")
            return result
        except Exception as e:
            print(f"\033[91m[ApplyFilterCommand] Error: Failed to apply filter '{self.filter_type}'. Exception: {e}\033[0m")
            raise

class ConcatenateVideosCommand(Command):
    def __init__(self, video_clip, video_clip2):
        if not video_clip or not video_clip2:
            print("\033[91m[ConcatenateVideosCommand] Error: video_clips list is empty.\033[0m")
            raise ValueError("ConcatenateVideosCommand received an empty video_clips list.")
        self.video_clip = video_clip
        self.video_clip2 = video_clip2

    def execute(self):
        if self.video_clip is None or self.video_clip2 is None:
            print("\033[91m[ConcatenateVideosCommand] Error: One or both video clips are None.\033[0m")
            raise ValueError("Cannot concatenate None video clips.")
        if self.video_clip.reader is NoneType:
            self.video_clip.reader = self.video_clip2.reader
        try:
            result = concatenate_videoclips([self.video_clip, self.video_clip2])
            print(f"[ConcatenateVideosCommand] Success: Concatenated 2 video clips.")
            return result
        except Exception as e:
            print(f"\033[91m[ConcatenateVideosCommand] Error: Failed to concatenate video clips. Exception: {e}\033[0m")
            raise


class TrimVideoCommand(Command):
    def __init__(self, video_clip, start_time, end_time):
        self.video_clip = video_clip
        self.start_time = start_time
        self.end_time = end_time

    def execute(self):
        if self.video_clip is None:
            print("\033[91m[TrimVideoCommand] Error: video_clip is None.\033[0m")
            raise ValueError("TrimVideoCommand received a None video_clip.")
        try:
            result = self.video_clip.subclip(self.start_time, self.end_time)
            print(f"[TrimVideoCommand] Success: Trimmed video from {self.start_time}s to {self.end_time}s.")
            return result
        except Exception as e:
            print(f"\033[91m[TrimVideoCommand] Error: Failed to trim video. Exception: {e}\033[0m")
            raise

if __name__ == "__main__":

    video_clip = VideoFileClip("../temp_files/video.mp4")
    video_clip2 = VideoFileClip("../temp_files/smth.mov")

    trim_video_command = TrimVideoCommand(video_clip, 0, 1)
    concatenate_video_command = ConcatenateVideosCommand(video_clip, video_clip2)
    fast_motion_command = FastMotionCommand(video_clip, speed_factor=2)  # 2x speed
    slow_motion_command = SlowMotionCommand(video_clip, speed_factor=2)  # 0.5x speed
    text_overlay_command = TextOverlayCommand(video_clip, "Hello, World!", position='center', duration=5)
    filter_command = ApplyFilterCommand(video_clip, "grayscale")
    filter_command2 = ApplyFilterCommand(video_clip, "invert")
    audio_clip_ = AudioFileClip("../temp_files/audio.mp3")
    audio_command = AddAudioCommand(video_clip, audio_clip_, 0)

    # audio_clip = audio_command.execute()
    # fast_motion_clip = fast_motion_command.execute()
    # slow_motion_clip = slow_motion_command.execute()
    # text_overlay_clip = text_overlay_command.execute()
    # filter1_clip = filter_command.execute()
    # filter2_clip = filter_command2.execute()
    # trim_clip = trim_video_command.execute()
    concate_video_clip = concatenate_video_command.execute()

    # audio_clip.write_videofile("../temp_files/audio_output.mp4")
    # fast_motion_clip.write_videofile("../temp_files/fast_motion_output.mp4")
    # slow_motion_clip.write_videofile("../temp_files/slow_motion_output.mp4")
    # text_overlay_clip.write_videofile("../temp_files/text_overlay_output.mp4")
    # filter1_clip.write_videofile("../temp_files/filter_output.mp4")
    # filter2_clip.write_videofile("../temp_files/filter_output2.mp4")
    # trim_clip.write_videofile("../temp_files/trimmed.mp4")
    concate_video_clip.write_videofile("../temp_files/concated.mp4")