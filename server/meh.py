from HTMLParser import HTMLParser

class LinksParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.recording = 0
    self.data = ''

  def handle_starttag(self, tag, attributes):
    if tag != 'section':
      return
    if self.recording:
      self.recording += 1
      return
    for name, value in attributes:
      if name == 'class':
        for val in value.split():
          if val == "doctor-tile":
            self.data +=  "------------- DOCTOR ---------------\n"
            break
      else:
        return
    self.recording = 1

  def handle_endtag(self, tag):
    if tag == 'section' and self.recording:
      self.recording -= 1

  def handle_data(self, data):
    data = data.lstrip().rstrip()
    if self.recording and data != "":
      self.data += "%s\n"  % data

parser = LinksParser()
docfilename = "doctors"

for line in open(docfilename).readlines():
    line = line.rstrip('\n')
    parser.feed(line)

print parser.data
