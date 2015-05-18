from flask import flash
from flask_wtf import Form
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

DEFAULT_TEMPLATE = """
<div style="display:inline-block">
    <a title="{{ title }}" href="#0.1_">{{ section_num }}</a>
    <ul>
        {% for item in subitems %}
        <li>
            <a title="{{ item.title }}" href="{{ item.html_url }}" target="_blank">{{ item.title }}</a>
        </li>
        {% endfor %}
    </ul>
</div>
"""

class ModuluesForm(Form):
    token = StringField( label='Canvas API Token',
                        validators=[DataRequired()])
    course_id = IntegerField(label='Course ID',
                             validators=[DataRequired()])
    template = TextAreaField(label='Template', default=DEFAULT_TEMPLATE)
    submit = SubmitField(label='Submit')

