"""
Prompts for song recommendation feature
"""
from typing import List
from app.models import Song


def create_system_prompt() -> str:
    """Create the system prompt for song recommendations"""
    return """You are a music recommendation expert. Your task is to recommend songs that complement a given playlist.

CRITICAL: You must respond with ONLY valid JSON in this exact format:
{
  "recommendations": [
    {
      "title": "Song Title",
      "artist": "Artist Name",
      "album": "Album Name",
      "genre": "Genre",
      "year": 2020,
      "reason": "Brief explanation of why this song fits"
    }
  ]
}

Rules:
- Return ONLY the JSON object, no markdown, no code blocks, no explanations
- Each recommendation must have: title, artist, album, genre, year (number), reason (string)
- Make recommendations that match the style, mood, and era of the input songs
- Provide diverse but coherent recommendations"""


def create_recommend_songs_prompt(songs: List[Song], number: int) -> str:
    """Create the user prompt for song recommendations"""
    
    # Format songs for the prompt
    songs_list = []
    for i, song in enumerate(songs[:10], 1):  # Limit to 10 songs to save tokens
        song_info = f"{i}. '{song.title}' by {song.artist}"
        if song.genre:
            song_info += f" ({song.genre})"
        if song.year:
            song_info += f" [{song.year}]"
        songs_list.append(song_info)
    
    songs_text = "\n".join(songs_list)
    
    return f"""Based on this playlist:

{songs_text}

Recommend exactly {number} songs that would fit well with this collection.

Your response must be ONLY this JSON format (no markdown, no code blocks):
{{
  "recommendations": [
    {{
      "title": "Recommended Song",
      "artist": "Artist Name",
      "album": "Album Name",
      "genre": "Genre",
      "year": 2020,
      "reason": "Why it fits"
    }}
  ]
}}

Generate exactly {number} recommendations now:"""