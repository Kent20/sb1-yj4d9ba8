"""Base service class with common functionality"""
import logging
from typing import Optional, Tuple, TypeVar, Any

T = TypeVar('T')

class BaseService:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    async def handle_operation(
        self,
        operation: str,
        func: callable,
        *args,
        **kwargs
    ) -> Tuple[Optional[T], Optional[str]]:
        """Generic error handler for service operations"""
        try:
            result = await func(*args, **kwargs)
            return result, None
        except Exception as e:
            self.logger.error(f"Error in {operation}: {str(e)}")
            return None, str(e)