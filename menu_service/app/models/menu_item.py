from pydantic import BaseModel
from uuid import uuid4 

class MenuItem(BaseModel):
    id: str = None 
    name: str
    description: str
    price: float
    type: str

    def __init__(self, **data):
        super().__init__(**data)
        if self.id is None:
            self.id = str(uuid4()) 
