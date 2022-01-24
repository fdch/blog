#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyleft (c) 2022, Fede Camara Halac.
# Distributed under the terms of the GNU General Public License
# -----------------------------------------------------------------------------
import datetime
import re
from xml.etree.ElementTree import ElementTree, Element, SubElement, indent, fromstring

__all__ = ['ParsePost']

class ParsePost(object):
  def __init__(self, textfile):
    super().__init__()
    self.textfile = textfile
    with open(self.textfile, 'r') as fp:
      self.text = fp.readlines()
    self.post = []
  
  def parse(self):
    """ Parse the text file and return a string with the HTML code. """
    
    consecutive_lines = 0
    is_html = False
    html_tag = None
    
    b_block = [] # buffer for a blockquote
    b_olist = [] # buffer for an ordered list
    b_ulist = [] # buffer for an unordered list
    b_par = []   # buffer for a paragraph
    b_html = []  # buffer for an html tag
    b_code = []  # buffer for a code block
    
    # regexes
    p_title = re.compile(r'^title:\s+')
    p_subtitle = re.compile(r'^subtitle:\s+')
    p_image = re.compile(r'^image:\s+')
    p_block = re.compile(r'^\|\s+')
    p_ulist = re.compile(r'^-\s+')
    p_olist = re.compile(r'^[0-9]\.\s+')
    p_html_open = re.compile(r'^<\w+>')
    p_code = re.compile(r'^\s*```(.*)')

    code_toggle = False
    
    # is it a new line
    is_new_line = lambda s: re.match(r'^\n$', s) or re.match(r'^\r\n$', s)

    # function to remove the tag from the fd format
    clean = lambda s,p: re.sub(p,'',s).strip()
    
    # go through the lines
    for s in self.text:

      if re.match(p_code, s):
        code_lang = re.match(p_code, s).group(1)
        if code_lang:
          code_language = code_lang
        code_toggle = not code_toggle
        if not code_toggle and len(b_code):
          tag = Element('pre')
          if code_language:
            tag.attrib.update({'language': code_language})
          tag.text = ''.join(b_code)
          b_code = []
          self.post.append(tag)
        continue

      if code_toggle:
        b_code.append(s)
        continue

      if is_html and (html_tag is not None):
        if re.match(rf".*</{html_tag}>", s):
          is_html = False
          b_html.append(s)
          self.post.append(fromstring(''.join(b_html)))
          b_html = []
          html_tag = None
        else:
          b_html.append(s)
        continue

      # The title
      elif re.match(p_title, s):
        tag = Element('h1')
        tag.text = clean(s, p_title)
        # store the title for the <title> tag
        self.title = tag.text
        self.post.append(tag)
        continue
      
      # The subtitle
      elif re.match(p_subtitle, s):
        tag = Element('h2')
        tag.text = clean(s, p_subtitle)
        self.post.append(tag)
        continue
      
      # The image
      elif re.match(p_image, s):
        tag = Element('figure')
        data = clean(s, p_image).split('|')
        url, title, caption = None, None, None
        
        if len(data): url = data.pop(0).strip()
        if len(data): caption = data.pop(0).strip()
        if len(data): title = data.pop(0).strip()
        img = SubElement(tag, 'img')
        img.attrib.update({'src': url or ''})
        img.attrib.update({'alt': title or caption or ''})
        img.attrib.update({'title': title or caption or ''})
        
        if caption:
          figcaption = SubElement(tag, 'figcaption')
          figcaption.text = caption.strip()
        
        # take care of this here...
        self.post.append(tag)
        continue
      
      # The blockquote
      elif re.match(p_block, s):
        b_block.append(clean(s, p_block))
        continue
      
      # The unordered list
      elif re.match(p_ulist, s):
        b_ulist.append(clean(s, p_ulist))
        continue

      # The ordered list
      elif re.match(p_olist, s):
        b_olist.append(clean(s, p_olist))
        continue
    
      # Ignore empty lines
      elif is_new_line(s):
        consecutive_lines += 1
        if consecutive_lines <= 1:
          continue
      
      elif re.match(p_html_open, s):
        __tag__ = re.match(p_html_open, s).group(0)[1:-1]
        if re.match(rf".*</{__tag__}>", s):
          self.post.append(fromstring(s))
        else:
          b_html.append(s)
          is_html = True
          if html_tag is None:
            html_tag = __tag__
        continue

      # The paragraph (everything else)
      else:
        b_par.append(s)
        continue
      
      if len(b_olist):
        tag = Element('ol')
        for s in b_olist:
          SubElement(tag, 'li').text = s
        b_olist = []
        self.post.append(tag)
        continue
      
      elif len(b_ulist):
        tag = Element('ul')
        for s in b_ulist:
          SubElement(tag, 'li').text = s
        b_ulist = []
        self.post.append(tag)
        continue

      elif len(b_par):
        tag = Element('p')
        tag.text = ' '.join(b_par).strip()
        b_par = []
        self.post.append(tag)
        continue
      
      elif len(b_block):
        tag = Element('blockquote')
        tag.text = clean(' '.join(b_block), p_block)
        b_block = []
        self.post.append(tag)
        continue
    


      consecutive_lines = 0
  
  def compile(self):
    root = Element('html', attrib={'lang': 'en'})

    head = SubElement(root, 'head')
    SubElement(head, 'title').text = self.title
    
    body = SubElement(root, 'body')
    for tag in self.post:
      body.append(tag)
    
    SubElement(body, 'footer').text = 'This is the footer: ' + datetime.datetime.now().isoformat()

    indent(root)

    with open(self.textfile+'.html', 'wb') as fp:
      fp.write('<!DOCTYPE html>\n'.encode('utf-8'))
      ElementTree(root).write(fp, encoding='utf-8', xml_declaration=False)

