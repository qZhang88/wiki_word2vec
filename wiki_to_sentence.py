import os
import re
import sys
import glob
import logging

import gensim
from opencc import OpenCC

from tokenization import BasicTokenizer


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


def main(argv):
  input_dir = argv[1]
  output_dir = argv[2]
  tokenizer = BasicTokenizer()

  if not os.path.exists(output_dir):
    os.mkdir(output_dir)

  for folder in os.listdir(input_dir):
    input_folder = os.path.join(input_dir, folder)
    output_folder = os.path.join(output_dir, folder)
    os.mkdir(output_folder)

    for text in os.listdir(input_folder):
      fin = open(os.path.join(input_folder, text), 'r', encoding='utf8')
      fout = open(os.path.join(output_folder, text), 'w', encoding='utf8')
      for line in fin:
        if line.startswith('<doc') or line.startswith('</doc'):
          continue

        line = line.strip()
        if not line:
          continue

        for sentence in sentence_tokenize(line):
          fout.write(" ".join(tokenizer.tokenize(sentence)) + '\n')


if __name__ == "__main__":
  main(sys.argv)
