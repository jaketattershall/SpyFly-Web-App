from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import users, sms
from . import db

# Creates the blueprint for the file 
auth = Blueprint('auth', __name__)



# Renders the login page
@auth.route('/login')
def login():
    
    return render_template('login.html')

# Logs the user in
@auth.route('/login', methods=['POST'])
def login_post():
    try:
        # Gets the user inputs from the page
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
    
        # Checks if user credentials are correct
        if checkLogin(email, password):
            username = getAccName(email)

            # Creates a secure cookie to store login data
            createSession(email, username)  
            print(url_for('main.profile'))

            # Sends the user to the profile page
            return redirect(url_for('main.profile'))

        # If credentials not correct flash error and return to login
        flash('Incorrect details entered')
        return redirect(url_for('auth.login'))
    except Exception as e:
        print("caught error: {}".format(e))
        return redirect(url_for('auth.login'))

# Checks user login
def checkLogin(email, password):
    
    print(email);

    
    # SQLAlchemy query to check user exists
    user = users.query.filter_by(email=email).first()
    print(user)

    # If credentials bad
    if not user or not check_password_hash(user.password, password):
        
        print("CHECKLOGINTESTFALSE")
        # Failure
        return False
    else:
        # Else success
        print("CHECKLOGINTESTTRUE")
        return True
       

# Gets the account name from the email
def getAccName(email):
    print("IN GET ACCOUNT NAME")
    # SQLAlchemy query to get user name
    account = users.query.filter_by(email=email)
    name = account.first().user
    print("GET USER NAME  = ")
    print(name)
    return name



def createSession(email, username):
    print("In create session")
    session['loggedin'] = True
    session['email'] = email
    session['username'] = username
    session['table'] = 'sms'
    print("end of create session")
    

@auth.route('/signup')
def signup():
    return render_template('signup.html')




@auth.route('/signup', methods=['POST'])
def signup_post():
    
    print("TEST")
    email = request.form.get('email')
    name = request.form.get('name') 
    password = request.form.get('password')

    # Hash of the password generated using werkzeug sha256 algorithm
    hashedpass = generate_password_hash(password, method="sha256")


    user = users.query.filter_by(email=email).first() 
    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    newUser = users(email=email, user=name, password=hashedpass)
    db.session.add(newUser)
    db.session.commit()
    return redirect(url_for('auth.login')) 


@auth.route('/test')
def test():
    return render_template('test.html')

@auth.route('/display')
def display():

  
    #print("INSIDE DISPLAY FUNCTION")
    if 'loggedin' in session:
        print(session['table'])
        table = session['table']

        # Does not allow user table to be printed in the event of manipulated cookie
        if session['table'] == 'users':
            session['table'] = 'sms'

        userEmail = session['email']

        
        data = [['demo@demo.com', '2021-06-30 17:25:38', 'Android is always a sweet treat!', '6505551212']]
        columns = getColumns(table)
        
            
        # Renders the display page and passes the user data to the html for rendering
        print("data = {}".format(data))
        print("columns = {}".format(columns))
        return render_template('display.html', data=data, columns=columns)
            

    # If user not logged in go to login page
    return redirect(url_for('auth.login'))

   

# Relevant buttons to display different data
@auth.route('/display', methods=['POST'])
def display_post():
    if request.form['displayButton'] == 'Call History':
        session['table'] = "calls"
        return redirect(url_for('auth.display'))
    elif request.form['displayButton'] == 'SMS History':
        session['table'] = "sms"
        return redirect(url_for('auth.display'))
    elif request.form['displayButton'] == 'Web History':
        session['table'] = "webhistory"
        return redirect(url_for('auth.display'))
    elif request.form['displayButton'] == 'Location Tracking':
        session['table'] = "location"
        return redirect(url_for('auth.display'))


        
# Deletes user session cookie to log out
@auth.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('auth.login'))


# Gets the data from the relevant database table
def getData(table, email):
    

    tableNames = getColumns(table)
    columnNo = len(tableNames)
    data = []
    # Loops throw the rows in the table, adding the data to a list
    print("USER EMAIL: " + email)   
    print("QUERY : ")
     
   
   
   
    return data

# Get the column names
def getColumns(table):
    print(sms.__table__.c.keys())
    columns = []
    columns = sms.__table__.c.keys()
    return columns