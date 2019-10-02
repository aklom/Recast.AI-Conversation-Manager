from flask import Blueprint, request, jsonify, session
from ..utils import Utils
from src import app, mongo, pusher_client
from recastai import Connect
from flask_wtf import  CSRFProtect
from flask_pymongo import PyMongo
from .functions import add_to_database, get_dev_token

import requests, recastai, datetime, time



apimod = Blueprint('api', __name__)


def reload_pages():

	pusher_client.trigger('inspect-channel', 'new-message', {'message': 'hello world'})
	pusher_client.trigger('index-channel', 'conversation-updated', {'message': 'hello world'})


@apimod.route('/update', methods= ['POST'])
def update():
	requestjson = request.json
	bot_name = request.headers["Bot-name"]
	conversation_id = requestjson['conversation']['id']
	memory = requestjson['conversation']['memory']
	add_to_database(conversation_id, memory, bot_name)

	reload_pages()

	return jsonify(status=200)
 


@apimod.route('/fallback', methods= ['POST'])
def fallback(): 
	#### add status column to database
	# if unanswered -> status = PROBLEM and send notification
	conv_id = request.get_json()["conversation"]["id"]
	source = request.get_json()["nlp"]["source"]
	conv = mongo.db.conversations.find_one({'id': conv_id})
	#updating database to add fallback status
	if conv: 
		mongo.db.conversations.update_one({'id': conv_id}, {"$set": {'status': "FALLBACK"}})
	
		print("Conversation of id" + conv_id + " updated! ----> Fallback")

		if conv["botmode"] == "ON": 
			if source != "FALLBACK":
				requests.post(Utils.CONV_URL + conv_id + '/messages', 
				json={'messages': [{'type': 'text', 'content': "Sorry, I don't understand."}]},
				headers={'Authorization': "Token {}".format(get_dev_token(request.headers["Bot-name"]))})
				
				print("Sorry message sent")


				reload_pages()
		else: 
			print("No answer ---> Bot mode is off ! ")
	
	
	return jsonify(status=200)

