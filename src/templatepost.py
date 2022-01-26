#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyleft (c) 2022, Fede Camara Halac.
# Distributed under the terms of the GNU General Public License
# -----------------------------------------------------------------------------

from xml.etree.ElementTree import ElementTree, Element, SubElement, indent
from src.utilities import expand_attributes

__all__ = ['TemplatePost']

class TemplatePost(object):
  
  def __init__(self):
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


  def write(self, filename):

    if self.autoindent:
      indent(self.root)

    with open(filename, 'wb') as fp:

      fp.write(f"{self.doctype}\n".encode(self.encoding))      
      ElementTree(self.root).write(fp, 
                                   encoding=self.encoding, 
                                   xml_declaration=False, 
                                   method='html')

