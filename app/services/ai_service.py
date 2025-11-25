from typing import List
import uuid
from app.models.song import Song
from app.models.responses import (
    DescribePlaylistResponse,
    RecommendSongsResponse,
    SongRecommendation,
    GeneratePlaylistNameResponse,
    AnalyzeMoodResponse,
    SemanticSearchResponse
)
from app.services.groq_service import GroqService
from app.prompts.describe_playlist import (
    create_describe_playlist_prompt,
    create_system_prompt as describe_system_prompt
)
from app.prompts.recommend_songs import (
    create_recommend_songs_prompt,
    create_system_prompt as recommend_system_prompt
)
from app.prompts.generate_name import (
    create_generate_name_prompt,
    create_system_prompt as generate_name_system_prompt
)
from app.prompts.analyze_mood import (
    create_analyze_mood_prompt,
    create_system_prompt as analyze_mood_system_prompt
)
from app.prompts.semantic_search import (
    create_semantic_search_prompt,
    create_system_prompt as semantic_search_system_prompt
)
from app.utils.logger import setup_logger
from app.utils.exceptions import InvalidRequestException


logger = setup_logger(__name__)


class AIService:
    """Business logic for AI features"""
    
    def __init__(self):
        self.groq = GroqService()
    
    async def describe_playlist(self, songs: List[Song]) -> DescribePlaylistResponse:
        """Generate a creative description for a playlist"""
        logger.info(f"Generating description for playlist with {len(songs)} songs")
        
        if not songs:
            raise InvalidRequestException("Cannot describe an empty playlist")
        
        prompt = create_describe_playlist_prompt(songs)
        system_prompt = describe_system_prompt()
        
        description = await self.groq.generate_completion(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.8
        )
        
        return DescribePlaylistResponse(description=description.strip())
    
    async def recommend_songs(
        self,
        current_songs: List[Song],
        number_of_recommendations: int
    ) -> RecommendSongsResponse:
        """Generate song recommendations based on current playlist"""
        logger.info(f"Generating {number_of_recommendations} recommendations")
        
        if not current_songs:
            raise InvalidRequestException("Cannot generate recommendations for an empty playlist")
        
        prompt = create_recommend_songs_prompt(current_songs, number_of_recommendations)
        system_prompt = recommend_system_prompt()
        
        response_data = await self.groq.generate_json_completion(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.7
        )
        
        # FIX: Handle different response formats
        recommendations_list = []
        
        # Check if response_data is a dict with 'recommendations' key
        if isinstance(response_data, dict):
            if 'recommendations' in response_data:
                recommendations_list = response_data['recommendations']
            else:
                # If it's a dict but not in expected format, log and raise error
                logger.error(f"Unexpected dict format: {response_data}")
                raise InvalidRequestException("Invalid recommendation format from AI")
        # Check if response_data is already a list
        elif isinstance(response_data, list):
            recommendations_list = response_data
        else:
            logger.error(f"Unexpected response type: {type(response_data)}")
            raise InvalidRequestException("Invalid response format from AI")
        
        # Parse recommendations with error handling
        recommendations = []
        for i, rec in enumerate(recommendations_list):
            try:
                # Ensure it's a dict
                if isinstance(rec, str):
                    logger.error(f"Recommendation {i} is a string: {rec}")
                    continue
                
                # Validate required fields
                if not isinstance(rec, dict):
                    logger.error(f"Recommendation {i} is not a dict: {type(rec)}")
                    continue
                
                # Create SongRecommendation object
                recommendations.append(SongRecommendation(**rec))
            except Exception as e:
                logger.error(f"Failed to parse recommendation {i}: {e}")
                logger.error(f"Recommendation data: {rec}")
                continue
        
        if not recommendations:
            raise InvalidRequestException("No valid recommendations generated")
        
        return RecommendSongsResponse(recommendations=recommendations)
    
    async def generate_playlist_name(
        self,
        songs: List[Song],
        style: str
    ) -> GeneratePlaylistNameResponse:
        """Generate creative names for a playlist"""
        logger.info(f"Generating playlist names with style: {style}")
        
        if not songs:
            raise InvalidRequestException("Cannot generate names for an empty playlist")
        
        prompt = create_generate_name_prompt(songs, style)
        system_prompt = generate_name_system_prompt()
        
        response_data = await self.groq.generate_json_completion(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.9
        )
        
        # FIX: Handle different response formats
        names = []
        
        if isinstance(response_data, list):
            # Response is directly a list
            names = response_data
        elif isinstance(response_data, dict):
            # Check for common keys
            if 'names' in response_data:
                names = response_data['names']
            elif 'playlist_names' in response_data:
                names = response_data['playlist_names']
            elif 'suggestions' in response_data:
                names = response_data['suggestions']
            else:
                logger.error(f"Unexpected dict format: {response_data}")
                raise InvalidRequestException("Invalid name format from AI")
        else:
            logger.error(f"Unexpected response type: {type(response_data)}")
            raise InvalidRequestException("Invalid response format from AI")
        
        # Ensure we have exactly 3 names
        if len(names) < 3:
            logger.warning(f"Only {len(names)} names generated, expected 3")
            # Pad with generic names if needed
            while len(names) < 3:
                names.append(f"Playlist #{len(names) + 1}")
        elif len(names) > 3:
            logger.warning(f"{len(names)} names generated, truncating to 3")
            names = names[:3]
        
        # Ensure all names are strings
        names = [str(name).strip() for name in names if name]
        
        if len(names) != 3:
            raise InvalidRequestException("Expected exactly 3 playlist names")
        
        return GeneratePlaylistNameResponse(names=names)
    
    async def analyze_mood(self, songs: List[Song]) -> AnalyzeMoodResponse:
        """Analyze the mood and emotional character of songs"""
        logger.info(f"Analyzing mood for {len(songs)} songs")
        
        if not songs:
            raise InvalidRequestException("Cannot analyze mood of empty playlist")
        
        prompt = create_analyze_mood_prompt(songs)
        system_prompt = analyze_mood_system_prompt()
        
        response_data = await self.groq.generate_json_completion(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.6
        )
        
        return AnalyzeMoodResponse(
            moods=response_data['moods'],
            description=response_data['description']
        )
    
    async def semantic_search(self, query: str, limit: int) -> SemanticSearchResponse:
        """Search for songs using natural language"""
        logger.info(f"Performing semantic search: '{query}'")
        
        if len(query.strip()) < 3:
            raise InvalidRequestException("Search query too short")
        
        prompt = create_semantic_search_prompt(query)
        system_prompt = semantic_search_system_prompt()
        
        response_data = await self.groq.generate_json_completion(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.7
        )
        
        # Parse songs and limit results
        # Ensure all required fields are present
        songs = []
        for song_data in response_data['songs'][:limit]:
            # Generate ID if not provided
            if 'id' not in song_data or not song_data['id']:
                song_data['id'] = str(uuid.uuid4())
            # Ensure duration is present (default to 180 seconds if not provided)
            if 'duration' not in song_data or not song_data['duration']:
                song_data['duration'] = 180
            # Remove 'reason' field as it's not part of Song model
            song_data.pop('reason', None)
            songs.append(Song(**song_data))
        
        explanation = response_data.get('explanation', '')
        
        return SemanticSearchResponse(songs=songs, explanation=explanation)