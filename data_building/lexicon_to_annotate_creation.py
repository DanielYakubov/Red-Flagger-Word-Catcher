"""The goal of this script is to create a file for human review
which will contain possibly hate/toxic terms"""

import datasets
import pandas as pd
import requests
from helpers import (
    clean_token_list,
    initialize_grams,
    return_list_of_first_item,
    update_grams,
)


def process_hso_dataset(
    unigram_n: int = 500, bigram_n: int = 300, trigram_n: int = 200
) -> tuple[list[str], list[str], list[str]]:
    """Processing the Hate Speech Offensive Dataset
    from Davidson et al. (2017).

    Dataset Schema:
    {
     'count': int,
     'hate_speech_count': int,
     'offensive_language_count': int,
     'neither_count': int,
     'class': int,
     'tweet': str
    }
    """
    # from hatebase.org
    hso_dataset = datasets.load_dataset("tdavidson/hate_speech_offensive")
    unigrams, bigrams, trigrams = initialize_grams()
    for item in hso_dataset["train"]:
        if item["class"] in [0, 1]:
            # 0: Hate
            # 1: Offensive
            words = clean_token_list(item["tweet"].split())

            unigrams, bigrams, trigrams = update_grams(
                words, unigrams, bigrams, trigrams
            )

    return return_list_of_first_item(
        unigrams.most_common(unigram_n),
        bigrams.most_common(bigram_n),
        trigrams.most_common(trigram_n),
    )


def process_tx_dataset(
    unigram_n: int = 500, bigram_n: int = 300, trigram_n: int = 200
) -> tuple[list[str], list[str], list[str]]:
    """Processing the Toxic Chat Dataset from Lin et al. (2023).

    Dataset Schema:
    {
        'conv_id': str,
        'user_input': str,
        'model_output': str,
        'human_annotation': bool,
        'toxicity': int,
        'jailbreaking': int,
        'openai_moderation': list[list[str, float]]
    }
    """
    tx_dataset = datasets.load_dataset("lmsys/toxic-chat", "toxicchat0124")
    unigrams, bigrams, trigrams = initialize_grams()
    for item in tx_dataset["train"]:
        if item["toxicity"] == 1:
            words = clean_token_list(item["user_input"].split())

            unigrams, bigrams, trigrams = update_grams(
                words, unigrams, bigrams, trigrams
            )

    return return_list_of_first_item(
        unigrams.most_common(unigram_n),
        bigrams.most_common(bigram_n),
        trigrams.most_common(trigram_n),
    )


def process_xplain_dataset(
    unigram_n: int = 500, bigram_n: int = 300, trigram_n: int = 200
) -> tuple[list[str], list[str], list[str]]:
    """Processing the HateXplain Dataset from Mathew et al. (2021).

    Dataset Schema:
    {
        'id': str,
        'annotators':
            {
                'label': list[int],
                'annotator_id': list[int],
                'target': list[list[str],
            },
        'rationales': list[list[int]],
        'post_tokens': list[str]
    }
    """
    hxplain = datasets.load_dataset(
        "Hate-speech-CNERG/hatexplain", trust_remote_code=True
    )

    unigrams, bigrams, trigrams = initialize_grams()
    for item in hxplain["train"]:
        annotations = item["annotators"]["label"]  # list of label
        if 0 in annotations or 2 in annotations:
            # 0: Hate
            # 2: Offensive
            # If any annotator found the text offensive, we are using it
            words = clean_token_list(item["post_tokens"])

            # adding to each
            unigrams, bigrams, trigrams = update_grams(
                words, unigrams, bigrams, trigrams
            )

    return return_list_of_first_item(
        unigrams.most_common(unigram_n),
        bigrams.most_common(bigram_n),
        trigrams.most_common(trigram_n),
    )


def process_offensive_dataset(
    unigram_n: int = 500, bigram_n: int = 300, trigram_n: int = 200
) -> tuple[list[str], list[str], list[str]]:
    """A Dataset of offensive language that is made from
    the OLID dataset (Zampieri et al., 2019) and the labels from
    (Davidson et al.,2017)

     Dataset Schema
     {
        'text': str,
        'label': int,
        'text_label': str
    }
    """
    offensive_dataset = datasets.load_dataset(
        "christinacdl/offensive_language_dataset"
    )

    unigrams, bigrams, trigrams = initialize_grams()
    for item in offensive_dataset["train"]:
        if item["label"] == 1:
            # 1: Offensive
            words = clean_token_list(item["text"].split())

            # adding to each
            unigrams, bigrams, trigrams = update_grams(
                words, unigrams, bigrams, trigrams
            )

    return return_list_of_first_item(
        unigrams.most_common(unigram_n),
        bigrams.most_common(bigram_n),
        trigrams.most_common(trigram_n),
    )


def download_github_wordlist(url: str) -> set[str]:
    """Downloads a word list from a raw github URL

    There's an underlying assumption about the format of the content of the URL

    Assumed format:
    <Word 1>
    <Word 2>
    ...
    <Word N>
    """
    response = requests.get(url)
    if response.status_code == 200:
        wordlist = response.text.split("\n")
        cleaned_wordlist = clean_token_list(wordlist)
        return set(cleaned_wordlist)
    else:
        print(f"Failed to get file from {url}. Code: {response.status_code}.")


if __name__ == "__main__":
    # Getting the top ngrams from each corpus.
    hso_unigrams, hso_bigrams, hso_trigrams = process_hso_dataset()
    tx_unigrams, tx_bigrams, tx_trigrams = process_tx_dataset()
    xplain_unigrams, xplain_bigrams, xplain_trigrams = process_xplain_dataset()
    offensive_unigrams, offensive_bigrams, offensive_trigrams = (
        process_offensive_dataset()
    )

    # Getting the lexicons of toxicity from open-source libraries.
    musk_hate = download_github_wordlist(
        "https://raw.githubusercontent.com/dan-hickey1/musk-hate-lexicon/refs/heads/main/hate_keywords.txt"  # noqa: E501
    )
    gab_hate = download_github_wordlist(
        "https://raw.githubusercontent.com/hate-alert/HateBegetsHate_CSCW2020/refs/heads/master/HateLexicons.txt"  # noqa: E501
    )
    gst_hate = download_github_wordlist(
        "https://raw.githubusercontent.com/martinigoyanes/LexiconGST/refs/heads/main/data/lexicons/hate.txt"  # noqa: E501
    )
    # TODO: something is odd about this raw file.
    # When you visit it in browser, it immediately begins a download.
    # gst_abuse = download_github_wordlist(
    #     "https://raw.githubusercontent.com/martinigoyanes/LexiconGST/refs/heads/main/data/lexicons/abuse.txt" # noqa: E501
    # )
    gst_toxic = download_github_wordlist(
        "https://raw.githubusercontent.com/martinigoyanes/LexiconGST/refs/heads/main/data/lexicons/toxic.txt"  # noqa: E501
    )
    shutter_stock_hate = download_github_wordlist(
        "https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/refs/heads/master/en"  # noqa: E501
    )

    # getting rid of overlaps
    all_unigrams = list(
        set.union(
            set(hso_unigrams),
            set(tx_unigrams),
            set(xplain_unigrams),
            set(offensive_unigrams),
            musk_hate,
            gab_hate,
            gst_hate,
            gst_toxic,
            shutter_stock_hate,
        )
    )

    all_bigrams = [
        " ".join(words)
        for words in set.union(
            set(hso_bigrams),
            set(tx_bigrams),
            set(xplain_bigrams),
            set(offensive_bigrams),
        )
    ]

    all_trigrams = [
        " ".join(words)
        for words in set.union(
            set(hso_trigrams),
            set(tx_trigrams),
            set(xplain_trigrams),
            set(offensive_trigrams),
        )
    ]

    print(f"{len(all_unigrams)} unique unigrams to review from corpora")
    print(f"{len(all_bigrams)} unique bigrams to review from corpora")
    print(f"{len(all_trigrams)} unique trigrams to review from corpora")

    dataset = all_unigrams + all_bigrams + all_trigrams

    corpus_possible_abuse = pd.DataFrame(
        data=dataset, columns=["words_to_check"]
    )
    # adding an empty column for annotation
    corpus_possible_abuse["Abuse Term (Y/N)"] = ""
    corpus_possible_abuse.to_csv(
        "possible_abuse_terms_for_review.csv", index=False
    )
    print(
        "possible_abuse_terms_for_review.csv file created,"
        " once it is annotated run post_annotation_processing.py"
    )
