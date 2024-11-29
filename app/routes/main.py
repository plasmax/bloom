from flask import Blueprint, render_template, current_app, request, jsonify
from flask_login import login_required
from app.services.sandbox import PythonSandbox
from app.services.file_manager import FileManager

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
    file_manager = FileManager()
    files = file_manager.list_files()
    return render_template('files.html', title='Files', files=files)

@bp.route('/sandbox')
@login_required
def sandbox():
    return render_template('sandbox.html', title='Python Sandbox')

@bp.route('/sandbox/execute', methods=['POST'])
@login_required
def execute_code():
    data = request.get_json()
    if not data or 'code' not in data:
        return jsonify({'success': False, 'error': 'No code provided'})
    
    code = data['code']
    sandbox = PythonSandbox()
    result = sandbox.execute(code)
    
    return jsonify(result)

@bp.route('/files/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'})
    
    file_manager = FileManager()
    result = file_manager.save_file(file)
    
    return jsonify(result)

@bp.route('/files/<filename>')
@login_required
def get_file(filename):
    file_manager = FileManager()
    result = file_manager.read_file(filename)
    
    if 'error' in result:
        return jsonify({'success': False, 'error': result['error']}), 404
        
    return jsonify(result)

@bp.route('/files/<filename>', methods=['DELETE'])
@login_required
def delete_file(filename):
    file_manager = FileManager()
    result = file_manager.delete_file(filename)
    
    if 'error' in result:
        return jsonify({'success': False, 'error': result['error']}), 404
        
    return jsonify(result)
