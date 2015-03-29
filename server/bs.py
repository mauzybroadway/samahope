import sys
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
from pymongo import MongoClient
import json

client = MongoClient()
db = client.samahope

BASE_URL="http://www.samahope.org"

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.recording = 0
        self.data = ''

    def handle_starttag(self, tag, attrs):
        self.recording = 1
        self.data = ''

    def handle_endtag(self, tag):
        self.recording = 0

    def handle_data(self, dat):
        if self.recording:
            self.data = dat.lstrip().rstrip()
        else:
            return

class Doctor():
    def __init__(self):
        self.dollars_sofar = None
        self.dollars_needed = None
        self.name = None
        self.bold_desc = None
        self.description = None
        self.treatment_focus = None
        self.treatment_description = None
        self.treatment_cost = None
        self.location = None
        self.donate_link = None
        self.learn_more_link = None
        self.badge_title = None
        self.badge_url = None

parser = MyHTMLParser();

docfilename = "doctors"
docfile = open(docfilename)
soup = BeautifulSoup(docfile.read(),"html.parser")

doctors = soup.findAll("section", { "class" : "doctor-tile" })

whos = []
i = 0

for doc in doctors:

    #who = Doctor()

    who={}

    print "---------- DOCTOR ---------"

    who['dollars_sofar'] = doc.find("div",{"class":"progress-bar"})["title"]

    elmt = doc.find("div",{"class":"progress-bar_helper"}).span
    parser.feed(elmt.prettify(formatter = "minimal"))
    who['dollars_needed'] = parser.data

    elmt = doc.find("h1",{"class":"entry-title"})
    parser.feed(elmt.prettify(formatter = "minimal"))
    who['name'] = parser.data


    info = doc.find("section",{"class":None})
    p = info.findAll("p")
    if len(p) >= 1:
        parser.feed(p[0].prettify(formatter = "minimal"))
        who['bold_desc'] = parser.data
    if len(p) >= 2: 
        parser.feed(p[1].prettify(formatter = "minimal"))
        who['description'] = parser.data

    elmt = doc.find("img",{"class" : "badge"})["src"]
    badge_url = ''
    badge_url += BASE_URL
    badge_url += elmt
    who['badge_url'] = badge_url
    #sys.stdout.write("%s%s\n" % (BASE_URL,elmt))
    

    elmt = doc.find("div",{"class" : "treatment_description"})
    parser.feed(elmt.h3.prettify(formatter = 'minimal'))
    who['treatment_focus'] = parser.data
    parser.feed(elmt.p.prettify(formatter = 'minimal'))
    who['treatment_description'] = parser.data
    
    elmt = doc.find("ul",{"class" : "treatment-cost"})
    if elmt:
        who['treatment_cost'] = []
        for li in elmt.findAll("li"):
            parser.feed(li.prettify(formatter = 'minimal'))
            who['treatment_cost'].append(parser.data)

    
    elmt = doc.find("div",{"class":"doctor-tile_location"}).span
    parser.feed(elmt.prettify(formatter = "minimal"))
    who['location'] = parser.data

    elmt = doc.find("div",{"class":"doc-pic_learn-more"})
    who['donate_link'] = elmt.find("a",{"class":"primary"})["href"]
    who['learn_more_link'] =elmt.find("a",{"class":"learn-more-link"})["href"]

    db.doctors.update(
        { 'name': who['name']},
        who,
        upsert=True
    )
    
    #whos.append(who)    

for who in whos:
    print json.dumps(vars(who),sort_keys=True, indent=4)
