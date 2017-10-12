from BeautifulSoup import BeautifulSoup
import urllib2
import os

os.environ['http_proxy']=''


url = "http://www.prokerala.com/travel/airports/india/"
page = urllib2.urlopen(url).read()

soup = BeautifulSoup(page)



tables = soup.findAll('table', {'class':'table table-condensed table-striped table-bordered'})

for table in tables:
	rows = table.findAll('tr')	
	for row in rows[2:]:
		cols = row.findAll('td')
		print str(cols[1].text) + '\t' + str(cols[4].text)
