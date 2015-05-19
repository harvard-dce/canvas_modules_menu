# Canvas Course Modules Menu Generator

Simple flask app as a throw-away, 1st iteration. Based on a course id and a snippet of template, generates an html menu for copy/pasting into a course page.

Could evolve into an evenutal LTI tool.

### .env vars

* SECRET_KEY (required)
* CANVAS_URL (required)
* FLASK_DEBUG
* FLASK_HOST
* FLASK_PORT

### getting, running

1. git clone
1. `pip install -r requirements.txt`
1. `foreman start`
1. visit `http://localhost:5000/`
