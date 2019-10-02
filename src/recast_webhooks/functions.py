from flask import Blueprint, request, jsonify, session
from ..utils import Utils
from src import  app, mongo 
from recastai import Connect
from flask_wtf import  CSRFProtect

import requests, recastai, datetime, pusher, time


def get_dev_token(bot_name): 
	owner = mongo.db.users.find_one({"bot.bot-name": bot_name, "owner": None})
	if owner: 
		return owner["bot"]["dev-token"]
	return ""
	

def get_channel_slug(channel_id, dev_token): 
	channels = requests.get(Utils.CHANNEL_URL, headers={'Authorization': "Token {}".format(dev_token)}).json()
	channels = channels["results"]
	for channel in channels: 
		if channel["id"] == channel_id: 
			return channel["slug"]

	return "not-found"



def add_to_database(conv_id, memory, bot_name): 
	dev_token = get_dev_token(bot_name)
	
	conversation = requests.get(Utils.CONV_URL + conv_id, headers={'Authorization': "Token {}".format(dev_token)}).json()
	conversation = conversation["results"]
	
	channel = get_channel_slug(conversation["channel"], dev_token)
	date = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
	
	username =""
	if "person" in memory: 
		username = memory['person']['fullname']
	email = ""
	if "email-address" in memory: 
		email = memory["email-address"]["raw"]

	phone = ""
	if "phone-number" in memory: 
		phone = memory["phone-number"]["value"]

	#Adding or updating database
	if not mongo.db.conversations.find_one({"id": conv_id}): 
		print("Adding a new conversation")
		bot_id = database_add_conv_to_users(conversation, conv_id, dev_token)
		convv = {
			"id": conv_id, 
			"date": date, 
			"username": username, 
			"channel": channel, 
			"status": "OK", 
			"botmode": "ON", 
			"email": email, 
			"phone": phone, 
			"botId": bot_id
		}
		mongo.db.conversations.insert_one(convv)

	row_to_update = mongo.db.conversations.find_one({"id": conv_id})
	
	row_to_update["date"] = date

	if row_to_update["username"] == "":
		row_to_update["username"] = username
	if row_to_update["email"] == "":
		row_to_update["email"] = email
	if row_to_update["phone"] == "":
		row_to_update["phone"] = phone

	mongo.db.conversations.replace_one({'id': conv_id}, row_to_update)	

	print("Conversation of id " + conv_id + " updated!")

		
	return 1




def database_add_conv_to_users(conversation, conv_id, dev_token):

	
	connector = conversation["connector"] 

	connector_info = requests.get(Utils.CONNECTOR_URL + connector, headers={'Authorization': "Token {}".format(dev_token)}).json()

	bot_id = connector_info["results"]["botId"]

	mongo.db.users.update_one({"bot.botId":bot_id, 'owner': None} , {"$push": {'conversations': { 'id' : conv_id}}})
	users = mongo.db.users.find({'bot.botId': bot_id, 'owner': None })
	print('added conv to user')

	return bot_id






