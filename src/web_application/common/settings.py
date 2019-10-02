from flask import session
from src import mongo
from ..common.groups import get_convs_from_groups
from werkzeug.security import generate_password_hash, check_password_hash

def get_managers_list(): 

	current_user = session['username']
	user = mongo.db.users.find_one({"username": current_user})
	print(user)

	managers_list = []
	if 'managers' in user:
		for manager in user['managers']: 
			managers_list.append(manager['username'])
	return managers_list



def create_manager_user(username, pwd, all, groups): 

	conv_ids = []
	current_user = session['username']
	user = mongo.db.users.find_one({"username": current_user})

	if all: 

		conv_ids = user["conversations"]

	else: 
		conv_set = get_convs_from_groups(groups)
		for cid in conv_set: 
			conv_ids.append({"id": cid})

	hashed_password = generate_password_hash(pwd, method='sha256')


	user = {
		'username': username, 
		'account': {'password': hashed_password}, 
		'bot': user['bot'], 
		'owner': current_user, 
		'conversations': conv_ids, 
		'groups': []
	}

	mongo.db.users.update({'username': current_user}, {'$push': {'managers': {'username': username}}})

	mongo.db.users.insert_one(user)



def change_bot_info(bot_name, req_token, dev_token): 
	current_user = session["username"]
	mongo.db.users.update({'username': current_user}, {'$set': {'bot': {'bot-name': bot_name, 'req-token': req_token, 'dev-token': dev_token}}})

