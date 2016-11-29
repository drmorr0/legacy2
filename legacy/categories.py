
from bokeh.models import CustomJS
from bokeh.models import Select
from bokeh.models import RadioButtonGroup

SHORT_CATEGORY_DICT = {
    "year": "Year",
    "MEMBTOT": "Total Membership",
    "AVATTWOR": "Average Worship Attendance",
}


PLOT_TYPES = ["Time Series", "Histogram", "Comparison"]


def make_category_select(selected_prop):

    return Select(
        title="Choose a category...", 
        options=list(SHORT_CATEGORY_DICT.items()), 
        callback=CustomJS(code="reloadWithParams('prop', cb_obj.value)"),
        value=selected_prop,
    )


def make_plot_type_buttons(plot_type):

    return RadioButtonGroup(
        labels=PLOT_TYPES,
        active=PLOT_TYPES.index(plot_type),
        callback=CustomJS(code="reloadWithParams('plot_type', cb_obj.labels[cb_obj.active])"),
    )

