from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from modules.whatsapp import (
    process_whatsapp_message,
    ask_for_new_date,
    format_flight_options,
    ask_for_booking_details,
    confirm_booking_details,
    provide_next_steps,
    handle_payment_confirmation
)
from modules.validator import validate_user_info
from modules.database import store_user_data, get_user_data, update_booking_status, get_user_bookings
from modules.nlp import extract_user_info
from modules.speech import convert_voice_to_text

# Load environment variables
load_dotenv()

app = Flask(__name__)

def handle_date_change_request(message_content, sender):
    """
    Handles a request to change the travel date.
    """
    # Get user's existing bookings
    bookings = get_user_bookings(sender)
    if not bookings:
        return "I couldn't find any existing bookings under your number. Would you like to make a new reservation?"
    
    # Ask for the new desired date
    return ask_for_new_date()

def handle_new_booking_request(sender):
    """
    Handles a new booking request.
    """
    return ask_for_booking_details()

def handle_flight_selection(message_content, user_info):
    """
    Handles flight option selection.
    """
    try:
        option = int(message_content)
        if 1 <= option <= 4:
            return confirm_booking_details(option, user_info)
        else:
            return "Please select a valid option number between 1 and 4."
    except ValueError:
        return "Please provide a valid option number between 1 and 4."

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Get the incoming WhatsApp message data
        data = request.get_json()
        
        # Process the incoming message
        message_type = data.get('type', 'text')
        message_content = data.get('message', '').lower()
        sender = data.get('sender', '')
        
        # Handle voice messages
        if message_type == 'voice':
            message_content = convert_voice_to_text(message_content)
        
        # Check message intent
        if any(phrase in message_content for phrase in ['change date', 'modify date', 'reschedule', 'new date']):
            response_message = handle_date_change_request(message_content, sender)
            process_whatsapp_message(sender, response_message, is_new_conversation=True)
            return jsonify({'status': 'success', 'message': 'Date change request processed'})
        
        if any(phrase in message_content for phrase in ['book flight', 'new reservation', 'make booking', 'book ticket']):
            response_message = handle_new_booking_request(sender)
            process_whatsapp_message(sender, response_message, is_new_conversation=True)
            return jsonify({'status': 'success', 'message': 'New booking request initiated'})
        
        # Handle payment confirmation
        if message_content.strip().lower() == 'yes':
            user_info = get_user_data(sender)
            if user_info and 'selected_flight' in user_info:
                response_message = handle_payment_confirmation(user_info, user_info['selected_flight'])
                process_whatsapp_message(sender, response_message)
                return jsonify({'status': 'success', 'message': 'Payment information sent'})
        
        # Check if this is a flight selection
        if message_content.isdigit():
            user_info = get_user_data(sender)
            if user_info:
                # Store the selected flight option
                user_info['selected_flight'] = int(message_content)
                store_user_data(sender, user_info)
                response_message = handle_flight_selection(message_content, user_info)
                process_whatsapp_message(sender, response_message)
                return jsonify({'status': 'success', 'message': 'Flight selection processed'})
        
        # Extract user information from the message
        user_info = extract_user_info(message_content)
        
        # Validate the extracted information
        validation_result = validate_user_info(user_info)
        
        if validation_result['is_valid']:
            # Store valid user information
            store_user_data(sender, user_info)
            
            # Show available flights
            response_message = format_flight_options(
                user_info['destination'],
                user_info['travel_date']
            )
        else:
            # Handle invalid information
            response_message = validation_result['message']
        
        # Process and send response through WhatsApp
        process_whatsapp_message(sender, response_message)
        
        return jsonify({'status': 'success', 'message': 'Webhook processed successfully'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/webhook', methods=['GET'])
def verify():
    # Handle WhatsApp webhook verification
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode and token:
        if mode == 'subscribe' and token == os.getenv('WEBHOOK_VERIFY_TOKEN'):
            return challenge
        else:
            return 'Forbidden', 403
    
    return 'Bad Request', 400

if __name__ == '__main__':
    app.run(debug=True) 