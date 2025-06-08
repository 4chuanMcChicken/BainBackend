import json
from typing import Dict, Tuple
import openai
from openai import AsyncOpenAI
from loguru import logger
from fastapi import HTTPException

from app.core.config import settings

# Initialize OpenAI client
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_PROMPT = """You are an address cleaning service. Your task is to:
1. Remove email addresses, postal codes, and extraneous tokens
2. Correct obvious typos in street or city names
3. Do NOT count simple removals (like stripping zip codes) as corrections
4. Return only valid JSON in the specified format

Example corrections that should set corrected=true:
- "toooooronto" → "Toronto"
- "vancuver" → "Vancouver"
- "New Yrok" → "New York"

Example cleanings that should set corrected=false:
- "Toronto, M5V 2T6" → "Toronto"
- "email@example.com 123 Main St" → "123 Main St"
"""

async def clean_addresses(source: str, destination: str) -> Dict[str, any]:
    """
    Clean and correct addresses using OpenAI
    
    Args:
        source: Source address
        destination: Destination address
        
    Returns:
        Dictionary containing cleaned addresses and correction flags
        
    Raises:
        HTTPException: If the OpenAI response format is invalid
    """
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": f"""
        Please clean and normalize the following user inputs before geocoding:

        Source: {source}
        Destination: {destination}

        Instructions:
        - Strip out any email addresses, postal codes, or other non–place tokens; these removals do **not** count as corrections.
        - Only if you correct an actual typo or replace a wrong place name (e.g. “toooooooronto” → “Toronto”) should you set the corresponding `…Corrected` flag to `true`.
        - If the original place name is already valid or you’ve only removed extraneous tokens, set the `…Corrected` flags to `false`.
        - Return **only** valid JSON, exactly in this format:

        {{
        "source": "<cleaned_source>",
        "destination": "<cleaned_destination>",
        "sourceCorrected": true|false,
        "destinationCorrected": true|false
        }}
        """
                }
            ],
            temperature=0,
            max_tokens=150,
            timeout=5
        )

        
        # Extract the response text
        result_text = response.choices[0].message.content.strip()
        
        try:
            # Parse the JSON response
            result = json.loads(result_text)
            
            # Validate required fields
            required_fields = ["source", "destination", "sourceCorrected", "destinationCorrected"]
            if not all(field in result for field in required_fields):
                raise ValueError("Missing required fields in response")
                
            return result
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Invalid format from OpenAI: {str(e)}\nResponse: {result_text}")
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "INVALID_OPENAI_FORMAT",
                    "message": "Invalid response format from address cleaning service"
                }
            )
            
    except Exception as e:
        # Log warning and fall back to original addresses
        logger.warning(f"Error cleaning addresses with OpenAI: {str(e)}")
        return {
            "source": source,
            "destination": destination,
            "sourceCorrected": False,
            "destinationCorrected": False
        } 