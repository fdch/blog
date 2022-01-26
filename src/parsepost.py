#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyleft (c) 2022, Fede Camara Halac.
# Distributed under the terms of the GNU General Public License
# -----------------------------------------------------------------------------
import re
from xml.etree.ElementTree import ElementTree, Element, SubElement, Comment, indent, fromstring, tostring
from src.utilities import expand_attributes, get_timestamp

__all__ = ['ParsePost']

class ParsePost(object):
  def __init__(self, textfile):
    super().__init__()
    self.textfile = textfile
    self.email = 'fdch@nyu.edu'
    self.author = 'Fede Camara Halac'
    self.encoding = 'utf-8'
    self.doctype = '<!DOCTYPE html>'
    self.viewport = (('width', 'device-width'), ('initial-scale', 1))
    self.css = '../css/main.css'
    self.ui = '../js/ui.js'
    self.description = "This is a blog where I post various thoughts, things I've learnt, and random ideas."
    self.keywords = ['programming', 'journal', 'blogging', 'composition']
    self.outcome = "If you'd like to contact me, email me at: "
    self.article_class = 'single-article'
    self.autoindent = True
    
    self.root = None
    self.post = []
    
    with open(self.textfile, 'r') as fp:
      self.text = fp.readlines()

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
    p_keywords = re.compile(r'^keywords:\s+')
    p_description = re.compile(r'^description:\s+')
    p_subtitle = re.compile(r'^subtitle:\s+')
    p_time = re.compile(r'^time:\s+')
    p_image = re.compile(r'^image:\s+')
    p_block = re.compile(r'^\|\s+')
    p_ulist = re.compile(r'^-\s+')
    p_olist = re.compile(r'^[0-9]\.\s+')
    p_html_open = re.compile(r'^<\w+>')
    p_code = re.compile(r'^\s*```(.*)')
    p_comment = re.compile(r'^//.*')

    # def check_for_inlines(element, s):
    #   """ Check if the string s contains inline elements. 
    #   `` is code block
    #   ** is bold
    #   * is italic
    #   _ is underline
    #   ~ is strike

    #   """
      # element = check_for_block(element, s)
      # element = check_for_block(element, element.text, char='*', tag='i')
      # element = check_for_block(element, element.text, char='**', tag='b')
      # element = check_for_block(element, element.text, char='~', tag='s')
      # return element

    def check_for_block(element, s):
      """ Check for the `char` character to open and close inline `code` blocks. """
      curr_inblock = False
      prev_inblock = not curr_inblock
      sub = None
      sub_array = []
      count = 0
      
      if '`' not in s:
        element.text = s
        return element

      for i in s:
        if i == '`':
          curr_inblock = not curr_inblock
        else:
          if prev_inblock != curr_inblock:
            sub = Element('code') if curr_inblock else sub
            if count % 2 == 0:
              sub_array.append(sub)
            prev_inblock = curr_inblock
          
          if curr_inblock:
            if sub.text is None:
              sub.text = ''
            sub.text += i
          else:
            if sub is None:
              if element.text is None:
                element.text = ''
              element.text += i
            else:
              if sub_array[-1].tail is None:
                sub_array[-1].tail = ''
              sub_array[-1].tail += i
      
      for idx,e in enumerate(sub_array[1:]):
        if idx % 2 == 0:
          element.append(e)

      return element


    def check_for_links(element, s):
      """ Check if the string s contains a link. 
      Notes
      -----
      Only matches the last link.
      """
      links = re.compile(r'.*\[.*\]\(.*\).*')
      found_links = re.findall(links, s)
      # print(found_links)

      if found_links:
        link = found_links.pop(0)
        n = re.compile(r'(?P<prev>.*)\[(?P<text>.*)\]\((?P<url>.*)\)(?P<post>.*)')
        m = re.match(n, link)
        # print('text', m.group('text'))
        # print('url', m.group('url'))
        # print('pref', m.group('prev'))
        # print('post',m.group('post'))
        
        if m.group('prev'):
          element = check_for_block(element, m.group('prev'))
        
        def make_link(element, url, text, post):
          a = Element('a')
          a.attrib.update({'href': url or ''})
          a.text = text or url or ''
          a.tail = post or ''
          element.append(a)
        
        make_link(element, m.group('url'), m.group('text'), m.group('post'))
        # while True:
        #   try:
        #     link = found_links.pop(0)
        #   except IndexError:
        #     break
        #   m = re.match(n, link)
        #   make_link(element, m.group('url'), m.group('text'), m.group('post'))

      else:
        element = check_for_block(element, s)
        # element.text = s


      return element

    code_toggle = False
    
    # is it a new line
    is_new_line = lambda s: re.match(r'^\n$', s) or re.match(r'^\r\n$', s)

    # function to remove the tag from the fd format
    clean = lambda s,p: re.sub(p,'',s).strip()
    
    # go through the lines
    for s in self.text:

      # The code block
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
      
      # The raw html input ( not checked for validity )
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
      
      # The Meta description
      elif re.match(p_description, s):
        self.description = clean(s, p_description)
        continue

      # The Meta keywords
      elif re.match(p_keywords, s):
        self.keywords = clean(s, p_keywords).split(',')
        continue

      # The comments to ignore
      elif re.match(p_comment, s):
        tag = Comment(s.replace('//', ''))
        self.post.append(tag)
        continue

      # The title
      elif re.match(p_title, s):
        self.title_tag = Element('h1')
        self.title_tag = check_for_block(self.title_tag, clean(s, p_title))
        # store the title for the <title> tag
        self.title = self.title_tag.text
        continue
      
      # The subtitle
      elif re.match(p_subtitle, s):
        tag = Element('h2')
        tag = check_for_block(tag, clean(s, p_subtitle))
        self.post.append(tag)
        continue
      
      # The timestamp
      elif re.match(p_time, s):
        self.time_tag = Element('time')
        data = clean(s, p_time).split('|')
        timestamp, time_tag = None, None
        if len(data):
          timestamp = data.pop(0).strip()
          self.time_tag.attrib.update({'datetime': timestamp})
        if len(data):
          time_tag = data.pop(0).strip()
        self.timestamp = get_timestamp(timestamp)
        self.timestring = self.timestamp.isoformat(sep=' ')
        self.time_tag.text = time_tag or timestamp or ''
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
          tag.append(check_for_links(Element('li'), s))
        b_olist = []
        self.post.append(tag)
        continue
      
      elif len(b_ulist):
        tag = Element('ul')
        for s in b_ulist:
          tag.append(check_for_links(Element('li'), s))
        b_ulist = []
        self.post.append(tag)
        continue

      elif len(b_par):
        tag = Element('p')
        tag = check_for_links(tag, ' '.join(b_par).strip())
        b_par = []
        self.post.append(tag)
        continue
      
      elif len(b_block):
        tag = Element('blockquote')
        tag = check_for_links(tag, clean(' '.join(b_block), p_block))
        b_block = []
        self.post.append(tag)
        continue

      consecutive_lines = 0
  
  def compile(self):
    
    # The HTML root element <html>
    self.root = Element('html', attrib={'lang': 'en'})
    
    # The <head>
    head = SubElement(self.root, 'head')
    SubElement(head, 'meta', attrib={'charset': self.encoding})
    SubElement(head, 'meta', attrib={'name': 'viewport', 'content':expand_attributes(self.viewport, quote='').strip()})
    SubElement(head, 'meta', attrib={'name': 'author', 'content': self.author})
    SubElement(head, 'meta', attrib={'name': 'description', 'content': self.description})
    SubElement(head, 'meta', attrib={'name': 'keywords', 'content': ','.join(self.keywords)})
    SubElement(head, 'link', attrib={'rel': 'stylesheet', 'href': self.css})
    SubElement(head, 'title').text = self.title
    
    # The <body>
    body = SubElement(self.root, 'body')
    
    # [BODY] The <nav> element
    nav = SubElement(body, 'nav')
    SubElement(nav, 'button', attrib={'class': 'back'})
    SubElement(nav, 'button', attrib={'class': 'mode'})
    # [BODY] The <main> element
    main = SubElement(body, 'main', attrib={'class': self.article_class})

    # [BODY>MAIN] The <header> element
    header = SubElement(main, 'header')
    header.append(self.time_tag)
    header.append(self.title_tag)
    
    # [BODY>MAIN] The Post content
    for tag in self.post:
      main.append(tag)
    
    # [BODY] The <footer>
    footer = SubElement(body, 'footer')
    ft = SubElement(footer, 'time', attrib={'datetime': self.timestring})
    ft.text = "Published on " + self.timestring
    ad = SubElement(footer, 'address')
    p = SubElement(ad,'p')
    p.text = self.outcome
    SubElement(p,'a',attrib={'href':'mailto:%s' % self.email}).text=self.email
    footer.append(nav)
    
    # [BODY] The <script> at the end of <body>
    SubElement(body, 'script', attrib={'src': self.ui, 'charset':self.encoding})

  def write(self, filename=None):
    
    if self.autoindent:
      indent(self.root)

    with open(filename or self.textfile+'.html', 'wb') as fp:
      fp.write(f"{self.doctype}\n".encode(self.encoding))
      ElementTree(self.root).write(fp, encoding=self.encoding, xml_declaration=False, method='html')
