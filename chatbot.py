import sqlite3
import datetime
import re
import spacy
# Load the spaCy English language model
nlp = spacy.load("en_core_web_sm")
# Connect to the SQLite database
conn = sqlite3.connect('chatbot_database.db')
c = conn.cursor()
# Function to add an event to the schedule
def add_event(date, event):
    c.execute("INSERT INTO Schedule (date, event) VALUES (?, ?)", (date, event))
    conn.commit()
    print("Event added to the schedule.")
# Function to retrieve schedule for a given date
def get_schedule(date):
    c.execute("SELECT event FROM Schedule WHERE date=?", (date,))
    events = c.fetchall()
    if events:
        print("Events for {}: ".format(date))
        for event in events:
            print("- " + event[0])
    else:
        print("No events found for {}.".format(date))
# Function to add mood for a given date
def add_mood(date, mood):
    c.execute("INSERT INTO Mood (date, mood) VALUES (?, ?)", (date, mood))
    conn.commit()
    print("Mood added.")
# Function to detect date from user input
def extract_date(input_text):
    match = re.search(r'\b(\d{4})-(\d{2})-(\d{2})\b', input_text)
    if match:
        return datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
    else:
        return None
# Function to analyze mood from user input
def analyze_mood(input_text):
    doc = nlp(input_text)
    for token in doc:
        if token.text.lower() in ['happy', 'joyful', 'excited', 'good']:
            return 'positive'
        elif token.text.lower() in ['sad', 'unhappy', 'depressed', 'bad']:
            return 'negative'
    return 'neutral'
# Main function to interact with the user
def main():
    print("Welcome to the Chatbot!")
    while True:
        user_input = input("You: ")
        # Add event to schedule
        if "add event" in user_input:
            date = extract_date(user_input)
            if date:
                event = input("What event would you like to add? ")
                add_event(date, event)
            else:
                print("Please provide a valid date (YYYY-MM-DD format).")
        # Get schedule for a given date
        elif "get schedule" in user_input:
            date = extract_date(user_input)
            if date:
                get_schedule(date)
            else:
                print("Please provide a valid date (YYYY-MM-DD format).")
        # Add mood for today
        elif "add mood" in user_input:
            mood = input("How are you feeling today? ")
            add_mood(datetime.date.today(), mood)
        # Analyze mood from user input
        elif "analyze mood" in user_input:
            mood = analyze_mood(user_input)
            print("Detected mood: " + mood)
        # Exit the chatbot
        elif "exit" in user_input:
            print("Goodbye!")
            break
        else:
            print("I'm sorry, I didn't understand that.")
if __name__ == "__main__":
    main()
