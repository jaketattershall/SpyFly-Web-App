from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify, abort
import requests
import json

from .models import users, sms
from . import db
from .auth import checkLogin

API = Blueprint('API', __name__)


@API.route('/api/login', methods=['POST'])
def appLogin():
    print("INCOMING POST REQUEST")
 
    try:
        if not request.json:
            print("Incoming data not json")
            response = {"value": "false"}
            return jsonify(response) 
        data = json.loads(request.get_data())
        email = data["email"]
        password = data["password"]
        
        print(email + " : " + password)

   
        if checkLogin(email, password):
            response = {"value": "true"}
            return jsonify(response)
        else:
            response = {"value": "false"}
            return jsonify(response)
    except Exception as e:
        print("Error with incoming data : {}".format(e))
        response = {"value": "false", "error": "404"}
        return jsonify(response)


@API.route('/api/sendData', methods=['POST'])
def appSendData():
    print("INCOMING DATA")

    data = json.loads(request.get_data())

    print(data)
    
    dataType = data['dataType'];


    if dataType == 'sms':
        insertSMS(data)
        response = {"value": "true"}
        return jsonify(response) 

    if dataType == 'location':
        insertLoc(data)
        response = {"value": "true"}
        return jsonify(response) 

    
    response = {"value": "false"}
    return jsonify(response) 



def insertSMS(data):
    user = "test@test.com"
    msg = data['msg']
    number = data['number']
    time = data['time']

    newSMS = sms(email = user, message=msg, number=number, dateTime=time)

    db.session.add(newSMS)
    db.session.commit()

    