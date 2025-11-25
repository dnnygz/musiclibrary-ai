from typing import List
from app.models import Song
from app.utils.helpers import (
    format_songs_for_prompt,
    extract_decades,
    extract_genres,
    get_dominant_genre,
    calculate_total_duration,
    format_duration
)


def create_describe_playlist_prompt(songs: List[Song]) -> str:
    """Create prompt for describing a playlist"""
    
    songs_list = format_songs_for_prompt(songs)
    decades = extract_decades(songs)
    genres = extract_genres(songs)
    dominant_genre = get_dominant_genre(songs)
    total_duration = calculate_total_duration(songs)
    
    prompt = f"""You are a music curator and expert. I have a playlist with the following songs:



{songs_list}



Playlist Details:

- Total songs: {len(songs)}

- Total duration: {format_duration(total_duration)}

- Main genre: {dominant_genre}

- Genres present: {', '.join(genres) if genres else 'Various'}

- Decades represented: {', '.join(decades) if decades else 'Various'}



Generate a creative, engaging, and atmospheric description for this playlist. The description should:

1. Capture the overall mood and vibe of the collection

2. Highlight the musical era(s) and style(s)

3. Be 2-4 sentences long

4. Be written in an evocative, descriptive style (like you'd see on Spotify or Apple Music)

5. Make someone excited to listen to it



Write ONLY the description, no preamble or explanation."""

    return prompt


def create_system_prompt() -> str:
    """System prompt for playlist description"""
    return """You are an expert music curator with deep knowledge of music history, genres, and cultural context. 
You write compelling, evocative playlist descriptions that capture the essence and mood of music collections. 
Your descriptions are concise yet vivid, making listeners eager to press play."""

