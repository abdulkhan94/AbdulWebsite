from flask import Flask, redirect, url_for, render_template, request, session
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "hi"
app.permanent_session_lifetime = timedelta(minutes=5)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class users(db.Model):
    uid = db.Column("uid", db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    
    def __init__(self, _uid, _name, _email):
        self.uid = _uid
        self.name = _name
        self.email = _email

    
class jobs(db.Model):
    jid = db.Column("jid", db.Integer, primary_key = True)
    desc = db.Column(db.String(100))
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable = False)
    
    def __init__(self, _jid, _desc, _uid):
        self.jid = _jid
        self.desc = _desc
        self.uid = _uid
    
    
@app.route('/create/', methods = ["POST", "GET"])
def create():
    if request.method == "POST":
        em_form = request.form["email"]
        name_form = request.form["nm"]
        uid_form = request.form["uid"]
        usr = users(uid_form, name_form, em_form)
        db.session.add(usr)
        db.session.commit()
        return redirect(url_for("view"))
    else:
        return render_template("create.html")
        
        
@app.route('/job/', methods = ["POST", "GET"])
def job():
    if request.method == "POST":
        jid_form = request.form["jid"]
        desc_form = request.form["desc"]
        uid_form = request.form["uid"]
        jb = jobs(jid_form, desc_form, uid_form)
        db.session.add(jb)
        db.session.commit()
        return render_template("jobs.html")
    else:
        return render_template("jobs.html")
        
        
        
@app.route('/view/')
def view():
    return render_template("view.html", values = users.query.all(), others = jobs.query.all())
    

@app.route('/')
def home():
    found_user = users.query.filter_by(email="abdullahnawaz94@gmail.com").first()
    found_user.email = "abdullah_changed@gmail.com"
    print(found_user.email)
    db.session.commit()
    return render_template("index.html")


@app.route('/time/')
def time():
    dt = datetime.now()
    return render_template("timer.html", tim=dt)


@app.route('/login/', methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent= True
        user_form = request.form["nm"]
        session["user"] = user_form
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route('/user/', methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        username = session["user"]
       
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
        else:
            if "email" in session:
                email = session["email"]
        
        return render_template("user.html", email=email, usr = username)
    else:
        return redirect(url_for("login"))


@app.route('/logout')
def logout():
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))


if __name__ == '__main__':
    db.create_all()
    app.run(port=8000, debug=True)

