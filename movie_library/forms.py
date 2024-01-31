from typing import Any
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, URLField, PasswordField
from wtforms.validators import InputRequired, NumberRange, Email, Length, EqualTo

class MovieForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    director = StringField("Director", validators=[InputRequired()])
    
    year = IntegerField(
                "Year", 
                validators=[
                    InputRequired(), 
                    NumberRange(min=1878, max=2024, message="Please enter a year in format YYYY.")
                ]
            )
    
    submit = SubmitField("Add movie")
    
    
class StringListField(TextAreaField):
    def _value(self):
        if self.data:
            return "\n".join(self.data)
        else:
            return ""

    def process_formdata(self, valuelist):
        # checks valuelist contains at least 1 element, and the first element isn't falsy (i.e. empty string)
        if valuelist and valuelist[0]:
            self.data = [line.strip() for line in valuelist[0].split("\n")]
        else:
            self.data = []


class ExtendedMovieForm(MovieForm):
    cast = StringListField("Cast")
    series = StringListField("Series")
    tags = StringListField("Tags")
    description = TextAreaField("Description")
    video_link = URLField("Video link")
    
    submit = SubmitField("Submit")
    
    
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(), 
            Length(min=4, max=20, message= "Sua senha deve ter entre 4 e 20 caracteres")
        ]
    )
    
    confirm_password = PasswordField(
        "Confirme sua senha",
        validators=[
            InputRequired(),
            EqualTo(
                "password", #nome da primeira variável
                message="Essa senha não corresponde a primeira."
            )
        ]
    )
    
    submit = SubmitField("Registrar")
    

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Senha", validators=[InputRequired()])    
    submit = SubmitField("Login")