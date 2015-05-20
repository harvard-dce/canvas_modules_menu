import jinja2
from urlparse import urlparse, urlunparse
from unipath import Path
from os import getenv as env
from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension

from forms import ModuluesForm
from canvas import CanvasApi, UnauthorizedError, NotFoundError

import dotenv
dotenv.load_dotenv(Path(__file__).parent.child('.env'))

app = Flask(__name__)
Bootstrap(app)

app.debug = bool(env('FLASK_DEBUG'))
app.config['SECRET_KEY'] = env('SECRET_KEY')

toolbar = DebugToolbarExtension(app)

@app.route('/', methods=['GET','POST'])
def index():
    form = ModuluesForm()
    context = {'form': form}
    if form.is_submitted():
        if form.validate():
            canvas = CanvasApi(form.canvas_url.data, form.token.data)
            try:
                module_data = canvas.get_modules(form.course_id.data)
                context['html'] = generate_html(form, module_data)
            except UnauthorizedError, e:
                flash("Unauthorized error. Check your token? %s", str(e))
            except NotFoundError, e:
                flash("Module/course content not found: %s" % str(e))
            except:
                raise
    return render_template('index.html', **context)

def render_section(template, section):
    section['section_num'] = section['title'].split()[0]
    return template.render(**section)

def generate_html(form, data):
    html = ""
    current_section = None
    t = jinja2.Template(form.template.data)
    for item in data:

        # skip unpublished
        if not item['published']:
            continue

        # convert to relative urls
        for key in ['html_url', 'url']:
            url_parts = urlparse(item[key])
            item[key] = url_parts.path

        if item['indent']:
            current_section['subitems'].append(item.copy())
        else:
            if current_section and current_section['id'] != item['id']:
                # render the section/items
                html += render_section(t, current_section) + "\n\n"
            current_section = item.copy()
            current_section['subitems'] = [item.copy()]

    html += render_section(t, current_section) + "\n\n"
    return html

if __name__ == '__main__':
    app.run(
        host=env('FLASK_HOST', '127.0.0.1'),
        port=int(env('FLASK_PORT', 5000))
    )
