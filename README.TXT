AI Assistant

This Python script provides an interactive AI Assistant capable of learning from user inputs and answering questions based on its training data. It utilizes a CSV file to store and retrieve training data and features a typewriter effect for displaying output.
Features

    Training Mode: Users can input questions and corresponding answers to train the AI.
    Query Mode: Users can ask questions and receive answers based on the AI's training.
    Data Persistence: Training data is saved in and loaded from a CSV file.
    Typewriter Effect: Enhances user experience with a typewriter-like display of text (can be toggled off).
    Search Functionality: Allows users to search for questions containing specific keywords.
    Show Answers: Displays all answers for a specific question.
    Menu Navigation: Easy navigation through a simple menu interface.

Installation

Install the Levenshtein library required for string similarity calculations:

bash

pip install python-Levenshtein

Usage

Run the script in a Python environment. The main menu offers several options:

    Train AI: Input a question and an answer to train the AI.
    Ask AI: Pose a question to the AI and receive an answer based on its training.
    Exit: Exit the application.

Additional Commands in Query Mode

    show: [question]: Show all answers for a specific question.
    search: [keyword]: Search for questions containing a given keyword.
    menu: Return to the main menu at any point.

Typewriter Effect

The typewriter effect is enabled by default. To disable it, set TYPEWRITER_EFFECT_ON to False in the script.
CSV Data File Format

The script reads and writes to a CSV file named ai_data.csv. Each line represents a question-answer pair, separated by a comma. Answers to the same question are concatenated using a vertical bar (|) as a separator.
Logging

Basic logging is enabled for tracking the application's operation and any errors that occur, especially during file operations.
