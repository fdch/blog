#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyleft (c) 2022, Fede Camara Halac.
# Distributed under the terms of the GNU General Public License
# -----------------------------------------------------------------------------
from html.parser import HTMLParser
from .utilities import expand_attributes, make_timetag, get_timestamp

__all__ = ['DelPost']

class DelPost(HTMLParser):
  def __init__(self):
    super().__init__()
    
    # Configure Time attributes
    self.timestamp = get_timestamp()
    self.timetag = make_timetag(self.timestamp)

    # Start with a doctype
    self.out = f"<!DOCTYPE html>"
    
    # The posts section tag to look for (and its id:posts)
    self.tag = 'section' 
    self.attr = ('id', 'posts')

    # flags to control the parser
    self.in_posts = False # are we in the posts section?
    self.in_footer = False # are we in the footer section?
    self.last_tag = '' # last tag we saw

  def copy_tag(self, tag, attrs):
    """ Copy start tag and attributes to output """
    self.out += f"<{tag}"
    self.out += expand_attributes(attrs) if attrs else ''
    self.out += ">"

  def copy_end(self, tag):
    """ Copy end tag to output """
    self.out += f"</{tag}>" 
  
  def is_in_tag(self, tag, attrs):
    """ Check if we are in the tag we want """
    if tag == self.tag:
      for attr in attrs:
        if attr[0] == self.attr[0] and attr[1] == self.attr[1]:
          self.in_posts = True

  def handle_starttag(self, tag, attrs):
    if self.in_posts:
      return
    
    self.last_tag = tag
    
    if tag == 'footer':
      self.in_footer = True
    
    if self.in_footer and tag == 'time':
      return
    
    self.copy_tag(tag, attrs)
    self.is_in_tag(tag, attrs)

  def handle_endtag(self, tag):
    if self.in_posts:
      if tag == self.tag:
        self.in_posts = False
        self.copy_end(self.tag)
      return
    if self.in_footer:
      self.in_footer = False
      if tag == 'time':
        return
    self.copy_end(tag)
  
  def handle_data(self, data):
    if self.in_posts:
      return
    if self.in_footer and self.last_tag == 'time':
      self.out += self.timetag
      return
    self.out += data
  
  def handle_comment(self, data):
    if self.in_posts:
      return
    self.out += f"<!--{data}-->"
