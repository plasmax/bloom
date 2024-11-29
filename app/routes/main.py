from flask import Blueprint, render_template, current_app
from flask_login import login_required

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@bp.route('/tasks')
@login_required
def tasks():
    return render_template('tasks.html', title='Tasks')

@bp.route('/files')
@login_required
def files():
    return render_template('files.html', title='Files')

@bp.route('/sandbox')
@login_required
def sandbox():
    return render_template('sandbox.html', title='Python Sandbox')
