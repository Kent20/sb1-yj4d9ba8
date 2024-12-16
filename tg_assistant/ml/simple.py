import random
from typing import List
from .base import BaseResponseGenerator

class SimpleResponseGenerator(BaseResponseGenerator):
    """A simple response generator that uses predefined responses"""
    
    def __init__(self):
        self.responses = [
            "Thanks for your message!",
            "I understand.",
            "That's interesting.",
            "Could you tell me more?",
            "I see what you mean.",
            "Let me think about that.",
            "That's a good point.",
            "I appreciate your perspective.",
        ]
    
    def generate_responses(self, message: str, num_responses: int = 3) -> List[str]:
        """Generate simple responses by randomly selecting from predefined list"""
        return random.sample(
            self.responses,
            min(num_responses, len(self.responses))
        )