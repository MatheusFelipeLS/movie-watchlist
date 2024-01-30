from typing import Any
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, URLField
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
    
    
class StringListField(TextAreaField):
    def _value(self):
        if self.data:
            return '\n'.join(self.data)
        else:
            return ""
    
    
    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            self.data = [line.strip() for line in valuelist[0].split('\n')]
        else:
            self.data = []


class ExtendedMovieForm(MovieForm):
    cast = StringListField("Cast")
    series = StringListField("Series")
    tags = StringListField("Tags")
    description = TextAreaField("Description")
    video_link = URLField("Video link")
    
    submit = SubmitField("Submit")