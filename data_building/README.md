This file contains script to build the list of keywords using ngram-based PMIs.

The procedure for each file is as follows - 
1. Download the relevant datasets. Each dataset is processed separately in the following way.
2. Tokenize at the word level, create unigram, bigram, and trigram representations of the tokens for hatespeech items only.
3. Sort by the most frequent ngrams in positive classes.
4. Manually review the most frequent values and construct the keyword list.

# Dataset Citations
@misc{mollas2020ethos,
      title={ETHOS: an Online Hate Speech Detection Dataset}, 
      author={Ioannis Mollas and Zoe Chrysopoulou and Stamatis Karlos and Grigorios Tsoumakas},
      year={2020},
      eprint={2006.08328},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}

@article{mazeika2024harmbench,
  title={HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal},
  author={Mantas Mazeika and Long Phan and Xuwang Yin and Andy Zou and Zifan Wang and Norman Mu and Elham Sakhaee and Nathaniel Li and Steven Basart and Bo Li and David Forsyth and Dan Hendrycks},
  year={2024},
  eprint={2402.04249},
  archivePrefix={arXiv},
  primaryClass={cs.LG}
}

@misc{lin2023toxicchat,
      title={ToxicChat: Unveiling Hidden Challenges of Toxicity Detection in Real-World User-AI Conversation}, 
      author={Zi Lin and Zihan Wang and Yongqi Tong and Yangkun Wang and Yuxin Guo and Yujia Wang and Jingbo Shang},
      year={2023},
      eprint={2310.17389},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}

@inproceedings{hateoffensive, title = {Automated Hate Speech Detection and the Problem of Offensive Language}, author = {Davidson, Thomas and Warmsley, Dana and Macy, Michael and Weber, Ingmar}, booktitle = {Proceedings of the 11th International AAAI Conference on Web and Social Media}, series = {ICWSM '17}, year = {2017}, location = {Montreal, Canada}, pages = {512-515} }