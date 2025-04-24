"""A script to run to avoid duplicate words post annotations"""

import argparse
import os
import pandas as pd

from red_flagger.obscure_data import obscure, unobscure, ObscuringError
from red_flagger.utils import filter_overlaps_and_sort

OUT_FILEPATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "abuse_flagger",
    "data",
    "toxic_keywords_b16.txt",
)


class ArgsError(Exception):
    pass


def set_up_parser() -> argparse.ArgumentParser:
    """Set up the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog="AnnotationPostProcessing",
        description="Processes an annotated wordlist and"
        " adds it to the stored global blacklist.",
    )
    parser.add_argument("filename", help="The path to the annotation file.")
    parser.add_argument(
        "--word_col",
        help="The name of the column containing the toxic words.",
        default="words_to_check",
    )
    parser.add_argument(
        "--annotation_col",
        help="The name of the column containing the binary annotations.",
        default="Abuse Term (Y/N)",
    )
    parser.add_argument(
        "--positive_label",
        help="The string that represents a positive annotation"
        " in the annotation_col.",
        default="y",
    )
    parser.add_argument(
        "--negative_label",
        help="The string that represents a negative annotation"
        " in the annotation_col",
        default="n",
    )
    parser.add_argument(
        "--out_file",
        help="The name of the file to write to.",
        default=OUT_FILEPATH,
    )

    return parser


def load_file(filename) -> pd.DataFrame:
    """Load in the file with an informative error in case something is off."""
    if not os.path.exists(filename):
        raise ValueError(
            f"The file name provided does not exist. File name: {filename}"
        )
    return pd.read_csv(filename)


def validate_data(df: pd.DataFrame, args: argparse.Namespace) -> None:
    """Validate the loaded in dataframe with the user specified args.
    This tries to catch any simple schema errors."""
    if args.word_col not in df.columns:
        raise ArgsError(f"word_col {args.word_col} not found in {df.columns}.")
    if args.annotation_col not in df.columns:
        raise ArgsError(
            f"Annotation_col {args.annotation_col} not found in {df.columns}."
        )
    if set(df[args.annotation_col]) - set(
        (args.positive_label, args.negative_label)
    ):
        raise ArgsError(
            f'Annotations other than positive_label "{args.positive_label}"'
            f' and negative_label "{args.negative_label}" '
            f"found in annotation_col {args.annotation_col}."
        )
    if os.path.exists(args.out_file):
        input(
            f"WARNING: Execution of this script will override {args.out_file}."
        )


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

    # This really shouldn't happen, this check doesn't cost much though.
    decoded_words = [unobscure(word) for word in encoded_words]
    for orig_word, decoded_word in zip(unique_toxic_words_only, decoded_words):
        if orig_word != decoded_word:
            raise ObscuringError(
                f"Encoding changed a word: {orig_word} -> {decoded_word}"
            )

    # Writing out.
    with open(args.out_file, "wb") as toxic_file:
        for encoded_word in encoded_words:
            toxic_file.write(encoded_word)
            toxic_file.write(b"\n")
    print(f"Obscured word list written to {args.out_file}")
