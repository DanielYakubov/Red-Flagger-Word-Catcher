"""A script to run to avoid duplicate words post annotations"""

# # for bigrams, we want to avoid overlaps with unigrams
# for w1, w2 in all_bigrams:
#     if w1 not in all_unigrams and w2 not in all_unigrams:
#         all_bigrams_processed.append(" ".join([w1, w2]))
#     else:
#         print(w1, w2)

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