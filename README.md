# Wikipedia Word2Vec

This repository uses gensim to train word2vec from wiki dump, especially for Chinese Wikipedia data

1 Down wiki data from [Wikimedia Downloads](https://dumps.wikimedia.org/backup-index.html)


2 Use [wikiextractor](https://github.com/attardi/wikiextractor) to extract and cleans wiki text.

```bash
git clone https://github.com/attardi/wikiextractor.git
cd wikiextractor
python WikiExtractor.py -i path/to/wiki_dump -o path/to/extract_dir
``` 

3 For Chinese user, you might want to convert traditional Chinese to simplified Chinese. [OpenCC](https://github.com/BYVoid/OpenCC) or pure python version [OpenCC-Python](https://github.com/yichen0831/opencc-python) could be used. Use following script to make the conversion.
```bash
python opencc_zhwiki_t2s.py path/to/extract_dir path/to/convert_dir 
```

4 Finnally we could train the vector, we borrow the tokenizer from [BERT](https://github.com/google-research/bert)
```bash
python wiki_word2vec.py path/to/extract_dir-or-convert_dir path/to/word2vec
```


