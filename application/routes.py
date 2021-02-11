from flask import render_template, url_for, flash, redirect, request, abort
from application import app, db, bcrypt
from application.forms import RegistrationForm, LoginForm, UpdateProfileForm, QuestionForm, AnswerForm
from application.models import User, Question, Answer
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get("page", default=1, type=int)
    questions = Question.query.order_by(Question.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", questions=questions)

@app.route("/home/most_viewed")
def most_viewed():
    page = request.args.get("page", default=1, type=int)
    questions = Question.query.order_by(Question.views.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", questions=questions)

@app.route("/home/most_answered")
def most_answered():
    page = request.args.get("page", default=1, type=int)
    questions = Question.query.order_by(Question.num_answers.desc()).paginate(page=page, per_page=5)
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
            flash('Username or password are incorrect.', 'danger')
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
    user = User.query.filter_by(username=current_user).first_or_404()
    questions = Question.query.filter_by(author=user)
    return render_template('profile.html', title='Profile', questions=questions, user=user)

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

@app.route("/question/<int:question_id>", methods=['GET', 'POST'])
def question_post(question_id):
    question = Question.query.get_or_404(question_id)
    page = request.args.get("page", default=1, type=int)
    answers = Answer.query.filter_by(question_id=question.id).order_by(Answer.date_posted.desc()).paginate(page=page, per_page=3)
    question.views += 1
    db.session.commit()
    form = AnswerForm()
    if form.validate_on_submit():
        answer = Answer(answer=form.answer.data, question_id=question.id, author=current_user)
        db.session.add(answer)
        question.num_answers += 1
        db.session.commit()
        flash('You have answered a question!', 'success')
        return redirect(request.url)
    return render_template('question.html', title="Question", question=question, form=form, answers=answers)

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
        return redirect(url_for('new_question', question_id=question_id))
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

@app.route("/question/<int:question_id>/edit_comment/<int:answer_id>", methods=["GET", "POST"])
@login_required
def edit_answer(question_id, answer_id):
    question = Question.query.get_or_404(question_id)
    answer = Answer.query.get_or_404(answer_id)
    if answer.author != current_user:
        abort(403)
    form = AnswerForm()
    if form.validate_on_submit():
        answer.answer = form.answer.data
        db.session.commit()
        flash('Your answer has been updated!', 'success')
        return redirect(url_for('question_post', question_id=question_id))
    elif request.method == 'GET':
        form.answer.data = answer.answer
    return render_template("edit_answer.html", title="Edit answer", form=form, question=question)

@app.route("/question/<int:question_id>/delete/<int:answer_id>", methods=['POST'])
@login_required
def delete_answer(question_id, answer_id):
    question = Question.query.get_or_404(question_id)
    answer = Answer.query.get_or_404(answer_id)
    if answer.author != current_user:
        abort(403)
    db.session.delete(answer)
    question.num_answers -= 1
    db.session.commit()
    flash('Your answer has been deleted!', 'success')
    return redirect(url_for('question_post', question_id=question_id))

@app.route("/user/<string:username>")
def user_profile(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    questions = Question.query.filter_by(author=user).order_by(Question.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('profile.html', questions=questions, user=user)
