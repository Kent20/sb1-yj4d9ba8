"""
Chat type mapping utilities
"""
class ChatMapper:
    @staticmethod
    def map_chat_type(chat_type: str) -> str:
        """Map Telegram chat type to internal type"""
        type_mapping = {
            'private': 'user',
            'personal_chat': 'user', 
            'group': 'group',
            'supergroup': 'group',
            'channel': 'channel',
            'saved_messages': 'user'
        }
        return type_mapping.get(chat_type, 'unknown')