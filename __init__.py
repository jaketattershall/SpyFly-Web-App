from flask import Flask, session, request
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy



# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():

    # Config for the MySQL database
    username = 'root'
    password = 'RCYQYoJ5HctzD'
    server = 'localhost'

    # Creates a flask app
    app = Flask(__name__)
 
    # Creates an instance of SQLAlchemy
    db = SQLAlchemy()


    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['MYSQL_HOST'] = 'localhost'
    #app.config['MYSQL_DATABASE_PORT'] = 3306
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'z?#ir4x#RCYQYoJ5HctzD'
    app.config['MYSQL_DB'] = ''
    app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:z?#ir4x#RCYQYoJ5HctzD@localhost/spyfly'

    

    #print(app.config['SERVER_NAME'])

    # Initiates the SQLAlchemy on the app
    db.init_app(app)

    # Blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    # Blueprint for API parts of app
    from .API import API as API_blueprint
    app.register_blueprint(API_blueprint)


    # Starts the app
    return app
