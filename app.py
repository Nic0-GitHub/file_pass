import os
from flask import Flask, abort, render_template, send_file, request, redirect, url_for

app = Flask(__name__)
FILES_DIR = './files'
UPLOAD_DIR = './download'

# Crear directorios si no existen
os.makedirs(FILES_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

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

    if file:
        safe_filename = os.path.basename(file.filename)
        file.save(os.path.join(UPLOAD_DIR, safe_filename))
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=1)
