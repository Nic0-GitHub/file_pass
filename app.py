import logging
from flask.logging import default_handler
from flask import Flask, abort, flash, render_template, send_file, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from utils import  get_files, get_users_from_json, stream_handler, file_handler
from classes import User
from sys import argv
import os

# CONST
FILES_DIR = './files'
UPLOAD_DIR = './download'
LOGS_DIR = './logs'

# app
app = Flask(__name__, template_folder='./static/templates')
app.secret_key = 'tu_clave_secreta_aqui'

# app-logger
app.logger.addHandler(stream_handler)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

app.logger.removeHandler(default_handler)
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.disabled = True

# auth
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# auth-data
users_json = get_users_from_json()
users: dict[str, User] = { str(user['id']): User(**user) for user in users_json['users'] }
groups = users_json.get('groups')

# Crear directorios si no existen
os.makedirs(FILES_DIR,  exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(LOGS_DIR,   exist_ok=True)

@app.route('/')
def index():
    app.logger.info("Esto esta todo bien!")
    try:
        files = get_files(FILES_DIR)
        download_files = get_files(UPLOAD_DIR)
        files.sort()
        download_files.sort()
    except FileNotFoundError:
        files = []
        download_files = []
    return render_template('index.html', files=files, download_files = download_files)

@app.route('/download/<filename>', methods=['GET'])
@login_required
def download_file(filename):
    safe_path = os.path.join(FILES_DIR, filename)
    if not os.path.isfile(safe_path):
        abort(404, description="Archivo no encontrado")
    return send_file(safe_path, as_attachment=True)

@app.route('/upload', methods=['POST'])
@login_required
def upload_files():
    
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    
    if file:
        safe_filename = os.path.basename(file.filename)
        file.save(os.path.join(UPLOAD_DIR, safe_filename))
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
    app.run(host='0.0.0.0', port=port_selected, debug=debug_mode)
