from flask import Blueprint, render_template, redirect, request, session
from ..common.groups import get_groups_list
from ..common.settings import get_managers_list, create_manager_user, change_bot_info
from ..common.session import session_required
from src import mongo

settings_bp = Blueprint('settings', __name__, template_folder='./templates', static_folder="./css", static_url_path='/web_application/static')


""" Render settings page """
@settings_bp.route('/settings')
@session_required
def settings(current_user): 
	

	if session['owner'] == 1: 
		groups = get_groups_list()
		managers = get_managers_list()
		bot = mongo.db.users.find_one({'username': session['username']})["bot"]
		return render_template('settings.html', groups=groups, managers=managers, owner=session['owner'], bot_name= bot["bot-name"], dev_token=bot["dev-token"], req_token=bot["req-token"])
	else: 
		return render_template('settings-manager.html', owner=session['owner'])



""" Add a manager """ 
@settings_bp.route('/addmanager', methods=['POST'])
@session_required
def addmanager(current_user): 

	username_manager = request.form.get("manager-name")
	password_manager = request.form.get("manager-pwd")
	all_users = request.form.get("all")
	groups = request.form.getlist("groups")

	create_manager_user(username_manager, password_manager, all_users, groups)
	
	return redirect('/settings')


@settings_bp.route('/savetokenchanges', methods=['POST'])
@session_required
def savetokenchanges(current_user): 

	bot_name = request.form.get("name")
	req_token = request.form.get("reqToken")
	dev_token = request.form.get("devToken")


	change_bot_info(bot_name, req_token, dev_token)

	return redirect('/settings')