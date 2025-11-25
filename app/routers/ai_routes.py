from fastapi import APIRouter, HTTPException, status
from app.models.requests import (
    DescribePlaylistRequest,
    RecommendSongsRequest,
    GeneratePlaylistNameRequest,
    AnalyzeMoodRequest,
    SemanticSearchRequest
)
from app.models.responses import (
    DescribePlaylistResponse,
    RecommendSongsResponse,
    GeneratePlaylistNameResponse,
    AnalyzeMoodResponse,
    SemanticSearchResponse
)
from app.services.ai_service import AIService
from app.utils.logger import setup_logger


router = APIRouter()
logger = setup_logger(__name__)
ai_service = AIService()


@router.post(
    "/describe-playlist",
    response_model=DescribePlaylistResponse,
    summary="Generate playlist description",
    description="Generate a creative, engaging description for a playlist based on its songs"
)
async def describe_playlist(request: DescribePlaylistRequest):
    """Generate a playlist description using AI"""
    try:
        return await ai_service.describe_playlist(request.songs)
    except Exception as e:
        logger.error(f"Error describing playlist: {str(e)}")
        raise


@router.post(
    "/recommend-songs",
    response_model=RecommendSongsResponse,
    summary="Get song recommendations",
    description="Get AI-powered song recommendations based on current playlist"
)
async def recommend_songs(request: RecommendSongsRequest):
    """Get song recommendations using AI"""
    try:
        return await ai_service.recommend_songs(
            request.current_songs,
            request.number_of_recommendations
        )
    except Exception as e:
        logger.error(f"Error recommending songs: {str(e)}")
        raise


@router.post(
    "/generate-name",
    response_model=GeneratePlaylistNameResponse,
    summary="Generate playlist names",
    description="Generate creative names for a playlist in different styles"
)
async def generate_playlist_name(request: GeneratePlaylistNameRequest):
    """Generate playlist names using AI"""
    try:
        return await ai_service.generate_playlist_name(
            request.songs,
            request.style
        )
    except Exception as e:
        logger.error(f"Error generating playlist names: {str(e)}")
        raise


@router.post(
    "/analyze-mood",
    response_model=AnalyzeMoodResponse,
    summary="Analyze playlist mood",
    description="Analyze the mood and emotional character of a playlist"
)
async def analyze_mood(request: AnalyzeMoodRequest):
    """Analyze playlist mood using AI"""
    try:
        return await ai_service.analyze_mood(request.songs)
    except Exception as e:
        logger.error(f"Error analyzing mood: {str(e)}")
        raise


@router.post(
    "/semantic-search",
    response_model=SemanticSearchResponse,
    summary="Semantic music search",
    description="Search for songs using natural language descriptions"
)
async def semantic_search(request: SemanticSearchRequest):
    """Perform semantic search using AI"""
    try:
        return await ai_service.semantic_search(request.query, request.limit)
    except Exception as e:
        logger.error(f"Error in semantic search: {str(e)}")
        raise

