from pydantic import BaseModel, Field
from typing import List, Literal
from app.models.song import Song


class DescribePlaylistRequest(BaseModel):
    """Request to generate a playlist description"""
    songs: List[Song] = Field(..., min_length=1, description="List of songs in the playlist")
    
    class Config:
        json_schema_extra = {
            "example": {
                "songs": [
                    {
                        "id": "1",
                        "title": "Bohemian Rhapsody",
                        "artist": "Queen",
                        "genre": "Rock",
                        "year": 1975,
                        "duration": 354
                    }
                ]
            }
        }


class RecommendSongsRequest(BaseModel):
    """Request to get song recommendations"""
    current_songs: List[Song] = Field(..., min_length=1, description="Songs currently in the playlist")
    number_of_recommendations: int = Field(5, ge=1, le=20, description="Number of recommendations to generate")
    
    class Config:
        json_schema_extra = {
            "example": {
                "current_songs": [
                    {
                        "id": "1",
                        "title": "Bohemian Rhapsody",
                        "artist": "Queen",
                        "genre": "Rock",
                        "year": 1975,
                        "duration": 354
                    }
                ],
                "number_of_recommendations": 5
            }
        }


class GeneratePlaylistNameRequest(BaseModel):
    """Request to generate creative playlist names"""
    songs: List[Song] = Field(..., min_length=1, description="Songs in the playlist")
    style: Literal['creative', 'descriptive', 'fun'] = Field('creative', description="Style of name generation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "songs": [
                    {
                        "id": "1",
                        "title": "Bohemian Rhapsody",
                        "artist": "Queen",
                        "genre": "Rock",
                        "year": 1975,
                        "duration": 354
                    }
                ],
                "style": "creative"
            }
        }


class AnalyzeMoodRequest(BaseModel):
    """Request to analyze mood of songs"""
    songs: List[Song] = Field(..., min_length=1, description="Songs to analyze")
    
    class Config:
        json_schema_extra = {
            "example": {
                "songs": [
                    {
                        "id": "1",
                        "title": "Bohemian Rhapsody",
                        "artist": "Queen",
                        "genre": "Rock",
                        "year": 1975,
                        "duration": 354
                    }
                ]
            }
        }


class SemanticSearchRequest(BaseModel):
    """Request for semantic search of songs"""
    query: str = Field(..., min_length=3, max_length=500, description="Natural language search query")
    limit: int = Field(10, ge=1, le=50, description="Maximum number of results")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "upbeat songs for running in the morning",
                "limit": 10
            }
        }

