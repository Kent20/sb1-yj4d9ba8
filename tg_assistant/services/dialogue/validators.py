"""
Validators for dialogue import data
"""
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class DialogueValidator:
    @staticmethod
    def validate_json_structure(data: Dict) -> bool:
        """Validate the JSON structure matches Telegram export format"""
        try:
            if not isinstance(data, dict):
                return False
                
            # Check for required fields
            required_fields = {'id', 'type', 'messages'}
            if not all(field in data for field in required_fields):
                return False
                
            if not isinstance(data['messages'], list):
                return False

            # Validate message structure
            for msg in data['messages']:
                if not isinstance(msg, dict):
                    return False
                if 'type' not in msg:
                    return False
                    
            return True
            
        except Exception as e:
            logger.error(f"Error validating JSON structure: {str(e)}")
            return False