from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__,static_folder="static",static_url_path="/static")

users = [
    {
        "email": "mohit@gmail.com",
        "password": "123",
        "name": "mohit"
    },
    {
        "email": "aman@gmail.com",
        "password": "456",
        "name": "aman"
    },

]


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

        for user in users:
            if user["email"] == form_email and user["password"] == form_password:
                return redirect(url_for("home", username=user["name"]))
            
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

        new_user = {
            "email": form_email,
            "password": form_password,
            "name": form_username
        }
        users.append(new_user) 
        return redirect(url_for("login"))

     
    else:
        return render_template("register.html")




if __name__=="__main__":
    app.run(debug=True, use_reloader=True)
