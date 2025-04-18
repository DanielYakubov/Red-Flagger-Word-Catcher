"""A script to run to avoid duplicate words post annotations"""
import argparse
import os

import pandas as pd

from abuse_flagger.obscure_data import obscure, unobscure, ObscuringError

OUT_FILEPATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "abuse_flagger", "data", "toxic_keywords_b16.txt")


class ArgsError(Exception):
    pass


def set_up_parser() -> argparse.ArgumentParser:
    """Set up the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog='AnnotationPostProcessing',
        description='Processes an annotated wordlist and adds it to the stored global blacklist.'
    )
    parser.add_argument('filename', help="The path to the annotation file.")
    parser.add_argument("--word_col", help="The name of the column containing the toxic words.", default="words_to_check")
    parser.add_argument("--annotation_col", help="The name of the column containing the binary annotations.", default="Abuse Term (Y/N)")
    parser.add_argument("--positive_label", help="The string that represents a positive annotation in the annotation_col.", default="y")
    parser.add_argument("--negative_label", help="The string that represents a negative annotation in the annotation_col", default="n")
    parser.add_argument("--out_file", help="The name of the file to write to.", default=OUT_FILEPATH)
    return parser


def load_file(filename) -> pd.DataFrame:
    """Load in the file with an informative error in case something is off."""
    if not os.path.exists(filename):
        raise ValueError(f"The file name provided does not exist. File name: {filename}")
    return pd.read_csv(filename)


def validate_data(df: pd.DataFrame, args: argparse.Namespace) -> None:
    """Validate the loaded in dataframe with the user specified args. This tries to catch any simple schema errors."""
    if args.word_col not in df.columns:
        raise ArgsError(f"Specified word_col {args.word_col} not found in sheet columns {df.columns}")
    if args.annotation_col not in df.columns:
        raise ArgsError(f"Specified annotation_col {args.annotation_col} not found in sheet columns {df.columns}")
    if set(df[args.annotation_col]) - set((args.positive_label, args.negative_label)):
        raise ArgsError(f"Annotations other than specified positive_label \"{args.positive_label}\" and negative_label \"{args.negative_label}\" found in annotation_col {args.annotation_col}.")
    if os.path.exists(args.out_file):
        input("WARNING!!!!! The out_file exists. Execution of this script will override it.")


def filter_overlaps_and_sort(word_list: list[str]) -> list[str]:
    """Filters the word list to ensure items are unique within the word list.

    Filtering happens in two steps:
    1) All the single gram items are extracted into a list, iff they are unique to the list. Multi-words are stored.
    2) The multi-word container is iterated and added to the unique words list iff the multi-words do not contain
        existing single words.

    This algorithm also pseudo-sorts the list. First, all the unigrams are listed, then the multiword items.
    """
    # NOT using a set here, want to be careful about determinism & insertion order.
    unique_words: list[str] = []
    multi_words: list[tuple[str, str, ...]] = []
    # Initial loop gets unigrams
    for word_item in word_list:
        words = word_item.split()
        if len(words) == 1:
            # Being explicit: We do not yet want >1 grams.
            word = words[0]
            if word not in unique_words:
                unique_words.append(word)
        else:
            if words not in multi_words:
                multi_words.append(words)

    # Second loop checks for overlap with longer sequences.
    for multi_word_tuple in multi_words:
        # "Are none of the seen words in the current multiword?"
        if all(
            [word not in unique_words for word in multi_word_tuple]
        ):
            recomposed_multi_word = " ".join(multi_word_tuple)
            unique_words.append(recomposed_multi_word)

    return unique_words


if __name__ == "__main__":
    cli_parser = set_up_parser()
    args = cli_parser.parse_args()

    data = load_file(args.filename)
    validate_data(data, args)
    print(f"Original dataset length: {len(data)}.")

    # Keeping only toxic or abuse words.
    toxic_words_df = data[data[args.annotation_col] == args.positive_label]
    toxic_words_only = toxic_words_df[args.word_col].to_list()
    print(f"Length of positive annotation filtering: {len(toxic_words_only)}.")

    # Dupe filtering.
    # TODO dupe filtering with existing wordlist.
    unique_toxic_words_only = filter_overlaps_and_sort(toxic_words_only)
    print(f"Length after overlap filtering: {len(unique_toxic_words_only)}.")

    # Obscuring each word.
    encoded_words = [obscure(word) for word in unique_toxic_words_only]

    # This really shouldn't happen, but this check doesn't cost much and could save heartache.
    decoded_words = [unobscure(word) for word in encoded_words]
    for orig_word, decoded_word in zip(unique_toxic_words_only, decoded_words):
        if orig_word != decoded_word:
            raise ObscuringError(f"Encoding changed a word: {orig_word} -> {decoded_word}")

    # Writing out.
    with open(args.out_file, "wb") as toxic_file:
        for encoded_word in encoded_words:
            toxic_file.write(encoded_word)
            toxic_file.write(b"\n")
    print(f"Obscured word list written to {args.out_file}")


