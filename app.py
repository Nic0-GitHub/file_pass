import logging
from flask import Flask, abort, flash, render_template, send_file, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask.logging import default_handler
from utils import get_files, get_users_from_json, group_provided_items_by_type, stream_handler, file_handler
from constants import *
from classes import FileTypes, ProvidedItem, User
from sys import argv
import os


# app
app = Flask(__name__, template_folder='./static/templates')
app.secret_key = 'tu_clave_secreta_aqui'

# app-logger
app.logger.addHandler(stream_handler)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

app.logger.removeHandler(default_handler)
werkzeug_logger = logging.getLogger('werkzeug')


# auth
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# auth-data
users_json = get_users_from_json()
users: dict[str, User] = { str(user['id']): User(**user) for user in users_json['users'] }
groups = users_json.get('groups')

def info(*args, **kwargs):
    return app.logger.info(*args, **kwargs)


@app.route('/')
@login_required
def index():
    info(f"{request.remote_addr} requested: '{request.url}'({request.method})")
    try:
        files_in_uploads = get_files(UPLOAD_DIR)
        files_in_downloads = sorted(get_files(DOWNLOAD_DIR))
        provided_items = list(map(ProvidedItem, files_in_downloads))
        grouped_provided_items = group_provided_items_by_type(provided_items)
        files_in_uploads.sort()
    except FileNotFoundError:
        grouped_provided_items = {file_type: [] for file_type in FileTypes}
        files_in_uploads = []
        
    return render_template('index.html', grouped_provided_items=grouped_provided_items, upload_files=files_in_uploads)

@app.route('/download/<filename>', methods=['GET'])
@login_required
def download_file(filename):
    info(f"{request.remote_addr} requested: '{request.url}'({request.method})")
    safe_path = os.path.join(DOWNLOAD_DIR, filename)
    if not os.path.isfile(safe_path):
        abort(404, description="Archivo no encontrado")
    return send_file(safe_path, as_attachment=True)


@app.route('/upload', methods=['POST'])
@login_required
def upload_files():
    info(f"{request.remote_addr} requested: '{request.url}'({request.method})")
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(url_for('index'))
    
    if file:
        safe_filename = os.path.basename(file.filename)
        file.save(os.path.join(UPLOAD_DIR, safe_filename))
        app.logger.info(f"{request.remote_addr} uploaded '{safe_filename}'")
        return redirect(url_for('index'))

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((
            user for user in users.values() 
                if user.username == username and user.password == password), None)
        if user:
            login_user(user)
            info(f"{request.remote_addr} started a session with user '{user.username}'")
            return redirect(url_for('index'))
        else:
            flash('Nombre de usuario o contraseña incorrectos', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port_selected = int(argv[1]) if len(argv) > 1 else 5000
    debug_mode = int(argv[2]) if len(argv) > 2 else 1
    host_selected = '0.0.0.0'
    app.run(host=host_selected, port=port_selected, debug=debug_mode)
    werkzeug_logger.disabled = True
