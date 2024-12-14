import requests
import json
import os
from rich import print

def has(words: list) -> list:
    # Create query string with OR for multiple words
    query = " OR ".join([f'"{word}"' for word in words])
    # print(f"Query being sent: {query}")

    # Step 1: Find note IDs for the query
    payload = {
        "action": "findNotes",
        "version": 6,
        "params": {
            "query": query
        }
    }
    response = requests.post("http://localhost:8765", json=payload)
    note_ids = response.json().get('result', [])

    # Debugging: Check if note IDs are found
    # print(f"Note IDs found: {note_ids}")

    # If no note IDs were found, all words are considered not present
    if not note_ids:
        return [False] * len(words)

    # Step 2: Fetch note fields to confirm matching words
    payload = {
        "action": "notesInfo",
        "version": 6,
        "params": {
            "notes": note_ids
        }
    }
    response = requests.post("http://localhost:8765", json=payload)
    notes = response.json().get('result', [])

    # Debugging: Print fetched note data
    # print(f"Notes fetched: {json.dumps(notes, indent=4)}")

    # Extract all words from fetched notes safely
    existing_words = set(
        note['fields']['Word']['value']
        for note in notes
        if 'fields' in note and 'Word' in note['fields']
    )

    # Debugging: Verify existing words set
    # print(f"Existing words in Anki: {existing_words}")

    # Step 3: Compare input words with fetched words
    return [word in existing_words for word in words]


def add(word, sentence, furigana_sentence, image_path, audio, translation, word_meaning, deck, model):
    try:
        sentence_bolded, furigana_bolded, word_furigana = bold_word_and_clean(sentence, furigana_sentence, word)

        url = "http://localhost:8765"        
        payload = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": deck,
                    "modelName": model,
                    "fields": {
                        "Word": word,
                        "Word Furigana": word_furigana,
                        "Word Meaning": word_meaning,
                        "Sentence Meaning": translation,
                        "Word Audio": f"[sound:{os.path.basename(audio)}]",
                        "Picture": f"<img src='{os.path.basename(image_path)}'>",
                        "Sentence Furigana": furigana_bolded,
                        "Sentence": sentence_bolded,
                    },
                    "tags": ["auto-added"],
                }
            },
        }
        response = requests.post(url, json=payload)
        response_data = response.json()
        if response_data.get('error'):
            print(f"[#ff1144]Error adding word '{word}': {response_data['error']}[/]")
        else:
            print(f"[#33ff77]Successfully added '{word}' to Anki.[/]")
    except Exception as e:
        print(f"[#ff1144]Error parsing Anki response for word '{word}': {e}[/]")

    return response_data

def bold_word_and_clean(sentence, furigana_sentence, word):
    sentence_bolded = sentence.replace(word, f"<b>{word}</b>")
    furigana_bolded = furigana_sentence.replace(word, f"<b>{word}</b>")
    word_furigana = word  
    return sentence_bolded, furigana_bolded, word_furigana