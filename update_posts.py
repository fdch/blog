#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyleft (c) 2022, Fede Camara Halac.
# Distributed under the terms of the GNU General Public License
# -----------------------------------------------------------------------------
from glob import glob
from src.formatpost import FormatPost
from src.delpost import DelPost
from src.fillpost import FillPost

def main(index_file="index.html", posts_dir="posts", new_index=None):
  
  if new_index is None: new_index = index_file

  # a list of tuples containing posts (html_data, timestamp)
  posts = []
  
  posts_dir += '/' if not str(posts_dir).endswith('/') else ''
  posts_dir += '*.html'

  # get the new data from the posts into the new data
  for post in glob(posts_dir):
    with open(post, 'r') as fp:
      # grab the post
      d = fp.read()
      # instantiate the formatter
      format = FormatPost(url=post, max_id=20)
      # run the parser
      format.feed(d)
      posts.append(format.output())
  
  if not posts:
    raise Exception(f"No posts found in: {posts_dir}")

  # Sort the new data by timestamp, get only the html
  posts.sort(key=lambda x: x[1], reverse=True)
  
  # read the index file, keep the template only
  with open(index_file, 'r') as fp:
    # instantiate the post delete handler
    template = DelPost()
    # This will simply delete the posts section
    template.feed(fp.read())
  
  # Instantiate the Filler and add the new data to it
  filler = FillPost(' '.join([x[0] for x in posts]))
  filler.feed(template.out)

  # Write the new index file
  with open(new_index, 'w') as fp:
    fp.write(filler.out)

# -----------------------------------------------------------------------------
# Begin main program
# -----------------------------------------------------------------------------

if __name__ == "__main__":
  import sys
  args = sys.argv[1:]
  if len(args) == 1:
    from os.path import exists
    if not exists(sys.argv[1]): 
      raise Exception(f"{sys.argv[1]} does not exist")
  
  main(*args)
