from red_flagger.red_flagger import RedFlagger
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

rf = RedFlagger()

def create_vec(content: str | list[str], wordlist: list[str] = rf.get_wordlist()) -> np.array:
    """
    Creates vector of shape [1, len(wordlist)].
    Can also be given a list of docuemnts for content which will return shape [len(content), len(wordlist)]
    """
    if isinstance(content, str):
        content = [content]
    elif not isinstance(content, list):
        raise TypeError("Input must either be a single document (str), or list of documents")
    vectorizer = CountVectorizer(vocabulary=wordlist)
    vector = vectorizer.fit_transform(content) # Sparse matrix
    return vector.toarray() # Dense matrix
