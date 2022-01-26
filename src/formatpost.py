#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyleft (c) 2022, Fede Camara Halac.
# Distributed under the terms of the GNU General Public License
# -----------------------------------------------------------------------------
from html import escape as html_escape
from .delpost import DelPost
from .utilities import make_url, clean_emojis, expand_attributes, make_post, get_timestamp

__all__ = ['FormatPost']

class FormatPost(DelPost):
  """ Format an html post

  Description:
  ------------
  This class will grab the html from the post:
  - keeping only the relevant content (no html,head,or meta-tags)
  - changing <h1> to <h2>, 
  - and wrapping the post in a <details> tag, see FormatPost.wrap()

  """

  def __init__(self, url, max_id=20):
    """ Instantiate with the url of the post and its id max char length"""
    super().__init__()
    # the time string for the post
    self.timestamp = None
    # the url of the post for its permalink
    self.url = url     
    # tags to ignore in the post
    self.ignore = ('html', 'head', 'body', 'meta', 'title', 'link')
    # characters of the <details> id field
    self.max_id = max_id
    
    self.title = ''
    self.out = ''
    self.post_id = ''
    # flags to control the parsing
    self.nodata = True
    self.in_main = False
    self.in_title = False
    self.in_time = False

  def make_id(self, data):
    """returns a formatted string of the post id"""
    d = clean_emojis(data)
    if self.max_id < len(d):
      d = d[:self.max_id]
    return d.replace(' ', '-').lower()

  def handle_starttag(self, tag, attrs):
    
    self.last_tag = tag
    
    if tag == 'main':
      self.in_main = True
    if tag == 'time':
      self.in_time = True
    if tag == 'title':
      self.in_title = True
    
    if not self.in_main: 
      return
    
    # converts h1 to h2
    if self.in_title and tag == 'h1':
      self.out += f"\n<h2" 
    else:
      self.out += f"\n<{tag}"
    
    # populate attributes
    self.out += expand_attributes(attrs)
    
    # end the tag
    self.out += ">"

    # grab datetime attr if present
    if tag == 'time':
      for k, v in attrs:
        if k == 'datetime':
          self.timestamp = get_timestamp(v)
          break

  
  def handle_endtag(self, tag):
    if tag == 'main':
      self.in_main = False

    if not self.in_main:
      return
    
    if tag == 'time':
      self.in_time = False
    
    if self.in_title and tag == "h1":
      self.copy_end('h2')
      self.in_title = False
    else:
      self.copy_end(tag)
    
    if tag == 'code':
      self.out += ' '
    
  def handle_data(self, data):
    
    if not self.in_main:
      return
    
    data = html_escape(str(data))
    
    if self.in_title:
      self.post_id = self.make_id(data)
      if self.last_tag == 'h1':
        self.title += data
    
    if self.in_time: 
      # remove newline from data
      data = data.replace('\n', '').strip()
      # timestamp - the permalink url
      if self.timestamp is None:
        self.timestamp = get_timestamp(data)
      data += ' - '
      data += make_url(self.url, text="permalink", title='Open in new tab')
      if self.last_tag == 'a':
        return
    
    # fill it with the content
    self.out += data.strip() 

  def output(self):
    """ Returns a tuple with the wrapped html post and the timestamp """
    return (make_post(self.post_id, self.title, self.out), self.timestamp)

