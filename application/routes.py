from flask import render_template, url_for, flash, redirect, request, abort
from application import app, db, bcrypt
from application.forms import RegistrationForm, LoginForm, UpdateProfileForm, QuestionForm
from application.models import User, Question
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    questions = Question.query.all()
    return render_template("home.html", questions=questions)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Something went wrong. Please try again.', 'danger')
    return render_template("login.html", title="Login", form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! Please Log In', 'success')
        return redirect(url_for('home'))
    return render_template("register.html", title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/profile")
@login_required
def profile():
    questions = Question.query.filter_by(author=current_user)
    return render_template('profile.html', title='Profile', questions=questions)

@app.route("/edit_profile", methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.description = form.description.data
        if form.description.data == "":
            current_user.description = "No description yet."
        db.session.commit()
        flash('Your account information has been updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.description.data = current_user.description
    return render_template('edit_profile.html', title='Edit-profile', form=form)

@app.route("/question/new", methods=['GET', 'POST'])
@login_required
def new_question():
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(question)
        db.session.commit()
        flash('Your questions has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_question.html', title='New Question',
                           form=form, legend='New Question')

@app.route("/question/<int:question_id>")
def question_post(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('question.html', title="Question", question=question)

@app.route("/question/<int:question_id>/update", methods=['GET', 'POST'])
@login_required
def update_question(question_id):
    question = Question.query.get_or_404(question_id)
    if question.author != current_user:
        abort(403)
    form = QuestionForm()
    if form.validate_on_submit():
        question.title = form.title.data
        question.content = form.content.data
        db.session.commit()
        flash('Your question has been updated!', 'success')
        return redirect(url_for('question', question_id=question_id))
    elif request.method == 'GET':
        form.title.data = question.title
        form.content.data = question.content
    return render_template('create_question.html', title='Update Question',
                           form=form, legend='Update Question')

@app.route("/question/<int:question_id>/delete", methods=['POST'])
@login_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    if question.author != current_user:
        abort(403)
    db.session.delete(question)
    db.session.commit()
    flash('Your question has been deleted!', 'success')
    return redirect(url_for('home'))