
from bokeh.models import CustomJS
from bokeh.models import Select

SHORT_CATEGORY_DICT = {
    "MEMBTOT": "Total Membership",
    "AVATTWOR": "Average Worship Attendance",
}


def make_category_select(selected_prop):

    category_select_cb = CustomJS(code=
    """
        var url = window.location.href.split('?')[0];
        window.location.href = url + "?prop=" + cb_obj.value
    """
    )

    return Select(
        title="Choose a category...", 
        options=list(SHORT_CATEGORY_DICT.items()), 
        callback=category_select_cb,
        value=selected_prop,
    )
