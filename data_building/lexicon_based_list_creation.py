import pandas as pd
import requests


def download_github_wordlist(url):
    response = requests.get(url)
    if response.status_code == 200:
        return set(response.text.split())  # wordlist!
    else:
        print(
            f"Failed to download file from {url}. Status code: {response.status_code}. Does this URL still exist?"
        )


if __name__ == "__main__":
    musk_hate = download_github_wordlist(
        "https://raw.githubusercontent.com/dan-hickey1/musk-hate-lexicon/refs/heads/main/hate_keywords.txt"
    )
    gab_hate = download_github_wordlist(
        "https://raw.githubusercontent.com/hate-alert/HateBegetsHate_CSCW2020/refs/heads/master/HateLexicons.txt"
    )
    gst_hate = download_github_wordlist(
        "https://raw.githubusercontent.com/martinigoyanes/LexiconGST/refs/heads/main/data/lexicons/hate.txt"
    )
    # TODO: something is odd about this raw file. When you visit it in browser, it immediately begins a download.
    # gst_abuse = download_github_wordlist(
    #     "https://raw.githubusercontent.com/martinigoyanes/LexiconGST/refs/heads/main/data/lexicons/abuse.txt"
    # )
    gst_toxic = download_github_wordlist(
        "https://raw.githubusercontent.com/martinigoyanes/LexiconGST/refs/heads/main/data/lexicons/toxic.txt"
    )

    lexicon = list(
        set.union(musk_hate, gab_hate, gst_hate, gst_hate, gst_toxic)
    )
    print(f"Lexicon of unique items of length {len(lexicon)} created.")

    lexicon_df = pd.DataFrame(lexicon, columns=["words_to_check"])
    lexicon_df["Abuse Term (Y/N)"] = ""
    lexicon_df.to_csv("lexicon_based_wordlist_to_check.csv", index=False)

    print(
        "lexicon_based_wordlist_to_check.csv file created, run corpus_based_list_creation.py if you haven't"
        "once both are reviewed and annotated run post_annotation_processing.py"
    )
