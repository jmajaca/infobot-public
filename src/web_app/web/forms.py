from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired


# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
class WatchlistForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    tag = SelectField('Tag:', choices=[''], validators=[DataRequired()])
    url = StringField('URL:', validators=[DataRequired()])
    watch = BooleanField('Watch:', validators=[])
    submit = SubmitField('Add')

    def init_tags(self, tags):
        for tag in tags:
            self.tag.choices.append(tag)
