from categories import SHORT_CATEGORY_DICT
from plot import PLOT_TYPES

from bokeh.models import CustomJS
from bokeh.models import RadioButtonGroup
from bokeh.models import Select
from bokeh.models import Slider


def make_range_slider(rng, title, callback, step=1):
    if step < 0:
        raise ValueError("Invalid setting for step: {step}".format(step=step))
    elif step < 1:
        step *= (rng[1] - rng[0])
        
    return Slider(
        start=rng[0]+1, 
        end=rng[1], 
        value=rng[1], 
        step=step,
        title=title,
        callback=callback,
    )


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

