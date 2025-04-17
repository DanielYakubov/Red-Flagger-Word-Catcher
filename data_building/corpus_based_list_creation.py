"""The goal of this script is to create a file for human review which will contain possibly hate/toxic terms"""

from collections import Counter

import datasets
import pandas as pd
from nltk import ngrams
from nltk.corpus import stopwords


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
    # not doing stopword cleaning because we want multi-word phrases.
    return [word.lower().strip(" .,!,?\"'`") for word in words]


def _return_list_of_first_item(*args):
    processed_args = []
    for lst in args:
        only_first = [i[0] for i in lst]
        processed_args.append(only_first)
    return *processed_args,


def process_hso_dataset(unigram_n=500, bigram_n=300, trigram_n=200):
    hso_dataset = datasets.load_dataset("tdavidson/hate_speech_offensive")
    unigrams, bigrams, trigrams = _initialize_grams()
    for item in hso_dataset['train']:
        if item['class'] in [0, 1]:
            # 0: Hate
            # 1: Offensive
            words = _clean_token_list(item["tweet"].split())

            unigrams, bigrams, trigrams = _update_grams(words, unigrams,
                                                        bigrams, trigrams)

    return _return_list_of_first_item(unigrams.most_common(unigram_n),
                                      bigrams.most_common(bigram_n),
                                      trigrams.most_common(trigram_n))


def process_hb_dataset(unigram_n=500, bigram_n=300, trigram_n=200):
    # processing hate_speech_offensive dataset
    hb_dataset = datasets.load_dataset("lmsys/toxic-chat", "toxicchat0124")
    unigrams, bigrams, trigrams = _initialize_grams()
    for item in hb_dataset['train']:
        if item['toxicity'] == 1:
            words = _clean_token_list(item["user_input"].split())

            unigrams, bigrams, trigrams = _update_grams(words, unigrams,
                                                        bigrams, trigrams)

    return _return_list_of_first_item(unigrams.most_common(unigram_n),
                                      bigrams.most_common(bigram_n),
                                      trigrams.most_common(trigram_n))


def process_xplain_dataset(unigram_n=500, bigram_n=300, trigram_n=200):
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

    return _return_list_of_first_item(unigrams.most_common(unigram_n),
                                      bigrams.most_common(bigram_n),
                                      trigrams.most_common(trigram_n))


if __name__ == "__main__":
    # getting the top ngrams from each file
    hso_unigrams, hso_bigrams, hso_trigrams = process_hso_dataset()
    hb_unigrams, hb_bigrams, hb_trigrams = process_hb_dataset()
    xplain_unigrams, xplain_bigrams, xplain_trigrams = process_xplain_dataset()

    # getting rid of overlaps
    all_unigrams = list(
        set.union(set(hso_unigrams), set(hb_unigrams), set(xplain_unigrams)))

    all_bigrams = list(
        set.union(set(hso_bigrams), set(hb_bigrams), set(xplain_bigrams)))
    # # for bigrams, we want to avoid overlaps with unigrams
    # for w1, w2 in all_bigrams:
    #     if w1 not in all_unigrams and w2 not in all_unigrams:
    #         all_bigrams_processed.append(" ".join([w1, w2]))
    #     else:
    #         print(w1, w2)

    all_trigrams = list(
        set.union(set(hso_trigrams), set(hb_trigrams), set(xplain_trigrams)))
    # # for trigrams we want to avoid overlap with bigrams, it's easier to do this in str form.
    # for w1, w2, w3 in all_trigrams:
    #     trigram_str = " ".join([w1, w2, w3])
    #     unique = True
    #
    #     if set.intersection({w1, w2, w3}, all_unigrams):
    #         # trigram is not unique if any gram is in unigrams
    #         continue
    #
    #     # inefficient, but lists are small enough
    #     for bigram_str in all_bigrams_processed:
    #         if bigram_str in trigram_str:
    #             unique = False
    #             break
    #     if unique:
    #         all_trigrams_processed.append(trigram_str)

    print(f"{len(all_unigrams)} unique unigrams to review from corpora")
    print(f"{len(all_bigrams)} unique bigrams to review from corpora")
    print(f"{len(all_trigrams)} unique trigrams to review from corpora")

    dataset = all_unigrams + all_bigrams + all_trigrams

    corpus_possible_abuse = pd.DataFrame(data=dataset,
                                         columns=["words_to_check"])
    # adding an empty column for annotation
    corpus_possible_abuse["Abuse Term (Y/N)"] = ""
    corpus_possible_abuse.to_csv("possible_abuse_terms_for_review.csv",
                                 index=False)
    print(
        "possible_abuse_terms_for_review.csv file created, "
        "once reviewed and annotated run corpus_based_list_post_processing.csv"
    )
