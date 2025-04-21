# Abuse Keywords (name-in-progress)

A repository containing a software that does keyword-based abuse flagging. It is designed with a philosophy of sensitivity and therefore a focus on recall rather than precision. It detects from a term list that contain terms that are indicative of hate speech, system abuse, toxicity, violence, or general profinity/obscenity. 

## Important Note on Keyword Detection Systems!

We highly discourage the use of keyword systems as the only line of defense for toxicity and/or abuse detection. Problems associated with keyword detection systems range from performance issues to socially harmful false positives in cases like reclaimation. This system is encouraged to be used in conjunction with a review process and/or a stronger classification systems such as a deep learning model. 

## Dataset Obscurity

The word list is obscured as a base16 representation of the list of hate words. We did not feel comfortable exposing this list and we discourage any non-base16 representations of the wordlist being uploaded elsewhere. For details on dataset creation, see `README.md` in `data_building/`.
