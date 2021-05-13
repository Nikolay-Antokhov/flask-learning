from flask import Flask, abort, request
from db import usersList
from jwt import JWT

app = Flask(__name__)

def wrapper(fn):
    def inWrapper(*args):
        jwt = JWT.parseHeader(request.headers.get('Authorization'))
        if not jwt.isValid():
            abort(401)
        return fn(*args)
    return inWrapper

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/users/', methods=[ 'GET' ])
def usersGet():
    return { 'users': usersList }

@app.route('/users/', methods=[ 'POST' ])
@wrapper
def userCreate():
    data = request.json
    usersList.append({
        'age': data['age'],
        'id': usersList[-1]['id'] + 1,
        'name': data['name'],
    })
    return { 'users': usersList }

@app.route('/users/<int:userId>/', methods=[ 'GET' ])
def userGet(userId):
    for user in usersList:
        if user['id'] == userId:
            return user
    return {}

@app.route('/signin/', methods=[ 'POST' ])
def userSignIn():
    data = request.json
    for user in usersList:
        if user['email'] == data['email'] and user['password'] == data['password']:
            jwt = JWT({ 'id': user['id'] })
            return { 'token': jwt.generateToken() }
    abort(401)
