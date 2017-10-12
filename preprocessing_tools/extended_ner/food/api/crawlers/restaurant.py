from bs4 import BeautifulSoup
import socket
import requests
from re import sub
from re import search
from ErrorHandler import typec
# from locality import find_foodpanda_valid_locality,find_locality


def find_all_restaurants(loca,cityId):
	try:
		restaurants = []
		searchurl = "https://www.foodpanda.in/location-suggestions?cityId=%s&area=%s" % (cityId,loca[1])
		f = requests.get(searchurl)
		html = f.text
		soup = BeautifulSoup(html)
		# data = BeautifulSoup(str(soup.find_all("div",{'class':'vendor__title'})))
		data = BeautifulSoup(typec(soup.find_all("div",{'class':'vendor__title'}), 'string', 'string'))
		for link in data.find_all("a"):
			uniqueId = search('/restaurant/(.+?)">', typec(link,'string','string')).group(1)
			restaurants.append((typec(uniqueId,'string','string'),))
		print restaurants
		return restaurants
	except:
		print "Error in find_all_restaurants"
		print "Loca"
		print loca
		print "cityId"
		print cityId

def restaurant_info(restaurantsData,count):
	try:
		searchurl = "https://www.foodpanda.in/restaurant/%s" % (restaurantsData[0])
		f = requests.get(searchurl)
		html = f.text
		soup = BeautifulSoup(html)
		restaurantsData += (typec(sub("(?m)^\s+","",sub(r"[^\x00-\x7F]+","",(soup.find('h1',{"itemprop":"name"}).text))),'string','string').rstrip('\n'),)
		restaurantsData += (typec(sub(r"[^\x00-\x7F]+","",(soup.find('address').text)),'string','string').lstrip('\n'),)
		restaurantsData += (typec((soup.find('i',{'class':'stars'}))['content'],'string','float'),)
		details = sub("(?m)^\s+","",typec(soup.find('ul',{'class':'cart__empty__elements'}).text,'string','string')).split('\n')
		deliveryFee = None
		deliveryTime = None
		paymentOption = None
		deliveryMinAmount = None
		Voucher = False
		pickupTime = None
		for index,item in enumerate(details):
			if(item == 'Delivery time:'):
				deliveryTime = details[index+1]
			elif(item == 'Online payment available'):
				paymentOption = True
			elif(item == 'Delivery fee'):
				deliveryFee = typec(sub(",","",sub("Rs.","",details[index+1])),'string','float')
			elif(item == 'Delivery min.:'):			
				deliveryMinAmount = typec(sub(",","",sub("Rs.","",details[index+1])),'string','float')
			elif(item == 'Accepts Vouchers'):
				Voucher = True
		if(soup.find("dt",{"class":"vendor-pickup-time"}) != None ):
			soup2 = BeautifulSoup(typec(soup.find("dt",{"class":"vendor-pickup-time"}).findNext("dd"),'string','string'))
			data = soup2.find("dd").text
			pickupTime = (sub("(?m)^\s+","",typec(data,'string','string')).split("\n")).pop(0)
		restaurantsData += (deliveryFee,deliveryTime,pickupTime,deliveryMinAmount,paymentOption,Voucher,searchurl,)
		
		#Extracing Food data for the Restaurant
		foodData = []
		print count
		soup = BeautifulSoup(html)
		
		#To store food data Temporarily
		string =''
		for data in soup.find_all('div',{'class':'menu-item__content-wrapper'}):
			# soup2 = BeautifulSoup(str(data))
			soup2 = BeautifulSoup(typec(data, 'string', 'string'))
			dish_name = soup2.find('div', {'class': 'menu-item__title'}).text
			for val in soup2.find_all('article', {'class': 'menu-item__variation'}):
				string += (sub("(?m)^\s+","",dish_name))
				string += (sub("(?m)^\s+","",val.text))
		string = string.strip().split('\n')
		for index,item in enumerate(string):
			if item == u'\xa0':
				string.pop(index)
			# print string
		foodtuple = ()
		itemCount = 0 
		foodtuple += (count,restaurantsData[0],)	
		for index,item in enumerate(string):
			if item == 'Add':
				itemCount = 0
				foodData.append(foodtuple+ (searchurl,))
				count += 1
				foodtuple = ()
				foodtuple += (count,restaurantsData[0],)			 
			else:
				item = item.replace(unichr(160),'')
				if "Rs." in typec((sub(r"[^\x00-\x7F]+","",item)),'string','string') and itemCount%2 == 1:
					item = sub("Rs.","",typec((sub(r"[^\x00-\x7F]+","",item)),'string','string'))
					item = sub(",","",typec(item,'string','string'))
					foodtuple += ('None',typec(item,'string','float'),)
					itemCount += 1
				elif "Rs." in typec((sub(r"[^\x00-\x7F]+","",item)),'string','string'):
					item = sub("Rs.","",typec((sub(r"[^\x00-\x7F]+","",item)),'string','string'))
					item = sub(",","",typec(item,'string','string'))
					foodtuple += (typec(item,'string','float'),)
				else:
					foodtuple += (typec((sub(r"[^\x00-\x7F]+","",item)),'string','string'),)
					itemCount += 1


		cuisineData = []
		soup = BeautifulSoup(html)
		for cuisines in (soup.find_all("li",{"itemprop" : "servesCuisine"})):
			cuisineData.append((restaurantsData[0],typec(cuisines.text,'string','string'),))
		return (restaurantsData,foodData,cuisineData)
	except:
		print "Error In restaurant_info"
		print "restaurantsData"
		print restaurantsData
		print "count"
		print count