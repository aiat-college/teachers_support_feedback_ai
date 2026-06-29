from pydantic import BaseModel

class RequestModel(BaseModel):
    school: str
    start_date: str
    end_date: str