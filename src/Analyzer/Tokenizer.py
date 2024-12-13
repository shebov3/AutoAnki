import spacy

nlp = spacy.load('ja_core_news_sm')

def tokenize(text: str) -> list[str]:
    """
        input: 日本語を一番好きな言語
        output: {'日本': 1, '一番': 1, '好き': 1, '言語': 1}
    """
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_punct and not token.is_stop and not token.text == r"\u3000" and not token.like_num]

    return tokens