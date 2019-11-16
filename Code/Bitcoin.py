import requests, json, conf, time

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

"""Driver function"""
if __name__=="__main__":
	while True:
			# Getting current Bitcoin price
		bitcoin_price = int(get_bitcoin_price())
			# Creating the message to be sent
		message = "Bitcoin price has crossed threshold limits! Current price is at INR "+ str(bitcoin_price)
			# Sending alerts if price crosses threshold limits
		try:
			if(bitcoin_price <= 600000 or bitcoin_price >= 615000):
				send_telegram_message(message)
				break
		except Exception as e:
			print("\n\t Something went wrong! [Details below]")
			print(e)
			# Delaying for 10 seconds
		time.sleep(10)		