import urllib2
import os
import re
import pdfkit
from lxml.html import parse, tostring

def ptoPDF(num,pname,pmeta,problem):
    problem = re.sub('<a href="(?!https://)(.*?)">([\s\S]*?)<\/a>','<a href="https://projecteuler.net/\g<1>">\g<2></a>',problem)
    problem = re.sub('<img src="(?!https://)(.*?)"(.*?)>','<img src="https://projecteuler.net/\g<1>"\g<2>>',problem)
    [date, solves] = pmeta.split(';')[:-1]
    date = date[13:]
    solves = solves[10:]
    phtml = '<h1 style="text-align:center;">Problem '+num+': '+pname+'</h1>'
    phtml += '<h2 style="text-align:center;">Published on '+date+'</h2>'
    phtml += '<h3 style="text-align:center;"> '+solves+' solves</h2>'
    phtml += problem
    pdfkit.from_string(phtml, num+'.pdf')

def parse_url(url):
    psource = parse(urllib2.urlopen(urllib2.Request(url))).getroot().get_element_by_id('content').getchildren()
    assert len(psource)==6
    pname = psource[1].text
    pmeta = psource[2].getchildren()[0].getchildren()[0].getchildren()[1].text
    problem = tostring(psource[3])
    ptoPDF(url.split('=')[1],pname,pmeta,problem)

