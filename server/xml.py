import sys
from HTMLParser import HTMLParser
from xml.etree import cElementTree as etree

class LinksParser(HTMLParser):
  def __init__(self):
      HTMLParser.__init__(self)
      self.tb = etree.TreeBuilder()

  def handle_starttag(self, tag, attributes):
      self.tb.start(tag, dict(attributes))

  def handle_endtag(self, tag):
      self.tb.end(tag)

  def handle_data(self, data):
      self.tb.data(data)

  def close(self):
      HTMLParser.close(self)
      return self.tb.close()

parser = LinksParser()
for line in open(docfilename).readlines():
    line = line.rstrip('\n')
    parser.feed(line)
root = parser.close()
span = root.find(".//span[@itemprop='description']")
etree.ElementTree(span).write(sys.stdout)

docfilename = "doctors"


print parser.data
