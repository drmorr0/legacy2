
from bokeh.models import CustomJS
from bokeh.models import Select
from bokeh.layouts import Row

FILTER_OPTIONS = [
    'None',
    'City',
    'Church',
    'District',
]

def make_filter_widget(cities, church_names, districts):

    filter_choice_selector = Select(id='filter_choice_selector')

    category_select_cb = CustomJS(args={'cities': cities, 'churches': church_names, 'districts': disctrics, code=
    """
        if (cb_obj.value == "None")
            $('#modelid_filter_choice_selector').css('visibility', 'hidden');
        else $('#modelid_filter_choice_selector').css('visibility', 'visible');
    """
    )

    filter_by_selector = Select(
        title="Filter by:",
        options=FILTER_OPTIONS,
        callback=category_select_cb,
    )


    return Row(filter_by_selector, filter_choice_selector)




