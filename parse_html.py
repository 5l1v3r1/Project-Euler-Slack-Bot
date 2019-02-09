import urllib2
import requests
from BeautifulSoup import BeautifulSoup 
from lxml.html import parse, tostring

def parse_url(url):
	a = parse(urllib2.urlopen(urllib2.Request(url))).getroot()
	psource = a.get_element_by_id("content")
	assert len(psource.getchildren())==6
	pname = psource.getchildren()[1].text
	pmeta = psource.getchildren()[2].getchildren()[0].getchildren()[0].getchildren()[1].text
	problem = psource.getchildren()[3]
	return tostring(problem)

def get_challenge_name(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.content)
	return soup.findAll('h2')[0].string
