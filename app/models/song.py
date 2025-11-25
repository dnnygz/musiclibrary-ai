from pydantic import BaseModel, Field
from typing import Optional


class Song(BaseModel):
    """Represents a song in the music library"""
    id: str
    title: str
    artist: str
    album: Optional[str] = None
    genre: Optional[str] = None
    year: Optional[int] = None
    duration: int  # in seconds
    lyrics: Optional[str] = None
    image_url: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Bohemian Rhapsody",
                "artist": "Queen",
                "album": "A Night at the Opera",
                "genre": "Rock",
                "year": 1975,
                "duration": 354
            }
        }

