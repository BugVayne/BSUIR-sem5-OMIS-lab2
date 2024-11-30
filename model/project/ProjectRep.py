import json
import os
from datetime import datetime
from typing import List

from config import DB_PATH
from model.project.Project import Project


# Helper functions
def datetime_to_str(dt: datetime) -> str:
    """Converts a datetime object to an ISO 8601 string."""
    return dt.isoformat() if dt else None


def str_to_datetime(dt_str: str) -> datetime:
    """Converts an ISO 8601 string to a datetime object."""
    return datetime.fromisoformat(dt_str) if dt_str else None


class ProjectRepository:
    def __init__(self, db_file=DB_PATH):
        self.db_file = db_file
        if not os.path.exists(self.db_file):
            with open(self.db_file, "w") as db:
                json.dump([], db)

    def load_projects(self) -> List['Project']:
        try:
            with open(self.db_file, "r") as db:
                data = json.load(db)  # Attempt to load JSON data
            return [
                Project(
                    name=proj["name"],
                    videos=proj.get("videos", []),
                    effects=proj.get("effects", []),
                    creationdate=str_to_datetime(proj["creation_date"]),
                    lastmodified=str_to_datetime(proj["last_modified"]),
                )
                for proj in data
            ]
        except (json.JSONDecodeError, FileNotFoundError):
            # Handle empty or corrupt JSON file by returning an empty list
            return []

    def save_projects(self, projects: List['Project']):
        """
        Saves a list of Project objects to the JSON file.
        """
        with open(self.db_file, "w") as db:
            json.dump(
                [
                    {
                        "name": proj.name,
                        "videos": proj.videos,
                        "effects": proj.effects,
                        "creation_date": datetime_to_str(proj.creation_date),
                        "last_modified": datetime_to_str(proj.last_modified),
                    }
                    for proj in projects
                ],
                db,
                indent=4
            )

    def add_project(self, project: 'Project'):
        """
        Adds a new Project to the repository and saves it.
        """
        projects = self.load_projects()
        projects.append(project)
        self.save_projects(projects)

    def delete_project(self, project_name: str):
        """
        Deletes a Project by name from the repository and saves the changes.
        """
        projects = [proj for proj in self.load_projects() if proj.name != project_name]
        self.save_projects(projects)

    def get_project(self, project_name: str) -> 'Project':
        """
        Retrieves a Project by name from the repository.
        Returns None if no project with the given name exists.
        """
        for project in self.load_projects():
            if project.name == project_name:
                return project
        return None

    def update_project(self, updated_project: 'Project'):
        """
        Updates an existing Project in the repository and saves the changes.
        """
        projects = self.load_projects()
        for i, project in enumerate(projects):
            if project.name == updated_project.name:
                projects[i] = updated_project
                break
        else:
            raise ValueError(f"\033[91m[ProjectRep] Project with name '{updated_project.name}' not found.\033[0m")
        self.save_projects(projects)

if __name__ == "__main__":
    # Example usage
    repo = ProjectRepository()

    # Create a new project
    new_project = Project(name="My First Project", videos=["video1.mp4"], effects=["fade", "blur"])
    repo.add_project(new_project)

    # Load and print all projects
    projects = repo.load_projects()
    print(projects)

    # Get a specific project
    project = repo.get_project("My First Project")
    print(project)

    # Update a project
    if project:
        project.videos.append("video2.mp4")
        project.update_last_modified()  # Update the last_modified timestamp
        repo.update_project(project)

    # Delete a project
    # repo.delete_project("My First Project")