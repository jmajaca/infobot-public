from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired


# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
class WatchlistForm(FlaskForm):
    id = IntegerField(default=-1)
    name = StringField('Name:', validators=[DataRequired()])
    tag = SelectField('Tag:', choices=[''], validators=[], default='#tinf')
    url = StringField('URL:', validators=[DataRequired()])
    watch = BooleanField('Watch:', validators=[])
    # https://stackoverflow.com/questions/39147578/set-wtforms-submit-button-to-icon
    # submit = SubmitField('Add')

    def init_tags(self, tags):
        for tag in tags:
            self.tag.choices.append(tag)
