# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for
import paramiko
import json
import threading
from gunicorn import glogging

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    hostname = request.form['hostname']
    username = request.form['username']
    password = request.form['password']
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password)
        return jsonify({"status": "authenticated"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/terminal')
def terminal():
    return render_template('terminal.html')

@app.route('/command', methods=['POST'])
def command():
    data = request.json
    command = data.get('command')
    
    if not command:
        return jsonify({"status": "error", "message": "No command provided"}), 400
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Here we're assuming the user credentials are passed with every command for simplicity
    hostname = data.get('hostname')
    username = data.get('username')
    password = data.get('password')

    try:
        ssh.connect(hostname, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(command)
        
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        ssh.close()
        
        return jsonify({
            "status": "success",
            "output": output,
            "error": error
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
else:
    gunicorn_error_logger = glogging.Logger(app.logger, glogging.ERROR)
    app.logger.handlers = gunicorn_error_logger.handlers
    app.logger.setLevel(gunicorn_error_logger.level)
