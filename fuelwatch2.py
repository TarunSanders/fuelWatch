#import requests
#r = requests.get('https://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS')
import feedparser
from datetime import datetime
from pprint import pprint 
#
def get_fuel(suburbAndSurrounding,day): #gets list of dictionaries with fuel info and returns this data structure
	product_id = 1; #1: unleaded
	url = 'https://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product={prod}&Suburb={sub}&Day={D}' # product = ? query strings
	url = url.format(prod = str(product_id), sub = suburbAndSurrounding, D = day) #.format is not mutable function/method
	#print(url)
	data = feedparser.parse(url) #grabs RSS data from url and converts RSS to dictionary format if not already
	return(data['entries'])

def by_price(x): # function handle for sort mutable method or sorted non-mutable function to sort prices in list of dictionaries x
	return x['price']

def createfuelHTMLTABLE(data): # creates fuel table with columns Price, Location, Brand, Address, date and highlights tomorrow's price
	header = '<thead> <tr> <th> Price (Cents) </th> <th> Location </th> <th> Brand </th> <th> Address </th> <th> Date (Y-M-D) </th></tr> </thead>' #heading format for html tables
	
	body = ''
	
	# loop creating body of table by iterating over each dictionary in list info grabbed f
	for entry in data:
		if entry['updated'] == getDate():
			body = body + '<tr> <td> {pr} </td> <td> {loc} </td> <td>{br}</td> <td>{addr}</td> <td>{dt}</td> </tr>'.format(loc = entry['location'], br = entry['brand'], pr = entry['price'],addr = entry['address'],dt = entry['updated'])
		else:
			body = body + '<tr bgcolor ="#008080"> <td> {pr} </td> <td> {loc} </td> <td>{br}</td> <td>{addr}</td> <td>{dt}</td> </tr>'.format(loc = entry['location'], br = entry['brand'], pr = entry['price'],addr = entry['address'],dt = entry['updated'])
	body = '<tbody>'+body+'</tbody>'
	legend = "Tomorrow's price (blue)"
	tableF = '<table>' + header + body + '</table>' + '<h1> Legend: </h1>'+'<p> {leg} </p>'.format(leg = legend)
	
	return tableF

def writeTable(tableDat,fileName,): #writing function for table
	with open(fileName,'w') as f:
		f.write(tableDat)	

def getDate():
	now = datetime.now()
	return str(now)[0:10]

def main():
	
	Days = ['today','tomorrow']
	Suburb = input('Choose suburb: ')
	
	fuelInfoToday = get_fuel(Suburb,Days[0])  #list of dictionaries with fuel info for today
	fuelInfoTomorrow = get_fuel(Suburb,Days[1]) #list of dictionaries with fuel info for tomorrow
	
	fuelInfo = fuelInfoToday + fuelInfoTomorrow 
	

	
	#fuelInfoToday.sort(key = by_price) #other option is to: fuelInfo = sorted(fuelInfo, key = by_price)
	#fuelInfoTomorrow.sort(key = by_price) 
	fuelInfo.sort(key = by_price)
	#pprint(fuelInfo,indent=4)
	
	#creates html table string format for info today/tomorrow
	#fuelTableToday = createfuelHTMLTABLE(fuelInfoToday) 
	#fuelTableTomorrow = createfuelHTMLTABLE(fuelInfoTomorrow)
	fuelTable = createfuelHTMLTABLE(fuelInfo)
	#writing full html string with fuel info to html file
	writeTable(fuelTable,'fuelTodayandTomorrow.html')
	#writeTable(fuelTableTomorrow,'fuelTomorrow.html')
	

main() #executing main function nested with other defined functions

