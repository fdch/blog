#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyleft (c) 2022, Fede Camara Halac.
# Distributed under the terms of the GNU General Public License
# -----------------------------------------------------------------------------
from .delpost import DelPost

__all__ = ['FillPost']

class FillPost(DelPost):
  def __init__(self, new_data=None):
    super().__init__()
    self.new_data = new_data

  def handle_starttag(self, tag, attrs):
    self.copy_tag(tag, attrs)
    self.is_in_tag(tag, attrs)
    self.last_tag = tag
    if self.in_posts:
      self.out += self.new_data
    
  def handle_endtag(self, tag):
    self.copy_end(tag)
    if self.in_posts and tag == self.tag:
      self.in_posts = False
    self.last_tag = ''
  
  def handle_data(self, data):
    self.out += data
