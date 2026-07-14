from extensions import db
import pytz
import datetime


 
student_skill = db.Table(
    "student_skill",

    db.Column("student_id", db.Integer, db.ForeignKey("students_info.id"), primary_key=True),
    db.Column("skill_id", db.Integer, db.ForeignKey("skills.id"), primary_key=True)
   
)

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



    # one to one 
    profile = db.relationship("StudentProfile",back_populates = "student", uselist=False, cascade="all,delete-orphan")

    # one to many 
    projects = db.relationship("Project",back_populates = "student", cascade="all,delete-orphan", lazy=True)

    # many to many
    skills = db.relationship("Skill",secondary = student_skill ,back_populates = "students", lazy=True)
   
    def __repr__(self):
        return f"Student - {self.name}"



class Book(db.Model):
    __tablename__ = "books_info"

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(120), nullable = False)
    description = db.Column(db.Text, nullable = True, default = "")


    def __repr__(self):
        return f"Book - {self.title}"
    




# one to one 
class StudentProfile(db.Model):
    __tablename__ = "student_profiles"

    id = db.Column(db.Integer, primary_key = True)
    linkedin = db.Column(db.String(255))
    github = db.Column(db.String(255))
    bio = db.Column(db.Text)
    student_id = db.Column(db.Integer, db.ForeignKey("students_info.id"),  unique= True, nullable=False)
    

    student = db.relationship("Student",back_populates = "profile")
  
    def __repr__(self):
        return f"Student profile {self.id}"


# 1 to many 
class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    student_id = db.Column(db.Integer, db.ForeignKey("students_info.id"), nullable=False)

    student = db.relationship("Student",back_populates = "projects")

    def __repr__(self):
        return f"Project - {self.title}"
    
# many to many
class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), unique=True, nullable=False)
   
    students = db.relationship("Student",secondary = student_skill ,back_populates = "skills")

    def __repr__(self):
        return f"Skill - {self.name}"


