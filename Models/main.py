import speech_recognition as sr
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from sklearn.linear_model import LinearRegression
import numpy as np
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    return ""

def process_command(command):
    tokens = word_tokenize(command.lower())
    if 'balance' in tokens:
        return 'balance'
    elif 'last' in tokens and 'transactions' in tokens:
        return 'last_transactions'
    elif 'saving' in tokens and ('goal' in tokens or 'progress' in tokens):
        return 'savings_goal'
    else:
        return 'unknown'
# Simulated data for balance and transactions
transactions = np.array([[1, 100], [2, 150], [3, 200]])
balance = 500

# Linear regression model for predicting future balance
X = transactions[:, 0].reshape(-1, 1)
y = transactions[:, 1]
model = LinearRegression()
model.fit(X, y)

def predict_balance(next_transaction):
    next_transaction_id = next_transaction + 1
    return model.predict([[next_transaction_id]])[0]


def main():
    while True:
        command = listen()
        action = process_command(command)

        if action == 'balance':
            print(f"Your current balance is: ${balance}")
        elif action == 'last_transactions':
            print("Your last three transactions:")
            for transaction in transactions[-3:]:
                print(f"- Transaction ID: {transaction[0]}, Amount: ${transaction[1]}")
        elif action == 'savings_goal':
            print("Your progress towards your savings goal:")
            # Implement logic to calculate progress towards savings goal
            # For simplicity, let's assume a fixed savings goal
            savings_goal = 1000
            current_savings = sum(transactions[:, 1])
            progress = (current_savings / savings_goal) * 100
            print(f"- Current savings: ${current_savings}")
            print(f"- Progress towards goal: {progress:.2f}%")
        else:
            print("Sorry, I didn't understand that command.")


if __name__ == "__main__":
    main()
