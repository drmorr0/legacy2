from categories import SHORT_CATEGORY_DICT
from categories import make_category_select
from categories import make_plot_type_buttons
from categories import PLOT_TYPES
from filter_widget import make_filter_widget
from filter_widget import validate_filters
from filter_widget import DISTRICT_NAMES
from histogram import make_histogram_plot
from time_series import make_time_series_plot

import logging
import pandas as pd
import sqlite3 as sql
import sys

from bokeh.models import Div
from bokeh.models import Row
from bokeh.models import Column 
from bokeh.plotting import curdoc
from bokeh.settings import settings

# defaults
prop = 'MEMBTOT'
filter_value = None
filter_choice_value = None
plot_type = 'Time Series'


class RequestError(Exception):
    pass


def error_request(msg):
    curdoc().add_root(Div(text="<h1>Error</h1>%s" % msg))
    raise RequestError(msg)


def parse_args():
    global prop, filter_value, filter_choice_value, plot_type

    request = curdoc().session_context.request
    if request:
        args = request.arguments
        if 'prop' in args: prop = args.get('prop')[0].decode('UTF-8') 
        if 'filter_by' in args: filter_value = args.get('filter_by')[0].decode('UTF-8')
        if 'filter_choice' in args: filter_choice_value = args.get('filter_choice')[0].decode('UTF-8')
        if 'plot_type' in args: plot_type = args.get('plot_type')[0].decode('UTF-8')
    if 'filter_by' == 'None': filter_by = None


def run_query(conn, prop, filter_value, selected):
    query = "select church_id, year, %s from church_data" % prop
    logging.info(selected)
    if filter_value:
        query += ", churches where church_data.church_id=churches.id "
        if filter_value == 'City':
            logging.info(selected)
            city, state = selected.split(",", 2)
            query += ' and churches.city="%s"' % city
        if filter_value == 'Church':
            query += ' and churches.name="%s"' % selected
        elif filter_value == 'District':
            query += ' and churches.district="%d"' % DISTRICT_NAMES[selected]

    logging.debug(query)
    return pd.read_sql(query, conn).sort_values('year')


def handle_request():
    global prop, filter_value, filter_choice_value, plot_type

    parse_args()
    conn = sql.connect('static/legacy.db')
    church_info = pd.read_sql("select * from churches", conn)

    if not validate_filters(church_info, filter_value, filter_choice_value):
        error_request("Invalid filter parameters %s %s" % (filter_value, filter_choice_value))
    filter_widget, selected = make_filter_widget(church_info, filter_value, filter_choice_value)

    if prop not in SHORT_CATEGORY_DICT.keys():
        error_request("Invalid property %s" % prop)

    if plot_type not in PLOT_TYPES:
        error_request("Invalid plot type %s" % plot_type)

    church_data = run_query(conn, prop, filter_value, selected)
    if plot_type == "Time Series":
        plot = make_time_series_plot(church_data, prop)
    elif plot_type == "Histogram":
        plot = make_histogram_plot(church_data, prop)

    curdoc().add_root(Column(
        make_plot_type_buttons(plot_type), 
        make_category_select(prop),
        filter_widget,
        plot,
    ))

try:
    handle_request()
except Exception:
    curdoc().session_context.request.arguments = ''
    raise
