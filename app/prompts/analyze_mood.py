from typing import List
from app.models import Song
from app.utils.helpers import format_songs_for_prompt, get_dominant_genre


def create_analyze_mood_prompt(songs: List[Song]) -> str:
    """Create prompt for analyzing mood"""
    
    songs_list = format_songs_for_prompt(songs)
    dominant_genre = get_dominant_genre(songs)
    
    prompt = f"""Analyze the mood and emotional character of this playlist:



{songs_list}



Main genre: {dominant_genre}

Number of songs: {len(songs)}



Provide:

1. A list of 3-5 mood tags/keywords (e.g., "energetic", "melancholic", "nostalgic", "uplifting", "intense")

2. A 2-3 sentence description of the overall emotional atmosphere



Consider:

- The musical characteristics (tempo, energy, instrumentation)

- The era and cultural context

- The typical emotional associations with these songs

- How the songs work together as a collection



Return your response as JSON with this exact structure:

{{

  "moods": ["mood1", "mood2", "mood3"],

  "description": "Overall emotional atmosphere description"

}}



Return ONLY the JSON object, no additional text, no markdown formatting, no code blocks."""

    return prompt


def create_system_prompt() -> str:
    """System prompt for mood analysis"""
    return """You are a music psychologist and mood analysis expert.
You understand how music affects emotions and can accurately identify the emotional character of songs and playlists.
You provide insightful, nuanced mood analyses that go beyond surface-level descriptions."""

