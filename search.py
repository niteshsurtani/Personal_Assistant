attribute_mapping = {}
attribute_mapping['CITY'] = "city.name"
attribute_mapping['LOCALITY'] = "locality.name"
attribute_mapping['CUISINE'] = "cuisine_name"
attribute_mapping['FOOD'] = "dish.dish_name"
attribute_mapping['RESTAURANT'] = "restaurants.name"
attribute_mapping['delivery fee'] = "restaurants.delivery_charge"

def findRestaurant(dictOfValues):
	cuisine_flag = 0
	if "CUISINE" in dictOfValues.keys():
		cuisine_flag = 1
		sqlQuery = "SELECT restaurants.restaurant_id, restaurants.name FROM city, locality, restaurants, locality_restaurant, cuisine,cuisine_restaurant WHERE " \
			"locality.locality_id = locality_restaurant.locality_id " \
			"AND city.city_id = locality.city_id " \
 			"AND locality_restaurant.`restaurant_id` = restaurants.`restaurant_id` " \
			"AND cuisine.`cuisine_id` = cuisine_restaurant.`cuisine_id` " \
			"AND cuisine_restaurant.`restaurant_id` = restaurants.`restaurant_id` AND "
	else:
		sqlQuery = "SELECT restaurants.restaurant_id, restaurants.name FROM city, locality, restaurants, locality_restaurant, dish, menu WHERE " \
			"locality.locality_id = locality_restaurant.locality_id " \
 			"AND city.city_id = locality.city_id " \
 			"AND locality_restaurant.`restaurant_id` = restaurants.`restaurant_id` " \
 			"AND dish.dish_id = menu.dish_id " \
			"AND menu.`restaurant_id` = restaurants.`restaurant_id` AND "

	food_key = 0
	food_value = []

	length = len(dictOfValues)
	for key in dictOfValues:
		print key
		if key in attribute_mapping.keys():
			if length>1:
				length -= 1
				if key == "FOOD":
					food_key = 1
					food_value = dictOfValues['FOOD']
					continue
				attribute_key = attribute_mapping[key]
				if type(dictOfValues[key]) == str:
					sqlQuery += "( " + attribute_key + " = " + " ' " + str(dictOfValues[key]) + "'" + " )" + " AND "
				elif type(dictOfValues[key]) == dict:
					for key2 in dictOfValues[key]:
						if type(dictOfValues[key][key2]) == dict:
							sqlQuery += "( " + attribute_key + " BETWEEN " + str(dictOfValues[key][key2]["min"]) + " AND " + str(dictOfValues[key][key2]["max"]) + " )"+ " AND "
						elif dictOfValues[key][key2] != None:
							sqlQuery += "( " + attribute_key + " = '" + str(dictOfValues[key][key2]) +  "' )" + " AND "
				else:
					sqlQuery += "( " + attribute_key + " = '" + str(dictOfValues[key]) + "' )" + " AND "
			else:
				attribute_key = attribute_mapping[key]
				if type(dictOfValues[key]) == str:
					sqlQuery += "( " + attribute_key + " = " + "'" + str(dictOfValues[key]) + "'" + " )"
					break
				elif type(dictOfValues[key]) == dict:
					for key2 in dictOfValues[key]:
						if type(dictOfValues[key][key2]) == dict:
							sqlQuery += "( " + attribute_key + " BETWEEN " + str(dictOfValues[key][key2]["min"]) + " AND " + str(dictOfValues[key][key2]["max"]) + " )"
						elif dictOfValues[key][key2] != None:
							sqlQuery += "( " + attribute_key + " = '" + str(dictOfValues[key][key2]) +  "' )"
					break
				else:
					sqlQuery += "( " + attribute_key + " = '" + str(dictOfValues[key]) + "' )"
					break
		print sqlQuery
		
	if food_key == 1:
		food_length = len(food_value)
		count = 1
		baseSQL = sqlQuery
		for item in food_value:
			if count == 1:
				sqlQueryAdd = baseSQL + " AND ( " + attribute_mapping['FOOD'] + " = '" + str(item) + "' ) "
				count += 1
			else:
				sqlQueryAdd += " INTERSECT " + baseSQL + " AND ( " + attribute_mapping['FOOD'] + " = '" + str(item) + "' ) "
		print sqlQueryAdd

# dictOfParams = {"prize":{"exact": None,"range":{"min":45,"max":567}},"name":"Papu Pizza","url":"PPizza.com","address":"Govind Nagar","locality_id":345,"latitude":1.73,"longitude":79.412,"rating":.0002,"country_id":42,"phone":9090909090,"timings":"0400am",}
# 			# "average_cost_for_two":None,"is_pure_veg":None,"sports_bar_flag":None,"has_bar":None,"has_ac":None,"has_dine_in":None,"has_delivery":None,"takeaway_flag":None,"accepts_credit_cards":None,\
# 			# "accepts_debit_cards":None,"sheesha_flag":None,"halal_flag":None,"has_wifi":None,"has_live_music":None,"nightlife_flag":None,"stag_entry_flag":None,"entry_fee":None,\
# 			# "has_online_delivery":None,"min_order":None,"average_delivery_time":None,"delivery_charge":None,"accepts_online_payment":None}
# findRestaurant(dictOfParams) 