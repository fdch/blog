#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyleft (c) 2022, Fede Camara Halac.
# Distributed under the terms of the GNU General Public License
# -----------------------------------------------------------------------------
from src.parsepost import ParsePost  
from pathlib import Path

def main(d_from, d_to, overwrite=False):

  d_to += '/' if not str(d_to).endswith('/') else ''
  d_from += '/' if not str(d_from).endswith('/') else ''

  texts_files = Path(d_from).glob('*.txt')
  posts_files = Path(d_to).glob('*.html')
  touch = 0
  for i in texts_files:
    if i.stem not in [j.stem for j in posts_files] or overwrite:
      print("Converting:", i)
      parser = ParsePost(i)
      parser.parse()
      parser.compile()
      parser.write(d_to + '/' + i.stem + '.html')
      touch += 1
  
  if touch == 0:
    print("No new files to convert.")
  else:
    print("Converted", touch, "files.")


# -----------------------------------------------------------------------------
# Begin main program
# -----------------------------------------------------------------------------

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser(description='Convert a text file to HTML.')
  parser.add_argument('-f', '--from',
                      help='Directory with the text files.')
  parser.add_argument('-t', '--to',
                      help='Directory to store the HTML files.')
  parser.add_argument('-o', '--overwrite',
                      action='store_true',
                      help='Overwrite existing HTML files.')
  # Get the arguments
  args = parser.parse_args()
  # Run the main program
  main(getattr(args, 'from'), getattr(args, 'to'), getattr(args,'overwrite'))
  