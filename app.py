from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,static_folder="static",static_url_path="/static")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50),nullable = False )
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(50))

with app.app_context():
    db.create_all()

# users = [
#     {
#         "email": "mohit@gmail.com",
#         "password": "123",
#         "name": "mohit"
#     },
#     {
#         "email": "aman@gmail.com",
#         "password": "456",
#         "name": "aman"
#     },

# ]


@app.route("/")
def index():
    info = {
        "name": "mohit",
        "age": 10,
        "address": "delhi, india",
        "skills"  : ["python", "java", "c++", "html", "css", "javascript"]
    }
    return render_template("index.html", data = info)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form_email = request.form.get("email")
        form_password = request.form.get("password")
        # print(form_email, form_password)

        current_user = User.query.filter_by(email = form_email).first()
        if current_user and current_user.password == form_password:
            return redirect(url_for('home', username = current_user.name))
        
        return "login failed"
    else:
        return render_template("login.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/home")
def home():
    username = request.args.get("username", "Guest")
    return render_template("home.html", name=username)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        form_username = request.form.get("username")
        form_email = request.form.get("email")
        form_password = request.form.get("password")
        print(form_email, form_password, form_username)

        new_user = User(
           email =  form_email,
           password = form_password,
           name= form_username
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))

     
    else:
        return render_template("register.html")




if __name__=="__main__":
    app.run(debug=True, use_reloader=True)
