import json
import random
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import nltk
import ssl
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
nltk.download('punkt', download_dir='/path/to/nltk_data')
nltk.download('stopwords', download_dir='/path/to/nltk_data')

class PersonalAI:
    def __init__(self):
        self.intents = json.loads(open('intents.json').read())
        self.knowledge_base = json.loads(open('knowledge_base.json').read())
        self.search_url = "https://duckduckgo.com/html/"
        self.conn = sqlite3.connect('chat_history.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history
            (timestamp TEXT, user_message TEXT, ai_response TEXT)
        ''')
        self.conn.commit()
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
    def get_response(self, message):
        print(f"Processing message: {message}")  # Debug print

        # Check for intent matches
        for intent in self.intents['intents']:
            if any(pattern.lower() in message.lower() for pattern in intent['patterns']):
                return random.choice(intent['responses'])

        # Check knowledge base
        kb_response = self.query_knowledge_base(message)
        if kb_response:
            return kb_response

        # If no matches, search the web
        search_results = self.search_web(message)
        if search_results:
            return self.generate_response_from_search(message, search_results)
        
        return "I'm sorry, I couldn't find a relevant answer to your question. Could you please rephrase or ask something else?"

    def query_knowledge_base(self, query):
        print("Querying knowledge base")  # Debug print
        query_words = set(re.findall(r'\w+', query.lower()))
        best_match = None
        best_score = 0

        for entry in self.knowledge_base:
            keywords = set(entry['keywords'])
            score = len(query_words.intersection(keywords))
            if score > best_score:
                best_score = score
                best_match = entry['response']
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
        return best_match if best_score > 0 else None
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
    def search_web(self, query, num_results=5):
        params = {'q': query, 'num': num_results}
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            response = requests.get(self.search_url, params=params, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            for result in soup.find_all('div', class_='result__body')[:num_results]:
                snippet = result.find('a', class_='result__snippet')
                if snippet:
                    results.append(snippet.text)
            return results
        except Exception as e:
            print(f"Error during web search: {e}")
            return []

    def generate_response_from_search(self, query, search_results):
        if not search_results:
            return "I'm sorry, I couldn't find any relevant information about that topic."

        # Combine all search results into one text
        combined_text = ' '.join(search_results)
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
        # Extract the most relevant sentences
        sentences = re.split(r'(?<=[.!?])\s+', combined_text)
        relevant_sentences = []
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in query.lower().split()):
                relevant_sentences.append(sentence)
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
        # Limit to 2-3 most relevant sentences
        relevant_sentences = relevant_sentences[:3]#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

        if not relevant_sentences:
            return "I found some information, but it doesn't seem directly relevant to your query. Could you please rephrase or provide more context?"

        response = f"\nHere's what I found about '{query}':\n"
        response += ' '.join(relevant_sentences)#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
        response += "\n\nWould you like more information on this topic?"
        return response#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

    def chat(self, message):
        response = self.get_response(message)
        self.save_conversation(message, response)
        return response

    def save_conversation(self, user_message, ai_response):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO chat_history (timestamp, user_message, ai_response)
            VALUES (?, ?, ?)
        ''', (timestamp, user_message, ai_response))
        self.conn.commit()

    def get_chat_history(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM chat_history ORDER BY timestamp DESC')
        return cursor.fetchall()#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

    def close(self):
        self.conn.close()

    def load_chat_history(self):
        try:
            with open('chat_history.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
    def display_chat_history(self):
        if not self.chat_history:
            print("No chat history available.")
            return

        for conversation in self.chat_history:
            print(f"[{conversation['timestamp']}]")#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
            print(f"You: {conversation['user']}")
            print(f"AI: {conversation['ai']}")
            print("-" * 50)
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
if __name__ == "__main__":
    ai = PersonalAI()
    print("Your personal AI is ready. Type 'quit' to exit or 'history' to view chat history.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'history':
            ai.display_chat_history()
        else:
            response = ai.chat(user_input)
            print(f"AI: {response}")#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 