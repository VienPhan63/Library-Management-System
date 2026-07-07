
from pydantic import BaseModel

class RegisterRequest(BaseModel):

    full_name: str
    email: str
    password: str
    phone_number: str
    gender: str