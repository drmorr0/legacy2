from legacy import app
from legacy.categories import CATEGORY_DICT

import flask
import sqlite3 as sql
import pandas as pd

def load_church_data(conn, church_id):
    query =  "select * from church_data, churches "
    query += "where church_data.church_id={church_id} and churches.id={church_id}".format(church_id=church_id)
    print(query)
    return pd.read_sql(query, conn).sort_values('year').set_index('year')

@app.route('/church/<int:church_id>')
def display_church(church_id):
    conn = sql.connect(app.config['DB_LOCATION'])
    church_data = load_church_data(conn, church_id)
    
    return flask.render_template(
        'church.html',
        church_name=church_data['name'].iloc[-1],
        church_data=church_data,
        properties=CATEGORY_DICT,
    )
