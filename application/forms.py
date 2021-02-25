from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import (StringField, PasswordField, SubmitField,
                     BooleanField, ValidationError)
from wtforms.widgets import TextArea
from wtforms.validators import Length, InputRequired, Email, EqualTo
from application.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[
            InputRequired(),
            Length(min=2, max=15,
                   message=("Username has to be between ",
                            "2 and 15 characters long"))
        ]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField(
        "Password", validators=[
            InputRequired(),
            Length(min=5, max=20,
                   message="Password must be between 2 and 20 characters long")
        ]
    )
    confirm_password = PasswordField(
        "Confirm password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is already taken.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is already taken.")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateProfileForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=2, max=15)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    description = StringField("Description", widget=TextArea())
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("That username is taken.")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("That email is taken.")


class QuestionForm(FlaskForm):
    title = StringField(
        "Title", validators=[
            InputRequired(),
            Length(min=3, max=100,
                   message="Question can be a maximum of 50 characters long")
        ],
        description="test"
    )
    content = StringField(
        "Body", validators=[InputRequired()], widget=TextArea()
    )
    submit = SubmitField("Ask your question")


class AnswerForm(FlaskForm):
    answer = StringField(
        "Your answer", validators=[InputRequired()], widget=TextArea()
    )
    submit = SubmitField("Post your answer")
