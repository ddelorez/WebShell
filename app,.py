# app.py
from flask import Flask, render_template, request, jsonify
import paramiko
import json

app = Flask(__name__)

# Placeholder for SSH credentials, you should use a secure method to manage these
SSH_CREDENTIALS = {
    'hostname': 'your.server.ip.or.hostname',
    'username': 'your_username',
    'password': 'your_password'
}

# Function to create and return an SSH client
def get_ssh_client():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(**SSH_CREDENTIALS)
    return ssh

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/connect', methods=['POST'])
def connect():
    try:
        ssh = get_ssh_client()
        return jsonify({"status": "connected"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')