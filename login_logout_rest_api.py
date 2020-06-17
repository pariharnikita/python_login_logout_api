import sqlite3
import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

session = []

app = Flask(__name__)
app.secret_key = 'any random string'
app.config["PERMANENT_SESSION_TIMEOUT"] = datetime.timedelta(minutes=15)
app.config["DEBUG"] = True

CORS(app)

@app.route('/api/v3/add_user',methods=['POST'])
def add_user():
	username = request.json.get("username")
	password = request.json.get("password")
	con = sqlite3.connect("user.db")
	cur = con.cursor()
	cur.execute("INSERT INTO USERS (USERNAME, PASSWORD) VALUES (?,?)",(username, generate_password_hash(password)))
	con.commit()
	return jsonify({'message':'User added successfully','username':username})


@app.route('/api/v3/login',methods=['POST'])
def login():			
	username = request.json.get('username')
	if username in session:
		return jsonify({'message':'You are already logged in','username':username})
	else:
		password = request.json.get('password')
		if username and password:
			con = sqlite3.connect("user.db")
			cur = con.cursor()
			cur.execute("SELECT USERNAME,PASSWORD FROM USERS WHERE USERNAME =?",(username,))
			res = cur.fetchone()
			if res:
				if check_password_hash(res[1],password):
					session.append(username)
					return jsonify({'message':'You are logged in successfully','username':username})
				else:
					return jsonify({'message':'Unauthorized'})
			else:
					return jsonify({'message':'Wrong Credential'})
		else:
			return jsonify({'message':'Please provide valide username and password.'})

@app.route('/api/v3/logout',methods=['POST'])
def logout():
	username = request.json.get('username')
	if username in session:
		session.remove(username)
		return jsonify({'message':'You are logged out successfully','username':username})
	else:
		return jsonify({'message':'You are already logged out','username':username})

app.run()
# curl -i -H "Content-Type: application/json" -X POST -d "{\"username\":\"user1\",\"password\":\"password\"}" http://localhost:5000/api/v3/user_add







