# Making sure the data coming from the front end is validated
"""
I always insist on using schemas to have full control of the data flow from fe -> be.
"""



# schemas.py

from pydantic import BaseModel
from typing import List, Dict

class TranslationRequestSchema(BaseModel):
    text: str
    languages: List[str]


class TaskResponseSchema(BaseModel):
    task_id: int

class TranslationStatusSchema(BaseModel):
    task_id: int
    status: str
    translations: Dict[str, str]