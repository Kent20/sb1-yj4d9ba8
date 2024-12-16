# Telegram Assistant

A Django-based Telegram assistant that learns from dialogue data and suggests responses based on the conversation context.

## Features

- Load and process dialogue data from JSON files
- Connect to Telegram account without marking messages as read
- Generate response suggestions using a pre-trained language model
- Modular and maintainable code structure

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
- Copy `config/.env.example` to `config/.env`
- Fill in your Telegram API credentials:
  - API_ID: Your Telegram API ID
  - API_HASH: Your Telegram API hash
  - PHONE: Your phone number
  - SESSION_NAME: Name for your session file

3. Prepare your dialogue data:
Create a JSON file with your dialogue data in the following format:
```json
[
  {
    "message": "Hello!",
    "sender": "user123",
    "timestamp": "2023-11-15T10:00:00",
    "context": "greeting"
  }
]
```

## Usage

Run the assistant:
```bash
python main.py
```

## Project Structure

- `tg_assistant/`
  - `data_loader.py`: Handles loading and processing dialogue data
  - `telegram_client.py`: Manages Telegram connection and message handling
  - `response_model.py`: Generates response suggestions using ML model
- `config/`: Configuration files and environment variables
- `main.py`: Main application entry point
- `requirements.txt`: Project dependencies