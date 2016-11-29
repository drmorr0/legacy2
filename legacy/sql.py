
import pandas as pd
import logging

def run_query(conn, props, filter_value, selected):
    query = "select church_id, year"
    for prop in props:
        if prop.lower() == 'year':
            continue
        query += ", {prop}".format(prop=prop)
    query += " from church_data"
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
