from legacy import app
from legacy.categories import CATEGORY_DICT
from legacy.categories import load_saved_visible_categories 

import flask
import simplejson


@app.route('/settings')
def display_settings():
    saved_categories = load_saved_visible_categories()

    return flask.render_template(
        'settings.html',
        saved_categories=saved_categories,
        properties=CATEGORY_DICT,
    )

@app.route('/settings.json', methods=['POST'])
def save_settings():
    response = flask.redirect('/')
    response.set_cookie('categories', simplejson.dumps(flask.request.form))
    return response

