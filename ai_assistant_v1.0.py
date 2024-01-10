import json
import os
import random
import time
import logging
import sys
from typing import Dict, List, Optional
import Levenshtein

# Constants
SIMILARITY_THRESHOLD = 0.6  # Lowered to increase matching flexibility
DATA_FILE = 'ai_data.json'
MAX_ATTEMPTS = 3
TYPEWRITER_EFFECT_ON = True
TYPEWRITER_SPEED = 0.05
SHOW_TRAIN_AI_OPTION = True
SHOW_ASK_AI_OPTION = True

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def typewriter_effect(text: str):
    """Print text with a typewriter effect."""
    if TYPEWRITER_EFFECT_ON:
        for char in text:
            print(char, end='', flush=True)
            time.sleep(TYPEWRITER_SPEED)
        print()
    else:
        print(text)

def find_closest_matches(user_question: str, dictionary: Dict[str, List[str]]) -> List[str]:
    """Find a list of close matches for a user question in the dictionary."""
    matches = []

    for trained_question in dictionary:
        similarity = Levenshtein.ratio(user_question, trained_question)
        if similarity > SIMILARITY_THRESHOLD:
            matches.append(trained_question)

    return matches

def load_ai_data(filepath: str) -> Dict[str, List[str]]:
    """Load AI data from a JSON file."""
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        try:
            if not os.path.exists(filepath):
                logging.info(f"File {filepath} not found. Starting with an empty dictionary.")
                return {}

            with open(filepath, mode='r', encoding='utf-8') as file:
                return json.load(file)
        except IOError as e:
            logging.error(f"IOError loading data: {e}")
            attempts += 1
        except Exception as e:
            logging.error(f"Unexpected error loading data: {e}")
            return {}

def save_ai_data(dictionary: Dict[str, List[str]], filepath: str):
    """Save AI data to a JSON file."""
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        try:
            with open(filepath, mode='w', encoding='utf-8') as file:
                json.dump(dictionary, file, ensure_ascii=False, indent=4)
                break
        except IOError as e:
            logging.error(f"IOError saving data: {e}")
            attempts += 1
        except Exception as e:
            logging.error(f"Unexpected error saving data: {e}")

def get_user_choice() -> str:
    """Get user choice from the menu."""
    menu_options = []
    if SHOW_TRAIN_AI_OPTION:
        menu_options.append("1. Train AI")
    if SHOW_ASK_AI_OPTION:
        menu_options.append("2. Ask AI")
    menu_options.append("3. Exit")

    menu = "\nAI Assistant\n" + "\n".join(menu_options)
    typewriter_effect(menu)
    return input("Choose an option: ").strip()

def get_training_question() -> str:
    """Get a training question from the user."""
    return input("Enter the question (or type 'menu:', 'clear:', 'exit:', 'commands:' to return to main menu): ").lower().strip()

def get_training_answer() -> Optional[str]:
    """Get a training answer from the user."""
    answer = input("Enter the answer: ").strip()
    if not answer:
        typewriter_effect("Answer cannot be empty.")
        return None
    return answer

def get_user_question() -> str:
    """Get a question from the user."""
    return input("What is your question? (or type 'menu:', 'clear:', 'exit:', 'commands:' to return to main menu): ").lower().strip()

def train_ai_loop(dictionary: Dict[str, List[str]]):
    """Training loop for the AI."""
    while True:
        question = get_training_question()
        if question == 'menu:':
            break
        elif question == 'clear:':
            os.system('cls' if os.name == 'nt' else 'clear')
        elif question == 'exit:':
            exit()
        elif question == 'commands:':
            display_commands('train')
        elif question.endswith(':'):
            typewriter_effect("Command not allowed in training mode.")
        else:
            answer = get_training_answer()
            if answer:
                dictionary.setdefault(question, []).append(answer)
                typewriter_effect("Training complete.")

def ask_ai_loop(dictionary: Dict[str, List[str]]):
    """Loop for asking questions to the AI."""
    while True:
        user_question = get_user_question()
        if user_question.startswith('show:'):
            show_all_answers(user_question[5:].strip(), dictionary)
        elif user_question.startswith('search:'):
            search_question(user_question[7:].strip(), dictionary)
        elif user_question == 'menu:':
            break
        elif user_question == 'clear:':
            os.system('cls' if os.name == 'nt' else 'clear')
        elif user_question == 'exit:':
            exit()
        elif user_question == 'commands:':
            display_commands('ask')
        else:
            answer_question(user_question, dictionary)

def display_commands(context: str):
    """Display available commands based on the context."""
    commands = ["menu:", "clear:", "exit:", "commands:"]
    if context == 'ask':
        commands.extend(["show:", "search:"])
    typewriter_effect("Available commands:\n" + "\n".join(commands))

def show_all_answers(question: str, dictionary: Dict[str, List[str]]):
    """Show all answers for a given question."""
    matches = find_closest_matches(question, dictionary)
    if matches:
        for match in matches:
            typewriter_effect(f"Question: {match}\nAnswers: {' | '.join(dictionary[match])}")
    else:
        typewriter_effect("No answers found for this question.")

def search_question(keyword: str, dictionary: Dict[str, List[str]]):
    """Search for questions containing a specific keyword."""
    found_questions = [q for q in dictionary if keyword in q]
    if found_questions:
        for question in found_questions:
            typewriter_effect(f"Question: {question}\nAnswers: {' | '.join(dictionary[question])}")
    else:
        typewriter_effect("No related questions found.")

def answer_question(user_question: str, dictionary: Dict[str, List[str]]):
    """Provide an answer to the user's question."""
    matches = find_closest_matches(user_question, dictionary)
    if matches:
        selected_match = random.choice(matches)
        answer = random.choice(dictionary[selected_match])
        typewriter_effect(f"AI: {answer}")
    else:
        typewriter_effect("AI: I don't know the answer to that. Please train me.")

def main():
    """Main function to run the AI Assistant."""
    try:
        ai_dictionary = load_ai_data(DATA_FILE)

        while True:
            choice = get_user_choice()
            if choice == '1' and SHOW_TRAIN_AI_OPTION:
                train_ai_loop(ai_dictionary)
                save_ai_data(ai_dictionary, DATA_FILE)
            elif choice == '2' and SHOW_ASK_AI_OPTION:
                ask_ai_loop(ai_dictionary)
            elif choice == '3':
                break
            else:
                typewriter_effect("Invalid choice. Please try again.")
    except KeyboardInterrupt:
        print("\nExiting program gracefully...")
        sys.exit(0)

if __name__ == "__main__":
    main()
