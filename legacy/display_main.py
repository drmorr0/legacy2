from legacy import app
from legacy.categories import is_valid_category
from legacy.categories import load_saved_visible_categories 
from legacy.categories import set_category_visibility
from legacy.categories import get_category_string
from legacy.comparison import make_comparison_plot
from legacy.controls import make_plot_type_buttons
from legacy.filter_widget import make_filter_widget
from legacy.filter_widget import validate_filters
from legacy.filter_widget import DISTRICT_NAMES
from legacy.histogram import make_histogram_plot
from legacy.plot import PLOT_TYPES
from legacy.time_series import make_time_series_plot

import flask
import logging
import sqlite3 as sql
import pandas as pd

from bokeh.embed import components
from bokeh.models import Div
from bokeh.models import Row
from bokeh.models import Column 
from bokeh.plotting import curdoc
from bokeh.themes import Theme

class LegacyException(Exception):
    pass


def parse_args():
    args = dict(flask.request.args)
    args.setdefault('properties', ['MEMBTOT', 'AVATTWOR']),
    args.setdefault('filter_by', [None]),
    args.setdefault('filter_choice', [None]),
    args.setdefault('plot_type', ['Time Series']),

    # This is a little hack-y, but oh well
    if len(args['properties']) < 2 and args['plot_type'] == ['Comparison']:
        print("Not enough properties, displaying MEMBTOT")
        args['properties'].append('MEMBTOT')

    return args


def load_churches_data(conn, props, filter_value, selected):
    query = "select church_id, year, name"
    for prop in set(props):
        if prop.lower() == 'year':
            continue
        query += ", {prop}".format(prop=prop)
    query += " from church_data, churches where church_data.church_id=churches.id "
    if filter_value:
        if filter_value == 'City':
            logging.info(selected)
            city, state = selected.split(",", 2)
            query += ' and churches.city="%s"' % city
        if filter_value == 'Church':
            query += ' and churches.name="%s"' % selected
        elif filter_value == 'District':
            query += ' and churches.district="%d"' % DISTRICT_NAMES[selected]

    print(query)
    return pd.read_sql(query, conn).sort_values('year').fillna(0)


@app.route("/")
def plot_church_data():

    args = parse_args()
    load_saved_visible_categories()

    conn = sql.connect(app.config['DB_LOCATION'])
    church_info = pd.read_sql("select * from churches", conn)

    if not validate_filters(church_info, args['filter_by'][0], args['filter_choice'][0]):
        raise LegacyException("Invalid filter parameters %s %s" % (args['filter_by'][0], args['filter_choice'][0]))
    filter_widget, selected = make_filter_widget(church_info, args['filter_by'][0], args['filter_choice'][0])

    for prop in args['properties']:
        if not is_valid_category(prop):
            raise LegacyException("Invalid property %s" % prop)
        set_category_visibility(prop)

    if args['plot_type'][0] not in PLOT_TYPES:
        raise LegacyException("Invalid plot type %s" % args['plot_type'][0])

    if args['plot_type'][0] == "Time Series":
        church_data = load_churches_data(conn, args['properties'][:1], args['filter_by'][0], selected)
        plot = make_time_series_plot(church_data, args['properties'][0])
    elif args['plot_type'][0] == "Histogram":
        church_data = load_churches_data(conn, args['properties'][:1], args['filter_by'][0], selected)
        plot = make_histogram_plot(church_data, args['properties'][0])
    elif args['plot_type'][0] == "Comparison":
        church_data = load_churches_data(conn, args['properties'], args['filter_by'][0], selected)
        plot = make_comparison_plot(church_data, args['properties'])

    plot_app = Column(
        make_plot_type_buttons(args['plot_type'][0]), 
        Row(plot, filter_widget),
    )

    script, div = components(plot_app)

    html = flask.render_template(
        'index.html',
        plot_script=script,
        plot_div=div,
        **args
    )

    return html
