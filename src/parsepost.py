#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyleft (c) 2022, Fede Camara Halac.
# Distributed under the terms of the GNU General Public License
# -----------------------------------------------------------------------------

import datetime
import re
from xml.etree.ElementTree import ElementTree, Element, SubElement, indent
from .delpost import DelPost

# import re

__all__ = ['ParsePost']

class ParsePost(DelPost):
  def __init__(self, textfile):
    super().__init__()
    # self.new_data = new_data
    self.textfile = textfile
    with open(self.textfile, 'r') as fp:
      self.text = fp.readlines()
    self.post = []
  
  def parse(self):
    """ Parse the text file and return a string with the HTML code. """
    prevtag = None
    in_block = False
    in_par = False
    for s in self.text:
      
      if s.startswith('title:'):
        in_block, in_par, in_ul = False, False, False
        tag = Element('h1')
        tag.text = s.replace('title:', '', 1).strip()
        self.title = tag.text
      
      elif s.startswith('subtitle:'):
        in_block, in_par, in_ul = False, False, False
        tag = Element('h2')
        tag.text = s.replace('subtitle:', '', 1).strip()
      
      elif s.startswith('image:'):
        in_block, in_par, in_ul = False, False, False
        tag = Element('figure')
        data = s.replace('image:', '', 1).split('|')
        url, title, caption = None, None, None
        if len(data):
          url = data.pop(0).strip()
          if len(data):
            caption = data.pop(0).strip()
            if len(data):
              title = data.pop(0).strip()
        if url:
          img = SubElement(tag, 'img')
          img.attrib.update({'src': url or ''})
          img.attrib.update({'alt': title or caption or ''})
          img.attrib.update({'title': title or caption or ''})
        
        if caption:
          figcaption = SubElement(tag, 'figcaption')
          figcaption.text = caption.strip()
        
      elif s.startswith('|'):
        in_ul, in_par = False, False
        if in_block and (prevtag is not None):
          tag = prevtag
        else:
          tag = Element('blockquote')
        tag.text = s.replace('|', '', 1).strip()
        in_block = True
  
      elif s.startswith('-'):
        in_block, in_par = False, False
        if in_ul:
          tag = prevtag
        else:
          tag = Element('ul')

        li = SubElement(tag, 'li')
        li.text = s.replace('-', '', 1).strip()
        in_ul = True
        
    
      elif re.match(r'^\s+[0-9]', s):
        in_block, in_par, in_ul = False, False, False
        pass
    
      elif s.startswith('\n'):
        in_block, in_par, in_ul = False, False, False
        continue
      
      else:
        in_ul, in_block = False, False
        if in_par and (prevtag is not None):
          tag = prevtag
        else:
          tag = Element('p')
        tag.text = s.strip()
        in_par = True
      
      prevtag = tag
      self.post.append(tag)
  
  
  def compile(self):
    root = Element('html', attrib={'lang': 'en'})

    head = SubElement(root, 'head')
    title = SubElement(head, 'title')
    title.text = self.title
    
    body = SubElement(root, 'body')
    for tag in self.post:
      body.append(tag)
    
    footer = SubElement(body, 'footer')
    footer.text = 'This is the footer: ' + datetime.datetime.now().isoformat()

    indent(root)

    with open(self.textfile+'.html', 'wb') as fp:
      fp.write('<!DOCTYPE html>\n'.encode('utf-8'))
      ElementTree(root).write(fp, encoding='utf-8', xml_declaration=False)