#import requests
#r = requests.get('https://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS')
import feedparser
import operator #.add
from functools import reduce #reduce function
#from datetime import datetime
from pprint import pprint 
#

#note defaults to metro and all products for both days
def getFuelWatchURL(suburbAndSurrounding,day,product):

	# product = ? query strings
	fuelChoiceEnc = {
				'1': '1',#unleaded
				'2': '2', #premium unleaded
				'3': '4', #'diesel'
				'4': '5', #'LPG'
				'5': '11',} #branded diesel
	product_id = fuelChoiceEnc.get(str(product),'invalid')
	fuelFilterAttr = {"fueltype": product_id,
					"Day": day,
					"Suburb": suburbAndSurrounding,
					}
	URL = 'https://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Day={Day}'
	if product_id != 'invalid':
		URL += '&Product={fueltype}'
	if suburbAndSurrounding != 'metro':
		URL += '&Suburb={Suburb}'
	URL = URL.format(**fuelFilterAttr)
	print(URL)
	return URL

def get_fuel(suburbAndSurrounding,day, product): #gets list of dictionaries with fuel info and returns this data in own dictionary with imp info
	#product_id = 1 #1: unleaded
	url = getFuelWatchURL(suburbAndSurrounding,day,product)
	#print(url)
	data = feedparser.parse(url) #grabs RSS data from url and converts RSS to dictionary format if not already
	#pprint(data)
	dataImp = [ {'price': entry['price'], 
				'location': entry['location'],
				'brand':entry['brand'], 
				'date': entry['updated'],
				'address': entry['address'],
				'day': day}
			    for entry in data['entries']
			]
	
	return(dataImp)

def by_price(x): # function handle for sort mutable method or sorted non-mutable function to sort prices in list of dictionaries x
	return x['price']

def createfuelHTMLTABLE(data): # creates fuel table with columns Price, Location, Brand, Address, date and highlights tomorrow's price
	blue ="#008080" #blue = "#008080"
	white = "#FFFFFF"
	header = '''
			<thead> 
				<tr> 
					<th> Price (Cents) </th> 
					<th> Location </th> 
					<th> Brand </th> 
					<th> Address </th> 
					<th> Date (Y-M-D) </th>
				</tr> 
			</thead>
			''' #heading format for html tables
	
	# loop creating body of table by iterating over each dictionary in list info grabbed f
		
	body = ''.join(
					'''
						<tbody>
							<tr bgcolor = {col}> 
								<td> {price} </td> 
								<td> {location} </td> 
								<td> {brand} </td> 
								<td> {address} </td> 
								<td> {date} </td> 
							</tr>
						</tbody>
			'''.format(**entry,col = blue if entry['day'] == 'tomorrow' else white) #unpacking dictionary entry in data
			for entry in data
	)
	argsT = [header, body]
	tableF = '''
			<table>
				{}
				{}
			</table>
			'''.format(*argsT)
	return tableF

def writeTable(tableDat,fileName,): #writing function for table
	with open(fileName,'w') as f:
		f.write(tableDat)	

def sortedFuel(SuburbandSurrounding='metro', product = 1): #defaults to unleaded
	
	sortedfuelInfo = sorted(getFuelTodayandTomorrow(SuburbandSurrounding,product), key = by_price)

	return sortedfuelInfo

def getFuelTodayandTomorrow(SuburbandSurrounding,product):
	Days = ['today','tomorrow']
	fuelInfo = reduce(operator.add, [get_fuel(SuburbandSurrounding,entry,product) for entry in Days])
	return fuelInfo

#print(__name__) #__name__ by default is main() from command prompt otherwise if importing it is name of file fuelwatch2.py
if __name__ == '__main__':
	#suburb = input('Choose suburb: ')
	
	data = sortedFuel('cannington',2) #executing main function nested with other defined functions
	#pprint(data)
	fuelTable = createfuelHTMLTABLE(data)
	writeTable(fuelTable,'fuelPrice.html')
#feedback from Robin Chew:
# use of **dic for unpacking arguments in dictionaries and *l for unpacking arguments in lists. e.g. minus(a,b) let d = {'a': 5, 'b':2} and l = [5, 2] then minus(**d) == minus(b=2,a=5) == minus(5,2) = minus(*l) etc etc
# create own dictionary
