from flask import flash
from flask_wtf import Form
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.validators import DataRequired

class ModuluesForm(Form):
    token = StringField( label='Canvas API Token',
                        validators=[DataRequired()])
    course_id = IntegerField(label='Course ID',
                             validators=[DataRequired()])
    top_level_item = TextAreaField(label='Top Level Item HTML')
    sub_item = TextAreaField(label='Sub Item HTML')


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))
