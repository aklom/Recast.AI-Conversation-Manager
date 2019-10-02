import requests
from flask import render_template, session, Blueprint, request, redirect
from ..common.session import session_required
from src.web_application.common.conversations import get_conversations_list, delete_conversation_from_database, get_conversation_content
from src import mongo
from ...utils import Utils

inbox_bp = Blueprint('inbox', __name__, template_folder='./templates', static_folder="./css", static_url_path='/web_application/static')


""" Render Inbox page """
@inbox_bp.route('/inbox')
@session_required
def manage_conversations(current_user):
	bot_name = mongo.db.users.find_one({'username': session['username']})["bot"]["bot-name"]
	conv_list = get_conversations_list()
	latest_message_date = "No messages received"
	if len(conv_list): 
		latest_message_date = conv_list[0]['date']
	return render_template('inbox.html', conversations=conv_list, owner=session['owner'], latest_message=latest_message_date, bot_name= bot_name)
    


""" Delete a conversation """
@inbox_bp.route('/delete', methods=['POST'])
@session_required
def delete_conversation(current_user):
    cid_del = request.form.get('conversation_id')
    delete_conversation_from_database(cid_del)
    return redirect('/inbox')
    


""" Render inspector page of a conversation """
@inbox_bp.route('/inspect/<conversation_id>', methods=['POST', 'GET'])
@session_required
def inspect_conversation(current_user, conversation_id): 
	user = mongo.db.users.find_one({'username': session['username']})
	if {"id": conversation_id} not in user['conversations']:
		return redirect('/inbox')
	else:
		conversation = get_conversation_content(conversation_id)
		conv_params = mongo.db.conversations.find_one({'id': conversation_id})
		
		return render_template('inspect.html', conversation=conversation, conversation_params= conv_params, owner=session['owner'])


""" Send a message """
@inbox_bp.route('/send_message/<conversation_id>', methods=['POST', 'GET'])
@session_required
def send_message(current_user, conversation_id): 
	if request.method == 'POST': 
		
		message_to_send = request.form.get("message_to_send")
		
		requests.post(
			Utils.CONV_URL + conversation_id + '/messages', 
			json={'messages': [{'type': 'text', 'content': "{}".format(message_to_send)}]},
			headers={'Authorization': "Token {}".format(session["devToken"])}
		)
		return redirect('/inspect/' + conversation_id)
	
	else: 
		return redirect('/inbox')


""" Set bot mode """
@inbox_bp.route('/setbotmode/<conversation_id>', methods= ['POST', 'GET'])
@session_required
def setbotmode(current_user, conversation_id): 

	print(conversation_id)

	botmode = request.form.get("bot_mode")
	
	if(botmode == "ON"):
		params = {
			'message': {'type': 'text', 'content': 'FALLBACK'}, 
			'conversation_id': conversation_id, 
			'memory': {'bot-mode': 'on', }
		}
		mongo.db.conversations.update_one(
			{'id': conversation_id}, 
			{ "$set": { "botmode": "ON" } }
		)
		
	else: 
		params = {
			'message': {'type': 'text', 'content': 'FALLBACK'}, 
			'conversation_id': conversation_id, 
			'memory': {'bot-mode': 'off'}
		}
		mongo.db.conversations.update_one(
			{'id': conversation_id}, 
			{ "$set": { "botmode": "OFF" } }
		)

	requests.post(
		'https://api.recast.ai/build/v1/dialog', 
		json=params, 
		headers={'Authorization': "Token {}".format(session["devToken"])})

	return redirect('/inspect/' + conversation_id)


