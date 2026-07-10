from flask_sqlalchemy import SQLAlchemy
import pytz
import datetime


db = SQLAlchemy()



def indian_time():
    india = pytz.timezone("Asia/Kolkata")
    return datetime.now(india)

class User(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50),nullable = False )
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(50))
    phone = db.Column(db.String(15), nullable = True)

    def __repr__(self):
        return f"User - {self.name}"

class Student(db.Model):
    __tablename__ = "students_info"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    dob = db.Column(db.Date)
    address = db.Column(db.Text)
    profile_pic = db.Column(db.String(255))
    resume = db.Column(db.String(255))
    marks = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default = True)
    created_at = db.Column(db.DateTime, default = indian_time)
    update_at = db.Column(db.DateTime, default = indian_time, onupdate=indian_time)
   
    def __repr__(self):
        return f"Student - {self.name}"



class Book(db.Model):
    __tablename__ = "books_info"

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(120), nullable = False)


    def __repr__(self):
        return f"Book - {self.title}"