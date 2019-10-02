from .common.session import session_required
from flask import Blueprint, redirect
base_bp = Blueprint('web_application', __name__, template_folder='templates', static_folder="static", static_url_path='/web_application/static')


@base_bp.route('/')
@session_required
def base(current_user):
    return redirect('/inbox')