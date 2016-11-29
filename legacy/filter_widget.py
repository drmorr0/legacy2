
from bokeh.models import CustomJS
from bokeh.models import Select
from bokeh.layouts import Column

import logging

FILTER_OPTIONS = [
    'None',
    'City',
    'Church',
    'District',
]

DISTRICT_NAMES = {
    'Bay View (defunct)': 5,
    'Delta (defunct)': 10,
    'Fresno (defunct)': 15,
    'Golden Gate (defunct)': 17,
    'San Jose (defunct)': 35,
    'Shasta (defunct)': 40,
    'Bridges': 45,
    'Central Valley': 50,
    'El Camino Real': 55,
    'Great Northern': 60,
}

def _get_city_strings(church_info):
    return ["{city}, {state}".format(city=el[0][0], state=el[0][1]) for el in church_info.groupby(['city', 'state'])]

def validate_filters(church_info, filter_value=None, filter_choice_value=None):
    if filter_choice_value and not filter_value:
        return False

    if filter_value and filter_value not in FILTER_OPTIONS:
        return False

    if filter_choice_value:
        if filter_value == 'District' and filter_choice_value not in DISTRICT_NAMES:
            return False

        if filter_value == 'Church' and filter_choice_value not in list(church_info['name']):
            logging.info(church_info['name'])
            return False

        if filter_value == 'City' and filter_choice_value not in _get_city_strings(church_info):
            return False

    return True

def make_filter_widget(church_info, filter_value, filter_choice_value):

    selected = None
    if filter_value == "None":
        filter_value = None

    category_select_cb = CustomJS(code="reloadWithParams(['filter_by', 'filter_choice'], [cb_obj.value, null])")
    filter_by_selector = Select(
        title="Filter by:",
        options=FILTER_OPTIONS,
        callback=category_select_cb,
        value=filter_value,
    )

    filter_choice_selector = None
    if filter_value:
        if filter_value == 'City':
            filter_choice_options = _get_city_strings(church_info)
        if filter_value == 'Church':
            filter_choice_options = list(church_info['name'])
        if filter_value == 'District':
            filter_choice_options = list(DISTRICT_NAMES.keys())
        filter_choice_options.sort()
        selected = filter_choice_value or filter_choice_options[0]
        filter_choice_cb = CustomJS(code="reloadWithParams('filter_choice', cb_obj.value)")
        filter_choice_selector = Select(
            options=filter_choice_options,
            callback=filter_choice_cb,
            value=filter_choice_value,
        )

    if filter_choice_selector:
        return Column(filter_by_selector, filter_choice_selector), selected
    else:
        return filter_by_selector, selected
