from flask import Blueprint, render_template, session, redirect, url_for
from . import db

# Creates the blueprint for the file
main = Blueprint('main', __name__)

# Renders the index page
@main.route('/')
def index():
    return render_template('index.html')

# Renders the profile page if a user is logged in
# If user is not logged in returns them to login
@main.route('/profile')
def profile():
    # Checks the session cookie to see if user logged in
   
    print("PROFILE SESSION:")
  

    print(session)
    if 'loggedin' in session:
        # Sends username to html file for rendering
        return render_template('profile.html', username = session['username'])
    else:
        print("NOT LOGGED IN")
        return redirect(url_for('auth.login'))

    

# Sends user to display page
@main.route('/profile', methods=['POST'])
def profile_post():
    return redirect(url_for('auth.display'))
    