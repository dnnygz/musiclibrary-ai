"""
Prompts for playlist name generation feature
"""
from typing import List
from app.models import Song


def create_system_prompt() -> str:
    """Create the system prompt for playlist name generation"""
    return """You are a creative playlist naming expert. Your task is to generate catchy, memorable playlist names.

CRITICAL: You must respond with ONLY valid JSON in this exact format:
["Name 1", "Name 2", "Name 3"]

Rules:
- Return ONLY a JSON array with exactly 3 strings
- No markdown, no code blocks, no explanations
- Names should be creative and reflect the playlist's mood/theme
- Keep names concise (2-5 words typically)"""


def create_generate_name_prompt(songs: List[Song], style: str) -> str:
    """Create the user prompt for playlist name generation"""
    
    # Analyze songs to understand the theme
    genres = list(set([song.genre for song in songs if song.genre]))[:5]
    artists = list(set([song.artist for song in songs]))[:5]
    years = [song.year for song in songs if song.year]
    avg_year = sum(years) // len(years) if years else None
    
    # Format songs for context
    songs_list = []
    for i, song in enumerate(songs[:5], 1):  # Show first 5 songs
        songs_list.append(f"{i}. '{song.title}' by {song.artist}")
    
    songs_text = "\n".join(songs_list)
    
    context = f"""Playlist contains {len(songs)} songs
Main genres: {', '.join(genres) if genres else 'Various'}
Featured artists: {', '.join(artists[:3]) if artists else 'Various'}"""
    
    if avg_year:
        era = ""
        if avg_year < 1980:
            era = "Classic/Vintage"
        elif avg_year < 2000:
            era = "90s Era"
        elif avg_year < 2010:
            era = "2000s Era"
        else:
            era = "Modern/Recent"
        context += f"\nEra: {era} (avg. {avg_year})"
    
    style_descriptions = {
        "creative": "Creative and imaginative names with wordplay",
        "descriptive": "Clear, descriptive names that explain the content",
        "fun": "Fun, playful, and energetic names",
        "elegant": "Sophisticated and elegant names",
        "edgy": "Bold, edgy names with attitude"
    }
    
    style_desc = style_descriptions.get(style, "Creative and memorable names")
    
    return f"""Generate exactly 3 playlist names for this collection:

{context}

Sample songs:
{songs_text}

Style: {style_desc}

Your response must be ONLY this JSON array (no markdown, no code blocks, no explanations):
["First Name Here", "Second Name Here", "Third Name Here"]

Generate exactly 3 names now:"""