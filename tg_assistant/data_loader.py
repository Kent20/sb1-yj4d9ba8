import json
from typing import List, Dict
from pathlib import Path

class DialogueDataLoader:
    def __init__(self, data_path: str):
        self.data_path = Path(data_path)
    
    def load_dialogues(self) -> List[Dict]:
        """
        Load dialogue data from a JSON file
        Returns a list of dialogue dictionaries
        """
        try:
            with open(self.data_path, 'r', encoding='utf-8') as file:
                dialogues = json.load(file)
            return self._validate_and_process_dialogues(dialogues)
        except FileNotFoundError:
            raise FileNotFoundError(f"Dialogue file not found at {self.data_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in file {self.data_path}")
    
    def _validate_and_process_dialogues(self, dialogues: List[Dict]) -> List[Dict]:
        """
        Validate and process the dialogue data
        """
        processed_dialogues = []
        required_fields = {'message', 'sender', 'timestamp'}
        
        for dialogue in dialogues:
            if not isinstance(dialogue, dict):
                continue
            
            if not all(field in dialogue for field in required_fields):
                continue
                
            processed_dialogues.append({
                'message': str(dialogue['message']),
                'sender': str(dialogue['sender']),
                'timestamp': str(dialogue['timestamp']),
                'context': dialogue.get('context', ''),
            })
            
        return processed_dialogues