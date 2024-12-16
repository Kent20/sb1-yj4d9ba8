"""
Service for generating response suggestions
"""
from typing import List
from ...ml.simple import SimpleResponseGenerator

class ResponseService:
    def __init__(self):
        self.generator = SimpleResponseGenerator()
        
    def generate_responses(self, message: str = "", num_responses: int = 3) -> List[str]:
        """Generate response suggestions"""
        try:
            # Generate responses based on message context
            responses = self.generator.generate_responses(message, num_responses)
            
            # Ensure we always return something
            if not responses:
                responses = [
                    "Спасибо за сообщение!",
                    "Хорошо, я понял.",
                    "Давайте обсудим подробнее."
                ]
                
            return responses[:num_responses]
            
        except Exception as e:
            # Fallback responses in case of error
            return [
                "Извините, не удалось сгенерировать ответ",
                "Попробуйте позже",
                "Произошла ошибка при генерации"
            ]