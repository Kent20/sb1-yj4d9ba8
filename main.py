import asyncio
import logging
from tg_assistant.data_loader import DialogueDataLoader
from tg_assistant.telegram_client import TelegramAssistant
from tg_assistant.response_model import ResponseGenerator

async def main():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize components
    data_loader = DialogueDataLoader("path/to/your/dialogues.json")
    response_generator = ResponseGenerator()
    telegram_assistant = TelegramAssistant()
    
    try:
        # Load dialogue data
        dialogues = data_loader.load_dialogues()
        logging.info(f"Loaded {len(dialogues)} dialogues")
        
        # Set up response generator
        telegram_assistant.set_response_generator(response_generator.generate_responses)
        
        # Start the Telegram client
        await telegram_assistant.start()
        logging.info("Telegram assistant started")
        
        # Keep the program running
        await asyncio.Event().wait()
        
    except Exception as e:
        logging.error(f"Error: {str(e)}")
    finally:
        await telegram_assistant.stop()

if __name__ == "__main__":
    asyncio.run(main())