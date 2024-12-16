from abc import ABC, abstractmethod
from typing import List

class BaseResponseGenerator(ABC):
    """Base class for response generators"""
    
    @abstractmethod
    def generate_responses(self, message: str, num_responses: int = 3) -> List[str]:
        """Generate response suggestions for a given message"""
        pass