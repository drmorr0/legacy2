from categories import SHORT_CATEGORY_DICT
from time_series import make_time_series_plot

import pandas as pd
import sqlite3 as sql
import sys

from bokeh.models import Div
from bokeh.models import Row
from bokeh.plotting import curdoc

def handle_request():
    args = curdoc().session_context.request.arguments
    try:
        prop = args.get('prop')[0].decode('UTF-8')
    except:
        prop = 'MEMBTOT'

    if prop not in SHORT_CATEGORY_DICT.keys():
        curdoc().add_root(Div(text="<h1>Error</h1>Invalid user parameter %s" % prop))
        curdoc().session_context.request.arguments = ''
        return

    conn = sql.connect('static/legacy.db')
    query = "select church_id, year, %s from church_data" % prop
    church_data = pd.read_sql(query, conn).sort_values('year')
    curdoc().add_root(make_time_series_plot(church_data, prop))

handle_request()
