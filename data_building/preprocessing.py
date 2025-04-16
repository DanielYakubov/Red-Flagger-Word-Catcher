"""The goal of this script is to create a file for human review which will contain possibly hate/toxic terms"""

import datasets
from nltk import ngrams
from nltk.corpus import stopwords
from collections import Counter

STOPS = set(stopwords.words('english'))


def _initialize_grams():
    unigrams = Counter()
    bigrams = Counter()
    trigrams = Counter()
    return unigrams, bigrams, trigrams


def _update_grams(words: list[str], unigrams, bigrams, trigrams):
    # adding to each
    unigrams.update(words)
    bigrams.update(ngrams(words, 2))
    trigrams.update(ngrams(words, 3))
    return unigrams, bigrams, trigrams


def _clean_token_list(words):
    return [
        word.lower().strip(" .,!,?\"'`") for word in words if word not in STOPS
    ]


def process_hso_dataset(unigram_n=300, bigram_n=150, trigram_n=100):
    hso_dataset = datasets.load_dataset("tdavidson/hate_speech_offensive")
    unigrams, bigrams, trigrams = _initialize_grams()
    for item in hso_dataset['train']:
        if item['class'] in [0, 1]:
            # 0: Hate
            # 1: Offensive
            words = _clean_token_list(item["tweet"].split())

            unigrams, bigrams, trigrams = _update_grams(words, unigrams,
                                                        bigrams, trigrams)

    return unigrams.most_common(unigram_n), bigrams.most_common(
        bigram_n), trigrams.most_common(trigram_n)


def process_hb_dataset(unigram_n=300, bigram_n=150, trigram_n=100):
    # processing hate_speech_offensive dataset
    hb_dataset = datasets.load_dataset("lmsys/toxic-chat", "toxicchat0124")
    unigrams, bigrams, trigrams = _initialize_grams()
    for item in hb_dataset['train']:
        if item['toxicity'] == 1:
            words = _clean_token_list(item["user_input"].split())

            unigrams, bigrams, trigrams = _update_grams(words, unigrams,
                                                        bigrams, trigrams)

    return unigrams.most_common(unigram_n), bigrams.most_common(
        bigram_n), trigrams.most_common(trigram_n)


def process_xplain_dataset(unigram_n=300, bigram_n=150, trigram_n=100):
    # processing hate_speech_offensive dataset
    hxplain = datasets.load_dataset("Hate-speech-CNERG/hatexplain",
                                    trust_remote_code=True)

    unigrams, bigrams, trigrams = _initialize_grams()
    for item in hxplain['train']:
        annotations = item['annotators']["label"]  # list of label
        if 0 in annotations or 2 in annotations:
            # 0: Hate
            # 2: Offensive
            # If any annotator found the text offensive, we are using it
            words = _clean_token_list(item["post_tokens"])

            # adding to each
            unigrams, bigrams, trigrams = _update_grams(words, unigrams,
                                                        bigrams, trigrams)

    return unigrams.most_common(unigram_n), bigrams.most_common(
        bigram_n), trigrams.most_common(trigram_n)


if __name__ == "__main__":
    hso_unigrams, hso_bigrams, hso_trigrams = process_hso_dataset()
    hb_unigrams, hb_bigrams, hb_trigrams = process_hb_dataset()
    xplain_unigrams, xplain_bigrams, xplain_trigrams = process_xplain_dataset()
