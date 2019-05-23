import os
import sys
import glob
from opencc import OpenCC


def main(argv):
  input_dir = argv[1]
  output_dir = argv[2]
  cc = OpenCC('t2s')

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
        fout.write(cc.convert(line))


if __name__ == "__main__":
  main(sys.argv)
