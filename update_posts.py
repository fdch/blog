import re
import glob
from html.parser import HTMLParser
from datetime import datetime

def deEmojify(text):
    """ Remove emojis and other non-safe characters from string
    Taken from SO: https://stackoverflow.com/a/49986645/8474128
    """
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

class DelPost(HTMLParser):
  def __init__(self):
    super().__init__()
    self.out = '<!DOCTYPE html>' # Start with a doctype
    # tag to look for 
    self.tag = 'section' 
    self.attr = ('id', 'posts') 
    self.in_posts = False # are we in the posts section?

  def expand_attrs(self, attrs):
    """ Expand attrs back to html string """
    if attrs:
      attrs = list(map(lambda x:f"{x[0]}=\"{x[1]}\"", attrs))
      return " " + " ".join(attrs)
    else:
      return ''

  def copy_start(self, tag, attrs):
    """ Copy start tag and attributes to output """
    self.out += f"<{tag}"
    self.out += self.expand_attrs(attrs)
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
    self.copy_start(tag, attrs)
    self.is_in_tag(tag, attrs)

  def handle_endtag(self, tag):
    if self.in_posts:
      if tag == self.tag:
        self.in_posts = False
        self.copy_end(self.tag)
      return
    self.copy_end(tag)
  
  def handle_data(self, data):
    if self.in_posts:
      return
    self.out += data
  
  def handle_comment(self, data):
    if self.in_posts:
      return
    self.out += f"<!--{data}-->"

class FillPost(DelPost):
  def __init__(self, new_data=None):
    super().__init__()
    self.new_data = new_data
    self.last_tag = ''

  def handle_starttag(self, tag, attrs):
    self.copy_start(tag, attrs)
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

class FormatPost(DelPost):
  def __init__(self, url, max_id=20):
    super().__init__()
    self.in_title = False
    self.in_time = False
    self.title = ''
    self.out = ''
    self.nodata = True
    self.ignore = ('html', 'head', 'body', 'meta', 'title')
    self.post_id = ''
    self.max_id = max_id # characters of the <details> id field
    self.url = url # the permalink url

  def make_id(self, data):
    """returns a formatted string of the post id"""
    d = deEmojify(data).replace(' ', '-')
    if self.max_id < len(d):
      return d[:self.max_id]
    else:
      return d

  def handle_starttag(self, tag, attrs):
    self.nodata = tag in self.ignore
    if self.nodata: 
      return
    # converts h1 to h2
    self.in_title = tag == 'h1'
    self.out += f"\n<h2" if self.in_title else f"\n<{tag}"
    # to get timestamp
    self.in_time = tag == 'time'
    # populate attributes
    self.out += self.expand_attrs(attrs)
    self.out += ">"
  
  def handle_endtag(self, tag):
    self.in_time = tag == 'time'
    self.nodata = tag in self.ignore
    if self.nodata:
      return
    
    if self.in_title and tag == "h1":
      self.copy_end('h2')
      self.in_title = False
    else:
      self.copy_end(tag)
    
  def handle_data(self, data):
    if self.nodata:
      return
    if self.in_title:
      self.title += data
      self.post_id = self.make_id(data)
    # format date 01/14/2022 18:00:00 to timestamp
    if self.in_time: 
      data = data.replace('\n', '').strip() # remove newline from data
      if data != '':
        self.timestamp = datetime.strptime(data, "%m-%d-%Y %H:%M:%S")
    # fill it with the content
    self.out += data

  def wrap(self):
    """returns the wrapped html post"""
    return f"""
    <details id="{self.post_id}">
      <summary>{self.title}</summary>
      <a href="{self.url}">permalink</a>
      <article>
        {self.out}
      </article>
    </details>
    """

  def output(self):
    """ Returns a tuple with the wrapped html post and the timestamp """
    return (self.wrap(), self.timestamp)

# -----------------------------------------------------------------------------
# Begin main program
# -----------------------------------------------------------------------------

if __name__ == "__main__":
  
  # a list of tuples containing (data, timestamp)
  new_data = []

  # get the new data from the posts into the new data
  for post in glob.glob('posts/*.html'):
    with open(post, 'r') as fp:
      # instantiate the formatter
      format = FormatPost(url=post, max_id=20)
      d = fp.read()
      # this will grab the html from the post
      # keeping only the relevant content (no html,head,or meta-tags)
      # changing the H1 to H2
      format.feed(d)
      # and it will wrap the html in a details tag
      # see FormatPost.wrap() for more info
      new_data.append(format.output())
  
  # Sort the new data by timestamp, get only the html
  new_data.sort(key=lambda x: x[1], reverse=True)
  
  # read the index file, keep the template only
  with open('index.html', 'r') as fp:
    # instantiate the post delete handler
    template = DelPost()
    # This will simply delete the posts section
    template.feed(fp.read())
  
  # Instantiate the Filler and add the new data to it
  filler = FillPost(' '.join([x[0] for x in new_data]))
  filler.feed(template.out)

  # Write the new index file
  with open('index.html', 'w') as fp:
    fp.write(filler.out)
