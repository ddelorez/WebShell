# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for
import paramiko
import json

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
        ssh.close()  # Close the connection after validation
        return redirect(url_for('terminal'))
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/terminal')
def terminal():
    return render_template('terminal.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')