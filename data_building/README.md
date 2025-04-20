# Data Creation

This folder contains the scripts used to generate data for annotation and subsequently post-process the annotated data. 

## Procedure

### Initial Data Creation

The procedure used for generating the data is as follows:

**For Corpora**
1. Download the relevant datasets. Each dataset is processed separately in the following way.
2. Tokenize at the word level, create unigram, bigram, and trigram representations of the tokens for hatespeech items only.
3. Keep only the n most frequent ngrams. When the data was generated, it was n=500 for unigrams, n=300 for bigrams, and n=200 for trigrams. These are magic numbers and had to do with resource availability for annotation.
4. Remove any duplicate ngrams.

**For Lexicons / Keyword Lists**
1. Load in the word list.
2. Check if there is any duplicates between the word list items and the list of unigrams from previous step.

Once both data sources are generated, a sheet is generated for annotations containing 5,348 words. 

### Annotation

The dataset was then carefully annotated with binary labels y/n. A positive annotation of 'y' meant that the word is a slur, offensive, toxic, tied to harmful ideologies such as scientific racism, violent, or obscene. Annotation involved finding standard and non-standard definitions of the terms and erring on the side of sensitivity. 

### Post-Processing

The annotated data is then fed into a post processing script which filters negative annotations. Then, filters duplicates once more and checks for overlap, mainly if any of the n>1 grams contain any unigrams. If this is the case, the ngram is filtered. After this filtering, the dataset ends up containing 1912 items.

Each item is then converted into base16 in order to obscure the wordlist, and then streamed into a file. The words are obscured as a form of reversible censorship, reversible just in case one needs to see all of the words for any reason (i.e. double-checking the annotations, research reporting, etc.). 

## Dataset Citations

### Sources for Corpora
Binny Mathew, Punyajoy Saha, Seid Muhie Yimam, Chris Biemann, Pawan Goyal, & Animesh Mukherjee. (2022). HateXplain: A Benchmark Dataset for Explainable Hate Speech Detection.

Davidson, T., Warmsley, D., Macy, M., & Weber, I. (2017). Automated Hate Speech Detection and the Problem of Offensive Language. In Proceedings of the 11th International AAAI Conference on Web and Social Media (pp. 512-515).

Mantas Mazeika, Long Phan, Xuwang Yin, Andy Zou, Zifan Wang, Norman Mu, Elham Sakhaee, Nathaniel Li, Steven Basart, Bo Li, David Forsyth, & Dan Hendrycks (2024). HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal.

Zampieri, M., Malmasi, S., Nakov, P., Rosenthal, S., Farra, N., & Kumar, R. (2019). Predicting the Type and Target of Offensive Posts in Social Media. In Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers) (pp. 1415–1420). Association for Computational Linguistics.

Zi Lin, Zihan Wang, Yongqi Tong, Yangkun Wang, Yuxin Guo, Yujia Wang, & Jingbo Shang. (2023). ToxicChat: Unveiling Hidden Challenges of Toxicity Detection in Real-World User-AI Conversation.

### Sources for Lexicons / Keyword Lists

https://github.com/dan-hickey1/musk-hate-lexicon/blob/main/hate_keywords.txt

https://github.com/hate-alert/HateBegetsHate_CSCW2020/blob/master/HateLexicons.txt

https://github.com/martinigoyanes/LexiconGST/tree/main/data/lexicons

https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/blob/master/en
