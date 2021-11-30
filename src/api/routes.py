"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend"
    }

    return jsonify(response_body), 200




@api.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    # chek if the user exist

    if User.query.filter(User.email == data['email']).count() > 0 :
        return "user_exist", 404



    # create a user
    user = User(
        email=data["email"], 
        password=data['password'], 
        is_active=True
        )
    db.session.add(user)
    db.session.commit()
    
    #this operation es correcta pero no retorna nada (None, 204)
    
    return "", 204

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter(User.email == data['email']).first()
    if user is None:
        return '', 404
    

    if user.password != data['password']:
        return 'wrong-password', 400

    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id })


    
