from flask import render_template, request, redirect, session, url_for, flash
from datetime import datetime
import os 
from werkzeug.utils import secure_filename
from models import *
from __init__ import create_app
# from flask_migrate import Migrate

from flask_mail import Mail, Message, mail


app = create_app()

# migrate = Migrate(app, db)

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
            msg = Message(
                    subject = "Password Reset Request",
                    sender = app.config['MAIL_DEFAULT_SENDER'],
                    recipients = [form_email],
                   
            )

            msg.body = "Hello your new password is: 123456"
            mail.send(msg)

            

    return render_template("login.html")

if __name__=="__main__":
    app.run(debug=True, use_reloader=True)
