from pydantic import BaseModel, Field
from typing import List
from app.models.song import Song


class DescribePlaylistResponse(BaseModel):
    """Response with playlist description"""
    description: str = Field(..., description="AI-generated playlist description")


class SongRecommendation(BaseModel):
    """A single song recommendation"""
    title: str
    artist: str
    reason: str = Field(..., description="Why this song was recommended")


class RecommendSongsResponse(BaseModel):
    """Response with song recommendations"""
    recommendations: List[SongRecommendation]


class GeneratePlaylistNameResponse(BaseModel):
    """Response with generated playlist names"""
    names: List[str] = Field(..., min_length=3, max_length=3, description="Three generated playlist names")


class AnalyzeMoodResponse(BaseModel):
    """Response with mood analysis"""
    moods: List[str] = Field(..., description="Identified moods/emotions")
    description: str = Field(..., description="Detailed mood description")


class SemanticSearchResponse(BaseModel):
    """Response with semantic search results"""
    songs: List[Song] = Field(..., description="Songs matching the semantic query")
    explanation: str = Field(..., description="Why these songs match the query")


class ErrorResponse(BaseModel):
    """Standard error response"""
    detail: str
    error_type: str = "error"

