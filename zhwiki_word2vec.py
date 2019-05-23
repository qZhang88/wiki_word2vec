import os
import re
import sys
import glob
import logging

import gensim

from tokenization import BasicTokenizer


logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def sentence_tokenize(para):
  para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
  para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
  para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
  para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
  # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注
  # 意前面的几句都小心保留了双引号
  para = para.rstrip()  # 段尾如果有多余的\n就去掉它
  # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽
  # 略，需要的再做些简单调整即可。
  return para.split("\n")


class WikiSentenceGenerator:
  def __init__(self, wiki_dir):
    self.wiki_dir = wiki_dir
    self.tokenizer = BasicTokenizer()

  def __iter__(self):
    for text in glob.glob(os.path.join(self.wiki_dir, '*/wiki_*')):
      with open(text, 'r', encoding='utf8') as fin:
        for line in fin:
          if line.startswith('<doc') or line.startswith('</doc'):
            continue

          line = line.strip()
          if not line:
            continue

          for sentence in sentence_tokenize(line):
            # TODO: change low frequency word to <unk>, and use FullTokenizer
            yield self.tokenizer.tokenize(sentence)


def main(argv):
  zhwiki_dir = argv[1]
  output_path = argv[2]

  sentences = WikiSentenceGenerator(zhwiki_dir)

  # TODO: first build vocab
  model = gensim.models.Word2Vec(
      sentences,
      min_count=5,
      workers=8,
      iter=10)
  model.wv.save_word2vec_format(output_path)


if __name__ == "__main__":
  main(sys.argv)
