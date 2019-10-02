from flask import session
from src import mongo
from datetime import datetime
import requests
from ...utils import Utils


def get_conversations_list():
	
	current_user = session['username'] 
	user = mongo.db.users.find_one({'username': current_user})
	
	conversation_ids = user['conversations']
	
	conversations = []
	for conv_id in conversation_ids: 
		conv = mongo.db.conversations.find_one({'id': conv_id["id"]})
		conversations.append(conv)
	
	conversations.sort(key=lambda r: datetime.strptime(r['date'], "%I:%M%p on %B %d, %Y"), reverse=True)
	
	return conversations


def delete_conversation_from_database(cid_del): 
	current_user = session['username'] 
	mongo.db.users.update({"username": current_user}, {"$pull": {'conversations': { 'id' : cid_del}}})

	print("Conversation of id " + cid_del + " deleted!")
		

def get_conversation_content(cid): 
	conversation = []
	url = Utils.CONV_URL + cid
	if cid == "":
		print("cid missing!")
		return {}
	conv = requests.get(url, headers={'Authorization': "Token {}".format(session["devToken"])}).json()
	if(conv["results"] != None): 
		participants = conv["results"]["participants"]

		for participant in participants:
			if(participant['isBot'] == False):
				human_id = participant['id']
			else: 
				bot_id = participant['id']

		messages = conv["results"]["messages"]
		for message in messages: 
			if message['participant'] == human_id: 
				conversation.append({'isBot': False, 'content': "{}".format(message['attachment']['content'])})
			elif message['participant'] == bot_id: 
				conversation.append({'isBot': True, 'content': "{}".format(message['attachment']['content'])})
	return conversation