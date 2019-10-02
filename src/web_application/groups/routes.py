from ..common.session import session_required
from ..common.groups import get_groups_list, send_to_groups, send_to_all_users
from ..common.conversations import get_conversations_list
from src import mongo
from flask import Blueprint, render_template, session, request, redirect

groups_bp = Blueprint('groups', __name__, template_folder='./templates', static_folder="./css", static_url_path='/web_application/static')


""" Render groups page """ 
@groups_bp.route('/groups', methods=['POST', 'GET'])
@session_required
def groups(current_user): 
	
	groups_list = get_groups_list()
	
	return render_template('groups.html', groups=groups_list, owner=session['owner'])


""" Render group creation page """ 
@groups_bp.route('/creategroup', methods=['POST', 'GET'])
@session_required
def create_group(current_user): 
	
	conv_list = get_conversations_list()
	
	if request.method == 'POST': 
		""" Create the group """
		group = {
			"id": str(mongo.db.groups.count() + 1),
			"name": request.form.get("name"),
			"description": request.form.get("description"),
			"conversations": request.form.getlist("conv"),
			"username": current_user
		}
		mongo.db.groups.insert_one(group)

		return redirect('/groups')
	
	else: 
		""" display """ 
		return render_template('creategroup.html', conversations=conv_list, owner=session['owner'])


""" Render Group edition page """
@groups_bp.route('/editgroup', methods=['POST', 'GET'])
@session_required
def editgroup(current_user): 
	conv_list = get_conversations_list()

	group_id = request.form.get("group_id") 
	print("Editing group :" + group_id)

	group = mongo.db.groups.find_one({'id': group_id})

	if request.method == 'POST': 
		
		name = group["name"]
		desc = group["description"]
		participants = group["conversations"]

		return render_template('editgroup.html', group_id=group_id, name=name, description=desc, participants=participants, conversations=conv_list, owner=session['owner'])


""" Save changes of a group edition """ 
@groups_bp.route('/savechanges', methods=['POST', 'GET'])
@session_required
def savechanges(current_user): 
	group2 = {
			"id": int(request.form.get("group_id")),
			"name": request.form.get("name"),
			"description": request.form.get("description"),
			"conversations": request.form.getlist("conv"), 
			"username": current_user
		}

	mongo.db.groups.replace_one({'id': int(request.form.get("group_id"))}, group2)
	
	return redirect('/groups')


""" Delete a group """ 
@groups_bp.route('/deletegroup/<group_id>', methods=['POST', 'GET'])
@session_required
def deletegroup(current_user, group_id): 
	
	mongo.db.groups.delete_one({'id' : group_id})
	print("Group deleted! ")
	
	return redirect('/groups')


""" Broadcast to a group of users """ 
@groups_bp.route('/broadcast', methods=['POST', 'GET'])
@session_required
def broadcast(current_user): 
	if request.method == 'POST': 
		
		#message to send
		message = request.form.get("message")

		# groups selected
		groups = request.form.getlist("groups")
		
		if "all_users" in groups: 
			send_to_all_users(message)
		else: 
			send_to_groups(groups, message)

		return redirect ('/broadcast')
	else: 
		groups_list = []
		groups = mongo.db.groups.find({'username': current_user})

		for group in groups: 
			groups_list.append({'name': "{}".format(group["name"]), 'id': "{}".format(group["id"])})

		return render_template('broadcast.html', groups=groups_list, owner=session['owner'])
