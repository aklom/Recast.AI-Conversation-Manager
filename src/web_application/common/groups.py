from flask import session
from src import mongo
from ...utils import Utils
import requests

def get_groups_list():
    
	current_user = session['username'] 
	groups = mongo.db.groups.find({'username': current_user})

	groups_list = []
	
	for group in groups:
		groups_list.append({
			'name': "{}".format(group["name"]),
			 'id': "{}".format(group["id"])
		})

	return groups_list



def get_convs_from_groups(groups): 
	participants_set = set()
	
	for group in groups: 
		group_db = mongo.db.groups.find_one({'id': str(group)})
		participants = group_db["conversations"]
		for participant in participants:
			participants_set.add(participant)

	return participants_set


def send_to_all_users(message):
    
	current_user = session['username'] 
	user = mongo.db.users.find_one({'username': current_user})

	conversation_ids = user["conversations"]
	
	for conversation_id in conversation_ids: 
		requests.post(
			Utils.CONV_URL + conversation_id['id'] + '/messages', 
			json={'messages': [{'type': 'text', 'content': "{}".format(message)}]},
			headers={'Authorization': "Token {}".format(session["devToken"])}
		)

def send_to_groups(groups, message): 

	participants_set =  get_convs_from_groups(groups)
	
	for participant in participants_set: 
		requests.post(
			Utils.CONV_URL + participant + '/messages', 
			json={'messages': [{'type': 'text', 'content': "{}".format(message)}]},
			headers={'Authorization': "Token {}".format(session["devToken"])}
		)

