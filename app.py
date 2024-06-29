import logging
from logging.handlers import RotatingFileHandler
import os
from random import choice
from sys import argv
from flask import Flask, abort, render_template, send_file, request, redirect, url_for
import toml

app = Flask(__name__)
FILES_DIR = './files'
UPLOAD_DIR = './download'
LOGS_DIR = './logs'
IPS_FILE = open("./ips.toml", 'r+')

# Crear directorios si no existen
os.makedirs(FILES_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

ips_emotes = toml.load(IPS_FILE)



@app.route('/')
def index():
    try:
        files = [f for f in os.listdir(FILES_DIR) if os.path.isfile(os.path.join(FILES_DIR, f))]
    except FileNotFoundError:
        files = []
    return render_template('index.html', files=files)

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    safe_path = os.path.join(FILES_DIR, filename)
    if not os.path.isfile(safe_path):
        abort(404, description="Archivo no encontrado")
    return send_file(safe_path, as_attachment=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))

    emote = ips_emotes.get(request.remote_addr)
    if not emote:
        emotes:list[str] = ips_emotes.get('emotes')
        emote = choice(emotes)
        emotes.remove(emote)
        ips_emotes['emotes'] = emotes
        ips_emotes[request.remote_addr] = emote
        toml.dump(ips_emotes, open(IPS_FILE.name, 'w'))
    app.logger.info(f"{emote} upload '{file.filename}'")
        
    if file:
        safe_filename = os.path.basename(file.filename)
        file.save(os.path.join(UPLOAD_DIR, safe_filename))
        return redirect(url_for('index'))

if __name__ == '__main__':
    port_selected = int(argv[1]) if len(argv) > 1 else 5000
    debug_mode = int(argv[2]) if len(argv) > 2 else 1
    app.run(host='0.0.0.0', port=port_selected, debug=debug_mode)
