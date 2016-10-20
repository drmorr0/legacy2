from categories import SHORT_CATEGORY_DICT
from categories import make_category_select
from filter_widget import make_filter_widget
from filter_widget import validate_filters
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

def error_request(msg):
    curdoc().add_root(Div(text="<h1>Error</h1>%s" % msg))
    curdoc().session_context.request.arguments = ''

def handle_request():
    global prop, filter_value, filter_choice_value

    request = curdoc().session_context.request
    if request:
        args = request.arguments
        if 'prop' in args: prop = args.get('prop')[0].decode('UTF-8') 
        if 'filter_by' in args: filter_value = args.get('filter_by')[0].decode('UTF-8')
        if 'filter_choice' in args: filter_choice_value = args.get('filter_choice')[0].decode('UTF-8')

    conn = sql.connect('static/legacy.db')
    church_info = pd.read_sql("select * from churches", conn)

    if not validate_filters(church_info, filter_value, filter_choice_value):
        error_request("Invalid filter parameters %s %s" % (filter_value, filter_choice_value))
        return

    filter_widget, selected = make_filter_widget(church_info, filter_value, filter_choice_value)

    if prop not in SHORT_CATEGORY_DICT.keys():
        error_request("Invalid property %s" % prop)
        return

    query = "select church_id, year, %s from church_data" % prop
    if filter_value == 'District':
        if not filter_choice_value:
            filter_choice_value = str(selected)
        query += ', churches where church_data.church_id = churches.id and churches.district == %s' % filter_choice_value

    logging.debug(query)
    church_data = pd.read_sql(query, conn).sort_values('year')
    curdoc().add_root(Column(
        make_category_select(prop), 
        filter_widget,
        make_time_series_plot(church_data, prop)
    ))

handle_request()
