from flask import session, redirect
from functools import wraps


def session_required(f):
	@wraps(f)
	def decorated(*args, **kwargs): 
		if not 'username' in session:
			return redirect('/login')
		current_user = session['username']
		return f(current_user, *args, **kwargs)

	return decorated
