from flask import request
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError

from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    about = TextAreaField("Bio", validators=[Length(min=0, max=140)])
    submit = SubmitField("Update profile")

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError("Please use a different username.")


class PitchForm(FlaskForm):
    category = SelectField(
        "Pitch category",
        choices=[
            ("pickup", "Pickup Line"),
            ("interview", "Interview Pitch"),
            ("product", "Product Pitch"),
            ("promotion", "Promotion Pitch"),
        ],
    )
    content = TextAreaField(validators=[DataRequired()])
    submit = SubmitField("Submit")
