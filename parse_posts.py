#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyleft (c) 2022, Fede Camara Halac.
# Distributed under the terms of the GNU General Public License
# -----------------------------------------------------------------------------
from src.parsepost import ParsePost  
from pathlib import Path

def main(texts_dir, posts_dir):

  posts_dir += '/' if not str(posts_dir).endswith('/') else ''
  texts_dir += '/' if not str(texts_dir).endswith('/') else ''

  texts_files = Path(texts_dir).glob('*.txt')
  posts_files = Path(posts_dir).glob('*.html')

  for i in texts_files:
    if i.stem not in [j.stem for j in posts_files]:
      print("Converting:", i.stem)
      parser = ParsePost(i)
      parser.parse()
      parser.compile()
      parser.write(posts_dir + '/' + i.stem + '.html')


# -----------------------------------------------------------------------------
# Begin main program
# -----------------------------------------------------------------------------

if __name__ == "__main__":
  import sys
  args = sys.argv[1:]
  if len(args) >= 2:
    from os.path import exists
    if not exists(args[0]): 
      raise Exception(f"{args[0]} does not exist")
    else:
      texts_dir = args[0]
    if not exists(args[1]): 
      raise Exception(f"{args[1]} does not exist")
    else:
      posts_dir = args[1]
    if len(args) > 2 :
      print("Ignoring extra arguments:", args[2:])
  else:
    raise Exception("Not enough arguments")
  
  main(texts_dir, posts_dir)