from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import InputRequired, NumberRange

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