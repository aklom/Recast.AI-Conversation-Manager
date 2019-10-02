from flask import render_template, session, Blueprint, request, redirect, jsonify
import requests
from ..common.session import session_required
from src import mongo
from werkzeug.security import generate_password_hash, check_password_hash


auth_bp = Blueprint('auth', __name__, template_folder='./templates', static_folder="./css", static_url_path='/web_application/static')

""" Render signup page """
@auth_bp.route('/register')
def register(): 
	return render_template('register.html')

""" Submit signup form """
@auth_bp.route('/signup', methods=['POST'])
def signup(): 

	fname = request.form.get("first-name")
	lname = request.form.get("last-name")
	
	username = request.form.get("username")
	password = request.form.get("password")
	password2 = request.form.get("password2")

	botname = request.form.get("bot-name")
	req_token = request.form.get("req-token")
	dev_token = request.form.get("dev-token")

	users = mongo.db.users.find()
	bot_content = requests.get("https://api.cai.tools.sap/core/v1/users/{}/bots/{}".format(username, botname),
		headers={'Authorization': "Token {}".format(dev_token)}
		).json()
	bot_id = ""
	if bot_content and bot_content["results"]:
		bot_id = bot_content["results"]["id"]

	for user in users: 
		if user['username'] == username: 
			return jsonify({'message': 'Username already exists'})

	if password2 != password: 
		return jsonify({'message': 'Wrong passwords'})

	
	hashed_password = generate_password_hash(password, method='sha256')
	
	account = {
		'password': hashed_password, 
		'first-name': fname,
		'last-name': lname
	}

	bot = {
		'bot-name': botname, 
		'dev-token': dev_token, 
		'req-token': req_token, 
		'botId': bot_id
	}

	user = {
		'username': username,
		'account': account,
		'bot': bot,
		'owner': None, 
		'conversations': []
	}

	mongo.db.users.insert_one(user)

	return redirect('/login')



""" Render login page """ 
@auth_bp.route('/login', methods=['GET'])
def login(): 
	return render_template('login.html')


""" Submit login form """ 
@auth_bp.route('/signin', methods=['POST'])
def signin():

	username = request.form.get("name")
	password = request.form.get("password")

	user = mongo.db.users.find_one({'username': "{}".format(username)})

	if not user: 
		return jsonify({'message': 'User not found'})

	account = user['account']

	if check_password_hash(account['password'], password):
		session['username'] = username
		session['devToken'] = user["bot"]["dev-token"]
		session['reqToken'] = user['bot']['req-token']
		if user['owner'] == None: 
			session['owner'] = 1
		else: 
			session['owner'] = 0
		return redirect('/inbox')

	return jsonify({'message': 'Wrong password'})


""" Log out user """ 
@auth_bp.route('/logout', methods=['POST'])
@session_required
def logout(current_user): 
	session.pop('username', None)
	session.pop('botId', None)
	session.pop('owner', None)
	session.pop('devToken', None)
	session.pop('reqToken', None)

	return redirect('/login')

