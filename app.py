import json
from unipath import Path
from os import getenv as env
from flask import Flask, request, render_template, flash
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension

from forms import ModuluesForm, flash_errors
from canvas import CanvasApi

import dotenv
dotenv.load_dotenv(Path(__file__).parent.child('.env'))

app = Flask(__name__)
Bootstrap(app)

app.debug = True
app.config['SECRET_KEY'] = env('SECRET_KEY')

toolbar = DebugToolbarExtension(app)

@app.route('/', methods=['GET','POST'])
def index():
    form = ModuluesForm()
    context = {'form': form}
    if form.is_submitted():
        if form.validate():
            canvas = CanvasApi(env('CANVAS_URL'), form.token.data)
            try:
                module_data = canvas.get_modules(form.course_id.data)
                context['module_data'] = module_data
            except:
                raise
        else:
            flash_errors(form)
    return render_template('index.html', **context)

if __name__ == '__main__':
    app.run()
