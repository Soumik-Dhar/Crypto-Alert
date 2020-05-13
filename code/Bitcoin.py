import requests, json, conf, time, math, statistics
data=[]

"""Getting current Bitcoin price in INR"""
def get_bitcoin_price():
	try:
			# API url to GET Bitcoin price from
		URL = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=INR"
		response = requests.request("GET", URL)
		response = json.loads(response.text)
			# Getting current price from INR field
		current_price = response["INR"]
		return current_price
	except Exception as e:
			# Displaying error details
		print("\n\t Something went wrong while getting Bitcoin price! [Details below]")
		print(e)	
		return False

"""Sending alerts via telegram"""
def send_telegram_message(message):
		# Building bot URL
	URL = "https://api.telegram.org/" + conf.BOT_ID + "/sendMessage"
		# Building channel data
	data = {
		"chat_id": conf.CHAT_ID,
		"text": message
	}
	try:
		response = requests.request(
			"GET",
			URL,
			params=data
		)
			# Displaying request status
		print("\n\t The Telegram response is as follows : \n",response.text)
		telegram_data = json.loads(response.text)
		return telegram_data["ok"]
	except Exception as e:
			# Displaying error details
		print("\n\t Something went wrong while sending alerts via Telegram! [Details below]")
		print(e)
		return False

"""Computing the upper and lower bounds of BTC prices using Z-score analysis"""
def computeBounds(data,frameSize,factor):
	if(len(data)<frameSize):
		return None
	if(len(data)>frameSize):
		del data[0:(len(data)-frameSize)]
		# Getting the mean
	mn=statistics.mean(data)
		# Getting the variance
	var=0
	for d in data:
		var+=math.pow((d-mn),2)
		# Computing Z-Score
	zn=factor*math.sqrt(var/frameSize)
		# Finding upper and lower bounds
	upperBound=data[frameSize-1]+zn
	lowerBound=data[frameSize-1]-zn
	return([upperBound,lowerBound])

"""Driver function"""
if __name__=="__main__":

	while True:
			# Getting current Bitcoin price
		bitcoin_price = int(get_bitcoin_price())
			# Computing Z-Score from bitcoin INR prices
		bound=computeBounds(data,conf.FRAME_SIZE,conf.MUL_FACTOR)
		if not bound:
			data_count=conf.FRAME_SIZE-len(data)
				# Creating the message to be sent to Telegram
			message="""\n\t Not enough data to compute Z-score. \n\t Need """ + str(data_count) + """ more data points. 
					\n\t Current Bitcoin price is INR """+ str(bitcoin_price)
			print(message)
			send_telegram_message(message)
				# Adding bitcoin prices to the list
			data.append(bitcoin_price)
			time.sleep(10)
			continue
			# Sending alerts if price suddenly crosses threshold limits
		try:
			if(bitcoin_price>bound[0]):
				message="\n\t ALERT! Current Bitcoin price [INR "+ str(bitcoin_price) +"] has crossed upper threshold limits!" 
				print(message)
				send_telegram_message(message)
				break
			elif(bitcoin_price<bound[1]):
				message="\n\t ALERT! Current Bitcoin price [INR "+ str(bitcoin_price) +"] has crossed lower threshold limits!" 
				print(message)
				send_telegram_message(message)
				break
		except Exception as e:
				# Displaying error details
		 	print("\n\t Something went wrong! [Details below]")
		 	print(e)
			# Delaying for 10 seconds
		time.sleep(10)		