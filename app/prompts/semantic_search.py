def create_semantic_search_prompt(query: str) -> str:
    """Create prompt for semantic search"""
    
    prompt = f"""A user is searching for music with this description:

"{query}"



Based on this search query, generate a list of 10 songs that match what the user is looking for.



Consider:

- The mood, energy, and atmosphere implied by the query

- Any specific genres, eras, or styles mentioned or implied

- The context or use case (e.g., "for running", "to relax", "for a party")

- Both literal and metaphorical interpretations



For each song, briefly explain why it matches the search criteria.



Return your response as JSON with this exact structure:

{{

  "songs": [

    {{

      "id": "unique-song-id-or-placeholder",

      "title": "Song Title",

      "artist": "Artist Name",

      "album": "Album Name (if known, otherwise null)",

      "genre": "Genre",

      "year": year_as_number_or_null,

      "duration": duration_in_seconds,

      "reason": "Why this matches the search"

    }}

  ],

  "explanation": "Overall explanation of how these songs match the user's search"

}}



Return ONLY the JSON object, no additional text, no markdown formatting, no code blocks."""

    return prompt


def create_system_prompt() -> str:
    """System prompt for semantic search"""
    return """You are a music search and discovery expert with comprehensive knowledge of songs across all genres and eras.
You excel at understanding natural language queries and translating them into relevant song recommendations.
You consider both explicit and implicit criteria, mood, context, and cultural associations."""

