from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    title: str

 #Как FastAPI регает инфо
class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    is_done: bool
