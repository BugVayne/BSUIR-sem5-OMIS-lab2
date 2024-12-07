from abc import abstractmethod, ABC
from typing import List
from model.project.ProjectRep import ProjectRepository
from model.project.Project import Project



class IProjectService(ABC):

    @abstractmethod
    def create_project(self, name: str):
        """Create a new project with the given name."""
        pass

    @abstractmethod
    def delete_project(self, name: str):
        """Delete a project by name."""
        pass

    @abstractmethod
    def get_project(self, name: str) -> Optional['Project']:
        """Retrieve a project by name."""
        pass

    @abstractmethod
    def list_projects(self) -> List['Project']:
        """List all projects."""
        pass

    @abstractmethod
    def update_project(self, project: 'Project'):
        """Update an existing project."""
        pass

    @abstractmethod
    def set_current_project(self, name: str):
        """Set the current project by name."""
        pass

    @abstractmethod
    def save_current_project(self):
        """Save the current project."""
        pass

    @abstractmethod
    def update_current_project_videos(self, videos: List[str]):
        """Update the current project's videos."""
        pass

    @abstractmethod
    def update_current_project_effects(self, effects: List[str]):
        """Update the current project's effects."""
        pass

class ProjectService(IProjectService):
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