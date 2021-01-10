from flask import Flask, render_template, url_for

app = Flask(__name__)

posts = [
    {
        'author': 'Jože',
        'title': 'What is the infinite sum of natural numbers?',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Janez',
        'title': 'Evaluate an integral to infinity?',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)

@app.route("/login")
def login():
    return render_template("login.html", title="Login")

@app.route("/register")
def register():
    return render_template("register.html", title="Login")


if __name__ == "__main__":
    app.run(debug=True)