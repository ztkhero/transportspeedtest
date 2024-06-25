from flask import Flask, render_template, jsonify, request, send_file
import os
import socket
import time
app = Flask(__name__)

# Define paths
STATIC_DIR = 'static'
TEST_FILE_PATH = os.path.join(STATIC_DIR, 'testfile')
TEST_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

def create_test_file():
    # Ensure the static directory exists
    os.makedirs(STATIC_DIR, exist_ok=True)
    
    # Create the test file
    with open(TEST_FILE_PATH, 'wb') as f:
        f.write(os.urandom(TEST_FILE_SIZE))

def get_client_ip():
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    elif request.headers.get("X-Real-IP"):
        return request.headers.get("X-Real-IP")
    else:
        return request.remote_addr

@app.route('/')
def index():
    return render_template('speedtest.html')

@app.route('/start_test')
def start_test():
    client_ip = get_client_ip()
    return jsonify({'client_ip': client_ip})

@app.route('/download_test')
def download_test():
    # Ensure the file exists before sending
    if not os.path.exists(TEST_FILE_PATH):
        create_test_file()
    return send_file(TEST_FILE_PATH, as_attachment=True)

@app.route('/upload', methods=['POST'])
def upload():
    # Simulating upload by receiving data
    data = request.get_data()
    return 'Upload received'

@app.route('/ping')
def ping():
    return 'pong'

if __name__ == '__main__':
    create_test_file()
    app.run(debug=True, host='0.0.0.0')