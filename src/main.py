import os
import requests
import time
import pyperclip
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from rich import print
import re


file_path = "./data.txt"
anki_deck_name = "Immersion Kit"
anki_model_name = "Kaishi 1.5k"

driver = webdriver.Chrome()

anki_media_folder = "C:/Users/sheha/AppData/Roaming/Anki2/User 1/collection.media/"

def download_file(file_url, file_extension):
    file_name = os.path.basename(urlparse(file_url).path)
    local_file_path = os.path.join(anki_media_folder, file_name)

    if not os.path.exists(anki_media_folder):
        os.makedirs(anki_media_folder)

    try:
        response = requests.get(file_url)
        response.raise_for_status()
        with open(local_file_path, 'wb') as f:
            f.write(response.content)
        print(f"[#33ff77]Downloaded {file_extension}:[/] {file_name}")
        return file_name
    except requests.RequestException as e:
        print(f"[#ff1144]Failed to download {file_extension}:[/] {file_url} | Error: {e}")
        return None

def fetch_word_data(word):
    print(f"[#2233ff]Searching For Word[/] [#33ff77]{word}[/]")

    driver.get(f"https://www.immersionkit.com/dictionary?keyword={word}")
    
    try:
        target_xpath = (
            "/html/body/div/div[1]/div/div[2]/div[@class='ui segment']/div/div[2]/div[3]/div[1]"
            "//div[not(@class)]/div/a[1]"
        )
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, target_xpath)))
        target_element = driver.find_element(By.XPATH, target_xpath)

        driver.execute_script("arguments[0].scrollIntoView();", target_element)
        time.sleep(0.1) 
        target_element.click()
        
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/div/div[2]/div[@class='ui segment']/div/div[2]/div[3]/div[1]//div[not(@class)]/div[2]/div[1]/button[1]"))
        )
        word_meaning = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div[2]/div[4]/div[1]")
        word_meaning = re.search(rf"\((.*?)\)", word_meaning.text).group(1) 
        sentence = fetch_clipboard_data("/html/body/div/div[1]/div/div[2]/div[@class='ui segment']/div/div[2]/div[3]/div[1]//div[not(@class)]/div[2]/div[1]/button[1]")
        furigana_sentence = fetch_clipboard_data("/html/body/div/div[1]/div/div[2]/div[@class='ui segment']/div/div[2]/div[3]/div[1]//div[not(@class)]/div[2]/div[1]/button[2]")
        image_url = fetch_clipboard_data("/html/body/div/div[1]/div/div[2]/div[@class='ui segment']/div/div[2]/div[3]/div[1]//div[not(@class)]/div[2]/div[3]/button[1]")
        audio_url = fetch_clipboard_data("/html/body/div/div[1]/div/div[2]/div[@class='ui segment']/div/div[2]/div[3]/div[1]//div[not(@class)]/div[2]/div[3]/button[2]")
        translation = fetch_clipboard_data("/html/body/div/div[1]/div/div[2]/div[@class='ui segment']/div/div[2]/div[3]/div[1]//div[not(@class)]/div[2]/button")

        
        local_image_name = download_file(image_url, "image")
        local_audio_name = download_file(audio_url, "audio")

        return (word, sentence, furigana_sentence, local_image_name, local_audio_name, translation, word_meaning)

    except Exception as e:
        print(f"[#ff1144]Error fetching data for {word}: {e}[/]")
        return None


def fetch_clipboard_data(xpath):
    driver.find_element(By.XPATH, xpath).click()
    time.sleep(0.1)  
    return pyperclip.paste()

def bold_word_and_clean(sentence, furigana_sentence, word):
    lis = list(word)
    furigana_match = re.search(rf"({re.escape(word)}\[[^\]]+\])", furigana_sentence) or re.search(rf"({re.escape(lis[0])}.*?(\[.*?\])?{re.escape(lis[-1])})(\[.*?\])?", furigana_sentence)
    word_furigana = furigana_match.group() if furigana_match else word

    
    furigana_pattern = rf"({re.escape(word)}\[[^\]]+\])"
    furigana_bolded = re.sub(furigana_pattern, r"<b>\1</b>", furigana_sentence)
    
    sentence_pattern = rf"({re.escape(word)})"
    sentence_bolded = re.sub(sentence_pattern, r"<b>\1</b>", sentence)
    
    return sentence_bolded, furigana_bolded, word_furigana

def add_to_anki(word, sentence, furigana_sentence, image_path, audio, translation, word_meaning):
    try:
        sentence_bolded, furigana_bolded, word_furigana = bold_word_and_clean(sentence, furigana_sentence, word)

        url = "http://localhost:8765"        
        payload = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": anki_deck_name,
                    "modelName": anki_model_name,
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
def main():
    with open(file_path, "r", encoding="utf-8") as file:
        words = file.readlines()
    failedWords = []
    for word in words:
        word = word.strip()
        
        if not word:
            continue
        word_data = fetch_word_data(word)
        if word_data:
            add_to_anki(*word_data)
            
        else:
            failedWords.append(word)
    if len(failedWords) > 0:
        print("[#ff1144]Words that failed to fetch:[/]")
    for word in failedWords:
        print(f"[#ff66ff]{word}[/]")

    driver.quit()

if __name__ == "__main__":
    main()
