import sys

from PyQt5.QtWidgets import QApplication

from controller.MainController import MainController
from model.project.ProjectRep import ProjectRepository
from model.project.ProjectService import ProjectService
from model.project.Project import Project
from view.window import VideoEditorUI


class Platform:
    def __init__(self):
        self.main_controller = MainController()
        self.project_repository = ProjectRepository()
        self.project_service = ProjectService(self.project_repository)


    def create_project(self, name):
        try:
            self.project_service.create_project(name)
            self.project_service.save_current_project()
        except Exception as e:
            print(f"\033[91m[Platform] Error: Create failed Exception: {e}\033[0m")

    def save_project(self):
        try:
            self.project_service.save_current_project()
        except Exception as e:
            print(f"\033[91m[Platform] Error: save failed Exception: {e}\033[0m")

    def load_video(self):
        try:
            if not self.project_service.current_project:
                print(f"\033[91m[Platform] no project loaded\033[0m")
            else:
                self.main_controller.load_video()
                self.project_service.update_current_project_videos([self.main_controller.edit_controller.get_current_video().filename])
        except Exception as e:
            print(f"\033[91m[Platform] Error: save failed Exception: {e}\033[0m")


    def apply_effect(self, choice = None, **kwargs):
        self.main_controller.choose_effect_to_apply(choice, **kwargs)
        kwargs_str = ', '.join(f"{key}={value}" for key, value in kwargs.items())
        self.project_service.update_current_project_effects([f"{choice} : {kwargs_str}"])
        self.project_service.save_current_project()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    platform = Platform()
    ui = VideoEditorUI(platform)
    ui.show()
    sys.exit(app.exec_())