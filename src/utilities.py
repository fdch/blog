#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyleft (c) 2022, Fede Camara Halac.
# Distributed under the terms of the GNU General Public License
# -----------------------------------------------------------------------------
from re import compile, UNICODE
import datetime

__all__ = [
  'make_timetag',
  'make_post',
  'replace_dir',
  'expand_attributes',
  'clean_emojis',
  'make_url',
  'get_timestamp'
]

def make_url(url, text=None, title=None, target='_top'):
  """ Returns a html link anchor tag """
  if text is None:
    text = url
  if title is None:
    title = text
  return f"<a href=\"{url}\" title=\"{title}\" target=\"{target}\">{text}</a>"

def get_timestamp(timestring=None, date_format='%Y-%m-%d %H:%M:%S'):
  if timestring is None:
    return datetime.datetime.now()
  else:
    date = lambda fmt: datetime.datetime.strptime(timestring, fmt)
    try:
      return date(date_format)
    except ValueError:
      try:
        return date('%Y-%m-%d %H:%M')
      except ValueError:
        try:
          return date('%Y-%m-%d')
        except ValueError:
          print(f"Could not parse timestamp: {timestring}... I'll make it up")
          return get_timestamp()


def make_timetag(timestamp):  
  """  format date 01-14-2022 18:00:00 to timestamp """
  text = f"{timestamp: %B %d, %Y, %H:%M}"
  return f"""<time title="{timestamp}" datetime="{timestamp}">{text}</time>"""

def make_post(id, title, content):
  """returns the wrapped html post"""
  return f"""
  <details id="{id}">
    <summary title="{title}">{title}</summary>
    <article>
      {content}
    </article>
  </details>
  """

def replace_dir(string):
  """ Redirects string from the previous directory to the current 
  Example
  -------

  images/img.jpg    -> an image
  posts/myfile.html -> contains src that points to ../images/img.jpg
  index.html        -> contains src that points to ./images/img.jpg

  Therefore, when placing code from posts/myfile.html into index.html,
  we need to replace_dir the src "../images/img.jpg" to "./images/img.jpg"


  """
  if str(string).startswith('../'):
    return str(string).replace('../','./')
  else:
    return string

def expand_attributes(attrs, quote='\"'):
  """ Expand attrs back to html string """
  if attrs:
    expand_attributes = lambda x : f"{x[0]}={quote}{replace_dir(x[1])}{quote}"
    return ' ' + ' '.join(list(map(expand_attributes, attrs)))
  else:
    return ''

def clean_emojis(text):
    """ Remove emojis and other non-safe characters from string
    Taken from SO: https://stackoverflow.com/a/49986645/8474128
    """
    regrex_pattern = compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = UNICODE)
    return regrex_pattern.sub(r'',text)
