from pydantic import BaseModel


class Object(BaseModel):
    name: str
    age: int
    gender: str


print(Object(name="Natasha", age="28", gender="female").json())
