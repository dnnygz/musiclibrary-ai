from typing import List, Dict
from app.models.song import Song


def format_songs_for_prompt(songs: List[Song]) -> str:
    """Format songs list into a readable string for prompts"""
    
    formatted = []
    for i, song in enumerate(songs, 1):
        parts = [f"{i}. '{song.title}' by {song.artist}"]
        
        if song.album:
            parts.append(f"from the album '{song.album}'")
        if song.genre:
            parts.append(f"({song.genre})")
        if song.year:
            parts.append(f"[{song.year}]")
        
        formatted.append(" ".join(parts))
    
    return "\n".join(formatted)


def format_duration(seconds: int) -> str:
    """Convert seconds to MM:SS format"""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"


def extract_decades(songs: List[Song]) -> List[str]:
    """Extract unique decades from songs"""
    decades = set()
    for song in songs:
        if song.year:
            decade = (song.year // 10) * 10
            decades.add(f"{decade}s")
    return sorted(list(decades))


def extract_genres(songs: List[Song]) -> List[str]:
    """Extract unique genres from songs"""
    genres = set()
    for song in songs:
        if song.genre:
            genres.add(song.genre)
    return sorted(list(genres))


def get_dominant_genre(songs: List[Song]) -> str:
    """Get the most common genre from songs"""
    genre_counts: Dict[str, int] = {}
    
    for song in songs:
        if song.genre:
            genre_counts[song.genre] = genre_counts.get(song.genre, 0) + 1
    
    if not genre_counts:
        return "Mixed"
    
    return max(genre_counts, key=genre_counts.get)


def calculate_total_duration(songs: List[Song]) -> int:
    """Calculate total duration of songs in seconds"""
    return sum(song.duration for song in songs)

