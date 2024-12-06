# Immersion Kit Anki Integration

This project is designed to fetch Japanese words and their associated data (such as sentences, furigana, images, audio, and translations) from the Immersion Kit website. The data is then formatted and added automatically to Anki as flashcards. This tool uses **Selenium**, **Requests**, and **Pyperclip** to scrape and interact with the website and the clipboard, and it interacts with Anki through its local API.

## Requirements

Before using this project, make sure you have the following installed:

- Python 3.x
- **Anki** (installed and running on your system)
- **AnkiConnect** add-on (for Anki API access)  
  You can install it from [here](https://ankiweb.net/shared/info/2055492159).
  
- Install Python dependencies:
  ```bash
  pip install selenium requests pyperclip rich
  ```

- **ChromeDriver**:
  This project uses **Selenium** with **Chrome**. You will need **ChromeDriver** compatible with your Chrome version.
  - Download ChromeDriver from [here](https://sites.google.com/chromium.org/driver/).
  - Make sure ChromeDriver is in your system’s PATH or specify the path to it in the code.

## Setup

### 1. Clone the Repository

Clone the project repository to your local machine:

```bash
git clone <repository_url>
cd <repository_name>
```

### 2. Anki Media Folder Setup

Ensure your Anki media folder is set up properly. You can find the location of the media folder in Anki’s preferences. The default location for a Windows machine is:

```plaintext
C:/Users/<YourUserName>/AppData/Roaming/Anki2/User 1/collection.media/
```

You can modify the `anki_media_folder` variable in the script to point to your specific Anki media folder.

### 3. Configure AnkiDeck and Model Name

You must modify the `anki_deck_name` and `anki_model_name` variables in the script to match the deck and model you want to use in Anki. The default values are:

```python
anki_deck_name = "Immersion Kit"
anki_model_name = "Kaishi 1.5k"
```

These should correspond to your Anki deck and card model.

### 4. Input Words

Create a `data.txt` file containing a list of Japanese words (one word per line) that you want to add to Anki. The file should look like this:

```plaintext
日本
学ぶ
食べる
```

### 5. Launch the Script

Run the script to fetch word data and add it to Anki:

```bash
python main.py
```

### 6. Anki Integration

The script interacts with Anki through AnkiConnect. The Anki app must be running and the AnkiConnect add-on must be enabled to allow the script to add notes.

## How It Works

- **Selenium**: This tool automates the process of opening the browser, navigating to the Immersion Kit website, and extracting information from the word's page. It scrapes data like the sentence, furigana, images, audio, and translation.
  
- **Requests**: The tool downloads images and audio files associated with the word.
  
- **Pyperclip**: This is used to interact with the system clipboard. After performing the necessary clicks on the page, the content (such as sentence, furigana, and translation) is copied to the clipboard, and the script retrieves it.

- **AnkiConnect**: The tool sends the scraped and formatted data to Anki's local API, which adds the word, its furigana, example sentence, image, audio, and translation to the specified deck.

## Example of Data Added to Anki

For each word, the following fields will be populated in the Anki deck:

- **Word**: The Japanese word.
- **Word Furigana**: The furigana for the word (if available).
- **Sentence**: A sample sentence containing the word.
- **Sentence Furigana**: The furigana for the sentence (if available).
- **Sentence Meaning**: The translation of the sentence.
- **Word Audio**: Audio for the word.
- **Picture**: Image associated with the word.

## Troubleshooting

- **AnkiConnect Issues**: Ensure that Anki is running and AnkiConnect is installed and enabled.
  
- **Selenium Issues**: If you face issues related to the browser or driver, ensure that **ChromeDriver** is installed and correctly configured.

- **No Data for Some Words**: The script relies on Immersion Kit’s website to provide data. Some words may not have all the information available, or the website may have changed, causing a mismatch with the script’s expectations.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
