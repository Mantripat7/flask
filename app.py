from flask import Flask, render_template, request, redirect, session, url_for, flash
from datetime import datetime
import os 
from werkzeug.utils import secure_filename
import requests
from extensions import db , mail, migrate


app = Flask(__name__,static_folder="static",static_url_path="/static")
app.secret_key = "12345"
# configuration for db 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# configuration for uploads
app.config["UPLOAD_PP"] = "static/uploads/profile_pics" 
app.config["UPLOAD_RESUME"] = "static/uploads/resumes"
# configuration for mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'openmaterial2@gmail.com'
app.config['MAIL_PASSWORD'] = 'okiu rvrt ozze dkks'
app.config['MAIL_DEFAULT_SENDER'] = 'openmaterial2@gmail.com'

db.init_app(app)
mail.init_app(app)
migrate.init_app(app, db)
 

from models import *



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
            session["user_id"] = current_user.id
            session["user_name"] = current_user.name
            flash("Login Successful")
            return redirect(url_for('home', username = current_user.name))
        
        flash("Invalid Credentails")
        return redirect(url_for('login'))
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
    students = Student.query.all()
    return render_template("home.html", name=username, students=students)


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
     
        flash("Account Created")
        return redirect(url_for("login"))

     
    else:
        return render_template("register.html")

@app.route("/student", methods =["GET", "POST"])
def student():
    if "user_id" not in session:
        flash("Please login to add students")
        return redirect(url_for("login"))



    if request.method == "POST":
        form_name = request.form.get("name")
        form_email = request.form.get("email")
        form_dob = request.form.get("dob")
        form_marks = request.form.get("marks")
        form_address = request.form.get("address")
        form_profile_pic = request.files.get("profile_pic")
        form_resume = request.files.get("resume")
        form_is_active = request.form.get("is_active")

        if form_profile_pic and form_profile_pic.filename != "":
            pic_filename =  secure_filename(form_profile_pic.filename)
            path = os.path.join(app.config["UPLOAD_PP"] , pic_filename)
            form_profile_pic.save(path)
        else:
            pic_filename = None

        if form_resume and form_resume.filename != "":
            resume_filename =  secure_filename(form_resume.filename)
            path = os.path.join(app.config["UPLOAD_RESUME"] , resume_filename)
            form_resume.save(path)
        else:
            resume_filename = None
        update_dob = datetime.strptime(form_dob, "%Y-%m-%d").date()
        print(update_dob, type(update_dob))
        new_student = Student(
            name = form_name,
            email = form_email,
            dob = update_dob,
            marks = float(form_marks),
            address = form_address,
            profile_pic = pic_filename,
            resume = resume_filename,
            is_active = True if form_is_active == "on" else False
        )
        db.session.add(new_student)
        db.session.commit()

        print("student data added")
        return redirect(url_for("student"))

    return render_template("student.html")


@app.route("/delete_student/<int:student_id>" , methods = ["GET"])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if student:
        db.session.delete(student)
        db.session.commit()
        flash("Student deleted successfully")
        
    else:
        flash("Student not found")

    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully")
    return redirect(url_for("login"))


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        form_email = request.form.get("email")
        print( form_email)
        user= User.query.filter_by(email=form_email).first()
        if user:
            
            msg = Message("Password Reset Request", recipients=[form_email])
            msg.body = f"Hello {user.name},\n\nYou requested a password reset. Your new password is: 123 \n\nPlease keep it secure."
    
            mail.send(msg)
            print("mail sent")
            user.password = "123"
            db.session.commit()


            flash("Password reset email sent.")
            return redirect(url_for("login"))
        else:
            print("Email not found")
            flash("Email not found.")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/books", methods=["GET", "POST"] )
def book():
    search = request.args.get("search", "")

    page = request.args.get("page", 1, type=int)

    per_page = 3
    if search:
        books = Book.query.filter( Book.title.ilike(f"%{search}%") | Book.author.ilike(f"%{search}%") ).paginate(page=page, per_page=per_page, error_out=False)
    else:
        books = Book.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template("book.html", books=books, search = search)



@app.route("/weather")
def weather():

    url = "https://api.open-meteo.com/v1/forecast?latitude=88.88&longitude=77.87&current_weather=True"

    response = requests.get(url)

    data = response.json()


    return render_template("weather.html", data=data)


if __name__=="__main__":
    app.run(debug=True, use_reloader=True)
