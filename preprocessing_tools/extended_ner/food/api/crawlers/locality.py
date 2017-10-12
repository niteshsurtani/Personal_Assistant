from bs4 import BeautifulSoup
import socket
import requests
from re import sub,search
from ErrorHandler import typec


def find_locality(cityName):
	try:
		searchurl = "http://www.commonfloor.com/localities/index/city/%s" % (cityName)
		f = requests.get(searchurl)
		html = f.text
		soup = BeautifulSoup(html)
		localities=[]
		data = soup.find('tbody')
		data= typec(sub("(?m)^\s+", "", typec(data.text,'string','string')),'string','string')
		data = data.split('\n')
		for item in data:
			if item.isalpha():
				localities.append(item)
		print localities
		return localities
	except:
		print "Error find_locality"
		print cityName
def find_foodpanda_valid_locality(cityId,localities):
	try:
		foodpanda_locality = []
		locality_id = []
		#To temporarily store  Area_idies 
		tempraroy_list1 = [] 
		#To temporarily store  Name of the localities
		tempraroy_list2 = []
		count = 1
		flag = 0
		for loca in localities:
			print count
			print len(foodpanda_locality)
			print len(locality_id)
			print locality_id
			print loca
			print cityId
			count +=1

			#getting html from the Search Url
			searchurl = "https://www.foodpanda.in/location-suggestions?cityId=%s&area=%s" % (cityId,loca)
			f = requests.get(searchurl)
			html = f.text
			soup = BeautifulSoup(html)

			#checking if the the page of Suggestions of localities is opened or 
			#the request has been redirected to the page of specific locality
			if(soup.find('h1',{'class':'h2'})):
				heading = sub(":","",soup.find('h1',{'class':'h2'}).text)
				heading = heading.strip()
				if heading=="Suggestions":		

					#Extracting Area_idies of the localities
					tempraroy_list1[:] = []
					for data in soup.find_all('a',{'class':'list-group-item'}):
						tempraroy_list1.append(search('area_id=(.+?)">', typec(data,'string','string')).group(1))
					
					#Appendng unique area_id in locality_id list 
					for area_id in tempraroy_list1:
						if area_id not in locality_id:
							locality_id.append(area_id)
					
					#Extracting Name of the Localities
					tempraroy_list2[:] = []
					for data in soup.find_all('div',{'class':'content-block location-suggestions'}):
						tempraroy_list2= sub("(?m)^\s+","",data.text).split('\n')
					tempraroy_list2.pop(0) 												# poping "Suggestion" string
					tempraroy_list2.pop(len(tempraroy_list2)-1)				 			# poping whitespace
					
					#Appending Uniquely Localities Full Data in the foodpanda_locality
					for locality,area_id in zip(tempraroy_list2,tempraroy_list1):
						searchurl= 'http://www.foodpanda.in/restaurants?area_id=%s' % (area_id) 
						Dummytuple =  (area_id,typec((locality).replace(unichr(8226),''),'string','string'),typec(cityId,'string','string'),searchurl,)
						for item in foodpanda_locality:
	 						if Dummytuple[0] == item[0]:						
								flag = 1 
						if flag != 1 :
							foodpanda_locality.append(Dummytuple)
						flag = 0
					
			else:

				#Appending the locality that is already a valid name for foodpanda
				data = soup.find('meta',{'property':'og:url'})
				area_id = search('area_id=(.+?)"',typec(data,'string','string')).group(1)

				#Appendng unique area_id in locality_id list 
				if area_id not in locality_id:
					locality_id.append(area_id)
				searchurl= 'http://www.foodpanda.in/restaurants?area_id=%s' % (area_id) 
				Dummytuple =  (area_id,typec((loca).replace(unichr(8226),''),'string','string'),typec(cityId,'string','string'),searchurl,)
				for item in foodpanda_locality:
					if Dummytuple[0] == item[0]:						
						flag = 1
				if flag != 1 :			
					foodpanda_locality.append(Dummytuple)
				flag = 0

		if None in locality_id:	
			locality_id.pop(locality_id.index(None))
		return (foodpanda_locality,locality_id)
	except:
		print "Error in locality"
		print "city Id"
		print cityId
		print "localities"
		print localities
