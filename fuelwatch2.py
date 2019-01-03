#import requests
#r = requests.get('https://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS')
import feedparser
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

def createfuelHTMLTABLE(data): # creates fuel table with columns Price, Location, Brand, Address
	header = '<thead> <tr> <th> Price </th> <th> Location </th> <th> Brand </th> <th> Address </th></tr> </thead>' #heading format for html tables
	
	body = ''
	
	# loop creating body of table by iterating over each dictionary in list info grabbed f
	for entry in data:
		body = body + '<tr> <td> {pr} </td> <td> {loc} </td> <td>{br}</td> <td>{addr}</td> </tr>'.format(loc = entry['location'], br = entry['brand'], pr = entry['price'],addr = entry['address'])
	body = '<tbody>'+body+'</tbody>'
	
	tableF = '<table>' + header + body + '</table>'
	
	return tableF

def writeTable(tableDat,fileName,): #writing function for table
	with open(fileName,'w') as f:
		f.write(tableDat)	

def main():
	Days = ['today','tomorrow']
	Suburb = input('Choose suburb: ')
	
	fuelInfoToday = get_fuel(Suburb,Days[0])  #list of dictionaries with fuel info for today
	fuelInfoTomorrow = get_fuel(Suburb,Days[1]) #list of dictionaries with fuel info for tomorrow
	
	#pprint(fuelInfoToday,indent=4)
	
	fuelInfoToday.sort(key = by_price) #other option is to: fuelInfo = sorted(fuelInfo, key = by_price)
	fuelInfoTomorrow.sort(key = by_price) 
	#pprint(fuelInfo,indent=4)
	
	#creates html table string format for info today/tomorrow
	fuelTableToday = createfuelHTMLTABLE(fuelInfoToday) 
	fuelTableTomorrow = createfuelHTMLTABLE(fuelInfoTomorrow)
	
	#writing full html string with fuel info to html file
	writeTable(fuelTableToday,'fuelToday.html')
	writeTable(fuelTableTomorrow,'fuelTomorrow.html')

main() #executing main function nested with other defined functions

