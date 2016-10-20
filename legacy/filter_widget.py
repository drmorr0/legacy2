
from bokeh.models import CustomJS
from bokeh.models import Select
from bokeh.layouts import Row

FILTER_OPTIONS = [
    'None',
    'City',
    'Church',
    'District',
]

_DISTRICT_NAMES = {
     "5": 'Bay View (defunct)',
    "10": 'Delta (defunct)',
    "15": 'Fresno (defunct)',
    "17": 'Golden Gate (defunct)',
    "35": 'San Jose (defunct)',
    "40": 'Shasta (defunct)',
    "45": 'Bridges',
    "50": 'Central Valley',
    "55": 'El Camino Real',
    "60": 'Great Northern',
}

def _get_city_strings(church_info):
    return ["{city}, {state}".format(city=el[0][0], state=el[0][1]) for el in church_info.groupby(['city', 'state'])]

def validate_filters(church_info, filter_value=None, filter_choice_value=None):
    if filter_choice_value and not filter_value:
        return False

    if filter_value and filter_value not in FILTER_OPTIONS:
        return False

    if filter_choice_value:
        if filter_value == 'District' and filter_choice_value not in _DISTRICT_NAMES:
            return False

        if filter_value == 'Church' and filter_choice_value not in church_info['name']:
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
            filter_choice_options = list(_DISTRICT_NAMES.items())
        filter_choice_options.sort()
        selected = filter_choice_options[0][0]
        filter_choice_cb = CustomJS(code="reloadWithParams('filter_choice', cb_obj.value)")
        filter_choice_selector = Select(
            options=filter_choice_options,
            callback=filter_choice_cb,
            value=filter_choice_value,
        )

    if filter_choice_selector:
        return Row(filter_by_selector, filter_choice_selector), selected
    else:
        return filter_by_selector, selected
