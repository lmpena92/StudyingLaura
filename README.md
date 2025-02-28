# Airline Digital Advisor

A WhatsApp-based digital advisor system that validates user information for airline reservations through text and voice messages.

## Features

- WhatsApp message integration (text and voice)
- Natural Language Processing for text analysis
- Speech-to-text conversion for voice messages
- User information validation
- Secure data storage
- Booking validation workflow

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your credentials:
   ```
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   MONGODB_URI=your_mongodb_uri
   ```
5. Run the application:
   ```bash
   python app.py
   ```

## Required Environment Variables

- `TWILIO_ACCOUNT_SID`: Your Twilio Account SID
- `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token
- `MONGODB_URI`: MongoDB connection string

## Project Structure

```
.
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Project dependencies
├── .env                 # Environment variables (not in repo)
└── modules/
    ├── whatsapp.py      # WhatsApp integration
    ├── nlp.py           # Natural Language Processing
    ├── speech.py        # Speech-to-text processing
    ├── validator.py     # User information validation
    └── database.py      # Database operations
``` 