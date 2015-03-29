from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print "START:", tag
    def handle_endtag(self, tag):
        print "END  :", tag
    def handle_data(self, data):
        print "DATA :",data.lstrip()

parser = MyHTMLParser()
#parser.feed('<html><head><title>Test</title></head>'
#            '<body><h1>Parse me!</h1></body></html>')

docfilename = "doctors"
#docfile = open(docfilename, 'r')

for line in open(docfilename).readlines():
    line = line.rstrip('\n')
    parser.feed(line)

