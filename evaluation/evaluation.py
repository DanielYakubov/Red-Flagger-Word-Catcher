import os.path
from typing import Any, Iterable

import datasets
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)

from red_flagger.red_flagger import RedFlagger

AF = RedFlagger()


def _get_metrics(
    y_true: Iterable[Any], y_pred: Iterable[Any]
) -> tuple[float, float, float, float]:
    """Helper to get all metrics for evaluation."""
    return (
        round(accuracy_score(y_true, y_pred), 2),
        round(precision_score(y_true, y_pred), 2),
        round(recall_score(y_true, y_pred), 2),
        round(f1_score(y_true, y_pred), 2),
    )


def predict_offensive_dataset():
    """Getting the evaluations for the offensive language dataset
    that is made from The OLID dataset (Zampieri et al., 2019)
    and the labels from (Davidson et al.,2017)

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
    predicted_labels = [
        1 if AF.detect_abuse(item["text"], return_words=False) else 0
        for item in offensive_dataset["test"]
    ]
    print("Prediction on christinacdl/offensive_language_dataset done.")
    return _get_metrics(offensive_dataset["test"]["label"], predicted_labels)


def predict_xplain_dataset():
    """Getting the evaluations for the HateXplain Dataset
    from Mathew et al. (2021).

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
    gold_labels = []
    pred_labels = []
    for item in hxplain["test"]:
        annotations = item["annotators"]["label"]  # list of label
        text = " ".join(item["post_tokens"])
        if 0 in annotations or 2 in annotations:
            # 0: Hate, 2: Offensive
            # If any annotator found the text offensive, it is a positive class
            gold_labels.append(1)
        else:
            gold_labels.append(0)
        pred_labels.append(
            1 if AF.detect_abuse(text, return_words=False) else 0
        )
    print("Prediction on Hate-speech-CNERG/hatexplain done.")
    return _get_metrics(gold_labels, pred_labels)


def predict_tx_dataset():
    """Getting the evaluations for the Toxic Chat Dataset
    from Lin et al. (2023).

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
    pred_labels = [
        1 if AF.detect_abuse(item["user_input"], return_words=False) else 0
        for item in tx_dataset["test"]
    ]
    print("Prediction on lmsys/toxic-chat done.")
    return _get_metrics(tx_dataset["test"]["toxicity"], pred_labels)


# Turns out there is no test set...
# def predict_hso_dataset():
#     # from hatebase.org
#     hso_dataset = datasets.load_dataset("tdavidson/hate_speech_offensive")
#     gold_labels = []
#     pred_labels = []
#     for item in hso_dataset['dev']:
#         if item['class'] in [0, 1]:
#             # 0: Hate, 1: Offensive
#             gold_labels.append(1)
#         else:
#             gold_labels.append(0)
#     pred_labels.append(
#         1 if AF.detect_abuse(item["tweet"], return_words=False) else 0
#     )
#     print("Prediction on tdavidson/hate_speech_offensive done.")
#     return _get_metrics(gold_labels, pred_labels)

if __name__ == "__main__":
    # Some hard coding, but it's fine for now.
    lst = [
        predict_offensive_dataset(),
        predict_xplain_dataset(),
        predict_tx_dataset(),
    ]
    df = pd.DataFrame(
        data=lst, columns=["Accuracy", "Precision", "Recall", "F1"]
    )
    df.insert(
        loc=0,
        column="Dataset",
        value=["Offensive language", "HateXplain", "Toxic Chat"],
    )
    with open(
        os.path.join(os.path.dirname(__file__), "results.txt"), "w"
    ) as sink:
        sink.write(df.to_string(index=False))
