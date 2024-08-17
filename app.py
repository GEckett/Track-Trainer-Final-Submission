from flask import Flask, flash, redirect, render_template, request, session, url_for, g
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps


# Create the db extension
db = SQLAlchemy()

# Configure application
app = Flask(__name__, template_folder='templates')

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tracks.db"

# Set secret key
app.config['SECRET_KEY'] = 'f3cfe9ed8fae309f02079dbf'

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# initialize the app with the extension
db.init_app(app)

# Create the username table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    hash = db.Column(db.String, nullable=False)
# Create the tracks table
class Tracks(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=False, nullable=False)
    track_name = db.Column(db.String, unique=False, nullable=False)
    track_img = db.Column(db.String, unique=False, nullable=False)
    lap_time = db.Column(db.String, nullable=True)
# Create the notes table
class Notes(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=False, nullable=False)
    track_name = db.Column(db.String, unique=False, nullable=False)
    turn_no = db.Column(db.Integer, nullable=False)
    event = db.Column(db.String, nullable=False)
    note = db.Column(db.String, nullable=False)
    ref_img = db.Column(db.String, nullable=True)
# Creates schema
with app.app_context():
    db.create_all()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session["user_id"] is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response    

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tracks")
def tracks():
    user_in_session = session["user_id"]
    tracks = Tracks.query.filter_by(user_id=user_in_session)
    return render_template("index.html", tracks=tracks)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("register.html", error="Must provide username")

        # Ensure password was submitted
        if not request.form.get("password"):
            return render_template("register.html", error="Must provide password")

        # Ensure password was confirmed
        if request.form.get("password") != request.form.get("confirm_password"):
            return render_template("register.html", error="Passwords do not match")

        # Check for duplicate users then add the user's entry into the database if check passed
        if User.query.filter_by(username=request.form.get("username")).first() is not None:
            return render_template("register.html", error="Username already taken")

        # Generate hash
        user = request.form.get("username")
        password = request.form.get("password")
        hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

        # Add user to database
        new_user = User(username=user, hash=hash)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/")
    
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            return render_template("login.html", error="Username not entered. Please try again.")

        # Ensure password was submitted
        if not password:
            return render_template("login.html", error="Password not entered. Please try again.")

        # Query database for username
        user = User.query.filter_by(username=username).first()

        # Ensure username exists and password is correct
        if not user or not check_password_hash(user.hash, password):
            return render_template("login.html", error="Login details not correct. Please try again.")

        # Remember which user has logged in
        session["user_id"] = user.id

        # Redirect user to home page
        return redirect("/tracks")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html")

@app.route("/add", methods=["GET","POST"])
@login_required
def add():
    if request.method == "POST":

        # Get the user in session
        user_in_session = session["user_id"]

        # Ensure Track Name was submitted
        if not request.form.get("track_name"):
            return render_template("register.html", error="Must provide track name")

        # Ensure Track Map was submitted
        if not request.form.get("track_url"):
            return render_template("register.html", error="Must provide track map link")

        # Check for duplicate tracks with user then add the user's entry into the database if check passed
        if Tracks.query.filter_by(track_name=request.form.get("track_name"),user_id=user_in_session).first() is not None:
            return render_template("register.html", error="Track already added")

        # Get form entries
        track_name = request.form.get("track_name")
        track_url = request.form.get("track_url")
        lap_time = request.form.get("lap_time")

        # Add track to database
        new_track = Tracks(user_id=user_in_session, track_name=track_name, track_img=track_url, lap_time=lap_time)
        db.session.add(new_track)
        db.session.commit()
        return redirect("/tracks")
    
    else:
        return render_template("add.html")

@app.route("/FAQ")
def FAQ():
    return render_template("FAQ.html")

@app.route("/notes/<track_name>", methods=["GET","POST"])
@login_required
def notes(track_name):
    if request.method == "POST":

        # Get the user in session
        user_in_session = session["user_id"]

        # Ensure Turn no. was submitted
        if not request.form.get("turn_no"):
            return render_template("notes.html", error="Must provide turn no.")
        
        # Ensure Event was submitted
        if not request.form.get("event"):
            return render_template("notes.html", error="Must provide turning event")
        
        # Ensure Note was submitted
        if not request.form.get("note"):
            return render_template("notes.html", error="Must provide note")

        # Get form entries
        turn_no = request.form.get("turn_no")
        event = request.form.get("event")
        note = request.form.get("note")
        ref_img = request.form.get("img")

        # Add note to database
        new_track = Notes(user_id=user_in_session, track_name=track_name, turn_no=turn_no, event=event, note=note,ref_img=ref_img)
        db.session.add(new_track)
        db.session.commit()
        return redirect("/tracks")
    
    else:
        return render_template("notes.html")

@app.route("/retime/<track_name>", methods=["GET","POST"])
@login_required
def retime(track_name):
    if request.method == "POST":

        # Get the user in session
        user_in_session = session["user_id"]

        track = Tracks.query.filter_by(track_name=track_name,user_id=user_in_session).first()
        print(track)

        # Ensure Lap Time was submitted
        if not request.form.get("lap_time"):
            return render_template("retime.html", error="Must provide lap time")

        # Get form entries
        lap_time = request.form.get("lap_time")
        print(track_name)

        # Update database entry
        track.lap_time = lap_time
        db.session.commit()
        return redirect("/tracks")
    
    else:
        return render_template("retime.html")

@app.route("/view_notes/<track_name>")
def view_notes(track_name):
    user_in_session = session["user_id"]
    notes = Notes.query.filter_by(user_id=user_in_session, track_name=track_name)
    return render_template("view_notes.html", notes=notes)



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

if __name__ == "__main__":
    # Creates database schema
    with app.app_context():
        db.create_all()

    app.run(debug=True)