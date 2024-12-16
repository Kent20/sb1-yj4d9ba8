"""
Service for generating responses using ML models
"""
from typing import List, Optional
from ..ml.base import BaseResponseGenerator
from ..ml.simple import SimpleResponseGenerator
import logging

logger = logging.getLogger(__name__)

class ResponseService:
    def __init__(self):
        # Try to use transformer model if available
        try:
            from ..ml.transformer import TransformerResponseGenerator
            self.generator = TransformerResponseGenerator()
        except ImportError:
            logger.info("Using simple response generator (transformers not available)")
            self.generator = SimpleResponseGenerator()

    async def generate_responses(
        self,
        message: str,
        context: Optional[List[str]] = None,
        num_responses: int = 3
    ) -> List[str]:
        """Generate response suggestions for a message"""
        try:
            if context:
                # Add context to the message
                full_message = "\n".join([*context[-3:], message])
            else:
                full_message = message

            return self.generator.generate_responses(
                full_message,
                num_responses=num_responses
            )
            
        except Exception as e:
            logger.error(f"Error generating responses: {str(e)}")
            return []