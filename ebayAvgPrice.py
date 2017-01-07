# ebay avg price script
# search page for avg price and give it to you
from bs4 import BeautifulSoup
import requests
import re
import tweepy
import os
import time
from random import randint
from time import gmtime, strftime
import math

def avgPrice(url):
	headers = {'User-agent': 'Mozilla/5.0'}
	r  = requests.get(url,headers=headers)
	data = r.text
	soup = BeautifulSoup(data,"html.parser")
	soldPrice = []
	itemNames = []
	# amntRegex = re.compile('\W[0-9]*')
	# amntRegex = re.compile('\$.(\d+).(\d+)')
	amntRegex = re.compile('((\d+).(\d+).(\d+)|(\d+).(\d+))')

	# Only check items from US + ignore "similar items" 
	count = int((soup.find_all("span",{"class":"rcnt"}))[0].text)

	# all items on page
	items = soup.find_all("ul",{"id": "ListViewInner"})
	itemPrice = items[0].find_all("span",{"class": "bold bidsold"})
	itemName = items[0].find_all("h3",{"class": "lvtitle"})

	print(count)
	for soldItems in range(0,count):
		currentPrice = (re.search(amntRegex,str(itemPrice[soldItems].text).lstrip().rstrip().strip())).group()
		soldPrice.append(float(currentPrice.replace(",","")))
		itemNames.append(str(itemName[soldItems].text).encode('utf-8').strip())
		
		# Note max of 198
		if soldItems == 198:
			break;

	# soldPrice = list(map(float, soldPrice))


	print("\nTotal items: ",count)
	print("Highest: ",max(soldPrice))
	print("Lowest: ",min(soldPrice))

	# Write sold prices to a file
	f = open('ebaySales.txt', 'w')
	for sales in range(len(itemNames)):
		f.write(str(itemNames[sales])+" : "+str(soldPrice[sales])+"\n")
	f.close()

	return (sum(soldPrice) / float(len(soldPrice)))


def main():
	# Get Input:
	print("This script will find the avg sold $ in the US\n")
	name = input("Item Name: ")
	# name.replace(" ","%20s")
	name.replace(" ","%20")
	# i.e seiko%20skx007j

	print("\nCondition\n\nNew with tags(0)\nNew without tage(1)\nNew with defects(2)")
	print("Pre-Owned(3)\nNot Specified(4)\nNew(5)\nUsed(6)")
	condition = int(input("Enter Correct Number: "))
	conditionDict = [1000,1500,1750,3000,10,3,4]

	print("Choose min/max price, or press ENTER\n")
	
	checkMinMax = 0
	try:
		minPrice = input("Min price: ")
	except:
		checkMinMax = -1
	try:
		maxPrice = input("Max price: ")
	except:
		checkMinMax = -1

	if minPrice != -1:
		minMaxString = "&_udlo="+str(minPrice)+"&_udhi="+str(maxPrice)
	else:
		minMaxString = ""
	# new is 3 used is 4 smh
	url = "http://www.ebay.com/sch/i.html?_from=R40&_sacat=0&LH_Complete=1&LH_Sold=1&LH_BIN=1&LH_ItemCondition="+str(conditionDict[condition])+"&_nkw="+name+"&_ipg=200&rt=nc&LH_PrefLoc=1&_trksid=p2045573.m1684"
	url += minMaxString
	print(url)
	price = avgPrice(url)
	print("The avg price for item is: $%.2f"%price)

main()
