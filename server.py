"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, get_flashed_messages

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie



app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users"""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/signup", methods=["POST", "GET"])
def sign_up_form():
    """Show and submit sign up form"""

    return render_template("sign_up_form.html")

@app.route("/login", methods=["POST", "GET"])
def login_form():
    """Show and submit login form"""

    return render_template("login_form.html")

#////////////

@app.route("/login-verification", methods=["POST"])
def check_for_email_password_match():
    """Check if email and password match"""

    email = request.form.get("email")
    password = request.form.get("password")

    users_with_match = db.session.query(User).filter((User.email == email) 
        & (User.password == password)).all()

    if len(users_with_match) == 0:
        flash("Information you provided does not match our records. Please try again.")
        return render_template('homepage.html')
    else:
        user = users_with_match[0].user_id
        session['user'] = user
        flash("You have been successfully logged in.")
        return redirect("/")


@app.route("/processing-form", methods=["POST"])
def check_for_user():
    """Check if user exists. If not, add new user to database."""

    email = request.form.get("email")
    password = request.form.get("password")

    users_with_email = db.session.query(User).filter(User.email == email).all()

    if len(users_with_email) == 0:
        user=User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Great success!!!!!!!!")
        return render_template('homepage.html')
    else:
        flash("""User with this email address already exists. 
            Please register with a different email address.""")
        return redirect("/")

@app.route("/logout")
def logout():
    """Logs out user"""

    session['user'] = None
    flash("Logged out!")
    return redirect ("/")
    

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
