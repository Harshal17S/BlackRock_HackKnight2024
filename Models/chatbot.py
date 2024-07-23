# from flask import Flask, request, jsonify
# from twilio.twiml.messaging_response import MessagingResponse
# from twilio.rest import Client

# app = Flask(__name__)

# # Twilio configuration
# TWILIO_ACCOUNT_SID = 'ACc71260cf469e1cc8f4f0d7cfca04f7df'
# TWILIO_AUTH_TOKEN = 'ac28c444e2cbeeeda7a8c578e49f2a00'
# TWILIO_PHONE_NUMBER = '+15677071132'

# client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# # Placeholder for user data
# users = {
#     "user1": {"balance": 1000, "goal": 5000, "transactions": []}
# }

# # Function to get user ID from phone number (simple mapping for demonstration)
# phone_to_user = {
#     '+919527374289': 'user1'  # Replace with actual phone number and user ID mapping
# }

# # Function to send SMS via Twilio
# def send_sms(to, message):
#     client.messages.create(body=message, from_=TWILIO_PHONE_NUMBER, to=to)

# # Function to get balance
# def get_balance(user_id):
#     balance = users.get(user_id, {}).get('balance', 0)
#     return f"Your balance is ${balance}"

# # Function to set a goal
# def set_goal(user_id, goal):
#     if user_id in users:
#         users[user_id]['goal'] = goal
#         return f"Your savings goal of ${goal} has been set successfully"
#     else:
#         return "User not found"

# # Function to add a transaction
# def add_transaction(user_id, amount, description):
#     if user_id in users:
#         users[user_id]['transactions'].append({"amount": amount, "description": description})
#         users[user_id]['balance'] += amount
#         return f"Transaction of ${amount} for {description} has been added successfully"
#     else:
#         return "User not found"

# @app.route('/sms', methods=['POST'])
# def sms_reply():
#     from_number = request.form.get('From')
#     body = request.form.get('Body').lower()

#     user_id = phone_to_user.get(from_number, None)

#     if not user_id:
#         response = MessagingResponse()
#         response.message("User not recognized. Please register.")
#         return str(response)

#     if 'balance' in body:
#         message = get_balance(user_id)
#     elif 'set goal' in body:
#         goal = int(body.split('set goal ')[1])
#         message = set_goal(user_id, goal)
#     elif 'transaction' in body:
#         parts = body.split('transaction ')[1].split(' for ')
#         amount = float(parts[0])
#         description = parts[1]
#         message = add_transaction(user_id, amount, description)
#     else:
#         message = "I can help you with balance, setting goals, and transactions. Please use keywords: 'balance', 'set goal <amount>', 'transaction <amount> for <description>'."

#     response = MessagingResponse()
#     response.message(message)
#     return str(response)

# if __name__ == '__main__':
#     app.run(debug=True)
