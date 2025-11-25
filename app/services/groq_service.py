from groq import Groq
import json
import asyncio
from typing import Dict, Any, Optional
from app.config import settings
from app.utils.exceptions import ClaudeAPIException, RateLimitException
from app.utils.logger import setup_logger


logger = setup_logger(__name__)


class GroqService:
    """Service for interacting with Groq API"""
    
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL
        self.max_tokens = settings.GROQ_MAX_TOKENS
    
    async def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 1.0,
        json_mode: bool = False
    ) -> str:
        """
        Generate a completion using Groq API
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature (0-1)
            json_mode: If True, instructs Groq to return only JSON
            
        Returns:
            The generated text response
        """
        try:
            logger.info(f"Generating completion with model {self.model}")
            
            messages = []
            
            # Prepare system and user prompts
            system_content = system_prompt or ""
            user_content = prompt
            
            # Add JSON mode instruction if requested
            if json_mode:
                json_instruction = "\n\nIMPORTANT: You must respond with valid JSON only, no markdown, no code blocks, just raw JSON."
                if system_content:
                    system_content = system_content + json_instruction
                else:
                    user_content = user_content + json_instruction
            
            if system_content:
                messages.append({"role": "system", "content": system_content})
            
            messages.append({"role": "user", "content": user_content})
            
            kwargs: Dict[str, Any] = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": self.max_tokens,
            }
            
            # Add JSON mode if requested (Groq supports response_format)
            if json_mode:
                kwargs["response_format"] = {"type": "json_object"}
            
            # Run synchronous API call in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.chat.completions.create(**kwargs)
            )
            
            # Extract text from response (OpenAI format)
            content = response.choices[0].message.content
            
            logger.info("Completion generated successfully")
            return content
            
        except Exception as e:
            error_str = str(e)
            # Check for rate limit errors
            if "rate limit" in error_str.lower() or "429" in error_str:
                logger.error(f"Rate limit error: {error_str}")
                raise RateLimitException()
            # Check for API errors
            elif "api" in error_str.lower() or "401" in error_str or "403" in error_str:
                logger.error(f"Groq API error: {error_str}")
                raise ClaudeAPIException(f"Groq API Error: {error_str}")
            else:
                logger.error(f"Unexpected error: {error_str}")
                raise ClaudeAPIException(f"Unexpected error: {error_str}")
    
    async def generate_json_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 1.0
    ) -> Dict[str, Any]:
        """
        Generate a completion and parse it as JSON
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            
        Returns:
            Parsed JSON response as dictionary
        """
        response = await self.generate_completion(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            json_mode=True
        )
        
        try:
            # Try to extract JSON from code blocks if present
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            elif "```" in response:
                json_start = response.find("```") + 3
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            else:
                json_str = response.strip()
            
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {response}")
            raise ClaudeAPIException(f"Failed to parse JSON response: {str(e)}")

