import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI')

# Webhook Configuration
WEBHOOK_VERIFY_TOKEN = os.getenv('WEBHOOK_VERIFY_TOKEN')

# Application Configuration
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
PORT = int(os.getenv('PORT', 5000))

# Validation Configuration
REQUIRED_FIELDS = [
    'full_name',
    'passport_number',
    'email',
    'phone_number',
    'travel_date',
    'destination'
]

# Response Messages
WELCOME_MESSAGE = """
Welcome to the Airline Digital Advisor! 👋

I can help you book your flight by validating your information. Please provide:

1. Your full name
2. Passport number
3. Email address
4. Phone number
5. Travel date (YYYY-MM-DD)
6. Destination

You can send this information in a single message or step by step. I'll guide you through the process!
"""

VALIDATION_SUCCESS = """
Great! I've validated all your information successfully. ✅

Your booking request is being processed. You'll receive a confirmation shortly.

Need anything else? Just let me know!
"""

VALIDATION_ERROR = """
I need some additional information to process your booking. Please provide the following details:

{missing_fields}

Make sure to format the information correctly!
"""

# Supported Audio Formats
SUPPORTED_AUDIO_FORMATS = ['.mp3', '.wav', '.ogg', '.m4a', '.opus'] 