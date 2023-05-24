from datetime import datetime
from typing import List
from pydantic import BaseModel


class TaskBaseSchema(BaseModel):
    id_category: int
    status: int 
    name: str
    description:str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ListNoteResponse(BaseModel):
    status: str
    results: int
    notes: List[TaskBaseSchema]

class Item(BaseModel):
    id: str
    title: str
    description: str | None = None
