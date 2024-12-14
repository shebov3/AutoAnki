import spacy, re
from glob import glob
import os
from rich import print
from collections import Counter

nlp = spacy.load('ja_core_news_sm')

def tokenize(text: str) -> list[str]:
    document = nlp(text)
    tokens = [
        token.lemma_ for token in document
        if not token.is_punct  
        and not token.is_stop  
        and not token.text == "\u3000"  
        and not token.like_num  
        and token.lang_ == "ja"
        and not re.match(r'^[A-Za-z0-9:~]+$', token.text)
        and not token.text == "♪"
        and not re.match(r'^[ア-ンあ-んー]+ッ*$', token.text)
        and not re.match(r'.*ー.*', token.text)  
        and not token.text.endswith("っ")
        and not token.is_ascii
    ]
    return tokens

def parse(path: str) -> list[str]:
    with open(path, 'r', encoding='utf-8') as file:
        srt_text = file.read()
    srt_blocks = srt_text.split('\n\n')
    sentences = []
    for block in srt_blocks:
        lines = block.split('\n')
        if len(lines) > 2: 
            text = ' '.join(lines[2:]) 
            sentences.append(text.strip())
    return sentences

def tokenizeSRT(path: str):
    srt_files = glob(os.path.join(path, '*.srt'))
    document = []
    for srt_file in srt_files:
        print(f"[#33ff99][b]Processing file: [/][#3399ff]{srt_file}[/]")
        sentences = parse(srt_file)
        for text in sentences:
            tokens = tokenize(text)
            for token in tokens:
                document.append(token)
    return document