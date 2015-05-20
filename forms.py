from os import getenv as env
from flask import flash
from flask_wtf import Form
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.fields.html5 import URLField
from wtforms.validators import url as url_validator
from wtforms.validators import DataRequired

DEFAULT_TEMPLATE = """
<div class="al-dropdown__container">
    <a class="al-trigger btn btn-small btn-primary" role="button" href="#" title="{{ title }}" href="#">{{ section_num }}</a>
    <ul id="content-1" class="al-options" role="menu" aria-hidden="true" aria-expanded="false">
        {% for item in subitems %}
        <li>
            <a title="{{ item.title }}" href="{{ item.html_url }}">{{ item.title }}</a>
        </li>
        {% endfor %}
    </ul>
</div>
"""

class ModuluesForm(Form):
    canvas_url = URLField(validators=[url_validator()], default=env('CANVAS_URL'))
    token = StringField( label='Canvas API Token',
                        validators=[DataRequired()])
    course_id = IntegerField(label='Course ID',
                             validators=[DataRequired()])
    module_id = IntegerField(label='Module ID')
    template = TextAreaField(label='Template', default=DEFAULT_TEMPLATE)
    submit = SubmitField(label='Submit')

