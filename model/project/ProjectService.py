from typing import List

from model.project.ProjectRep import ProjectRepository
from model.project.Project import Project


class ProjectService:
    def __init__(self, project_repository):
        self.project_repository = project_repository
        self.current_project = None  # Store the current project as None initially

    def create_project(self, name: str):
        if self.project_repository.get_project(name):
            raise ValueError(f"\033[91m [ProjectService] Project with name '{name}' already exists.")
        self.current_project = Project(name)
        self.project_repository.add_project(self.current_project)

    def delete_project(self, name: str):
        if not self.project_repository.get_project(name):
            raise ValueError(f"\033[91m [ProjectService] Project with name '{name}' does not exist.")
        self.project_repository.delete_project(name)

    def get_project(self, name: str):
        return self.project_repository.get_project(name)

    def list_projects(self):
        return self.project_repository.load_projects()

    def update_project(self, project: Project):
        self.project_repository.update_project(project)

    def set_current_project(self, name: str):
        project = self.project_repository.get_project(name)
        if not project:
            raise ValueError(f"\033[91m [ProjectService] Project with name '{name}' does not exist.\033[0m")
        self.current_project = project

    def save_current_project(self):
        if not self.current_project:
            raise ValueError("\033[91m [ProjectService] No current project to save.\033[0m")
        self.project_repository.update_project(self.current_project)

    def upload_to_current_project(self, videos: List[str], effects: List[str]):
        if not self.current_project:
            raise ValueError("\033[91m [ProjectService] No current project to upload to.\033[0m")
        self.current_project.videos.extend(videos)  # Add videos to the current project
        self.current_project.effects.extend(effects)  # Add effects to the current project
        self.current_project.update_last_modified()  # Update last modified date

    def update_current_project_videos(self, videos: List[str]):
        if not self.current_project:
            raise ValueError("\033[91m [ProjectService] No current project to update.\033[0m")
        self.current_project.videos.extend(videos)  # Replace the current project's videos
        self.current_project.update_last_modified()  # Update last modified date

    def update_current_project_effects(self, effects: List[str]):
        if not self.current_project:
            raise ValueError("\033[91m [ProjectService] No current project to update.\033[0m")
        self.current_project.effects.extend(effects)  # Replace the current project's effects
        self.current_project.update_last_modified()  # Update last modified date