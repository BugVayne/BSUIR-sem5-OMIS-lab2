from typing import List
from datetime import datetime


class Project:
    def __init__(self, name: str, videos: List[str] = None, effects: List[str] = None,  creationdate = datetime.now(), lastmodified = datetime.now() ):
        self.name = name
        self.videos = videos or []
        self.effects = effects or []
        self.creation_date = creationdate
        self.last_modified = lastmodified

    def update_last_modified(self):
        self.last_modified = datetime.now()

    def __repr__(self):
        return f"Project(name={self.name}, videos={self.videos}, effects={self.effects},  creation_date={self.creation_date}, last_modified={self.last_modified})\n"