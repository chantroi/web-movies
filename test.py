from pydantic import BaseModel


class Movie(BaseModel):
    title: str
    year: int
    rating: float
    director: str
    actors: list[str]
    genres: list[str]
    plot: str