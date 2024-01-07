from pydantic import BaseModel

class Artists(BaseModel):
    ids: list[str]

class Tracks(BaseModel):
    ids: list[str]

class Albums(BaseModel):
    ids: list[str]