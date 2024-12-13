import spacy

nlp = spacy.load('ja_core_news_sm')

def tokenize(text: str) -> dict[str, int]:
    """
        input: 日本語を一番好きな言語
        output: {'日本': 1, '一番': 1, '好き': 1, '言語': 1}
    """
    doc = nlp(text)
    
    
    tokens = [
        token.lemma_ for token in doc
        if not token.is_punct  
        and not token.is_stop  
        and not token.text == "\u3000"  
        and not token.like_num  
        and len(token.text.strip()) > 1  
    ]
    
    token_counts = {}
    for token in tokens:
        token_counts[token] = token_counts.get(token, 0) + 1

    return token_counts
