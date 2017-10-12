import re
cityId = '11'
flag =0 
foodpanda_locality = []
tempraroy_list1 = [tuple(range(0,1)),tuple(range(1,2)),tuple(range(2,3)),tuple(range(3,4)),tuple(range(4,5)),tuple(range(5,6)),tuple(range(0,1)),tuple(range(1,2)),tuple(range(2,3)),] 
tempraroy_list2 = [('chimpoo',),('ricky',),('shabad',),('angad',),('ricky',),('shabad',),('angad',),('humpy')]
for locality,area_id in zip(tempraroy_list2,tempraroy_list1):
	searchurl= 'http://www.foodpanda.in/restaurants?area_id=%s' % (area_id) 
	Dummytuple = (area_id,str(locality),str(cityId),searchurl,)
	for item in foodpanda_locality:
		if Dummytuple[0] == item[0]:
			flag = 1
	if flag != 1:
		foodpanda_locality.append(Dummytuple)
		flag= 0
print foodpanda_locality