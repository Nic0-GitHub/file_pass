import os
from random import choice
from sys import argv
from flask import Flask, abort, render_template, send_file, request, redirect, url_for
from utils import  get_files

app = Flask(__name__, template_folder='./static/templates')
FILES_DIR = './files'
UPLOAD_DIR = './download'
LOGS_DIR = './logs'

# Crear directorios si no existen
os.makedirs(FILES_DIR,  exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(LOGS_DIR,   exist_ok=True)

@app.route('/')
def index():
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
def download_file(filename):
    safe_path = os.path.join(FILES_DIR, filename)
    if not os.path.isfile(safe_path):
        abort(404, description="Archivo no encontrado")
    return send_file(safe_path, as_attachment=True)

@app.route('/upload', methods=['POST'])
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

if __name__ == '__main__':
    port_selected = int(argv[1]) if len(argv) > 1 else 5000
    debug_mode = int(argv[2]) if len(argv) > 2 else 1
    app.run(host='0.0.0.0', port=port_selected, debug=debug_mode)
