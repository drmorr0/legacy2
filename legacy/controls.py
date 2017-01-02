from legacy.categories import get_visible_category_strings
from legacy.plot import PLOT_TYPES

from bokeh.models import CustomJS
from bokeh.models import RadioButtonGroup
from bokeh.models import Row
from bokeh.models import Select
from bokeh.models import Slider


def make_range_slider(rng, title, callback, step=1):
    if step < 0:
        raise ValueError("Invalid setting for step: {step}".format(step=step))
    elif step < 1:
        step *= (rng[1] - rng[0])
        
    return Slider(
        start=rng[0], 
        end=rng[1], 
        value=rng[1], 
        step=step,
        title=title,
        callback=callback,
    )


def make_category_select(selected_props):
    selected_props = selected_props if isinstance(selected_props, list) else [selected_props]
    children = []
    for cb_index, prop in enumerate(selected_props):
        cb_values = ['"{prop}"'.format(prop=prop) for prop in selected_props]
        cb_values[cb_index] = 'cb_obj.value'
        cb_string = '[' + ','.join(cb_values) + ']'

        children.append(Select(
            title="Choose a category...", 
            options=list(get_visible_category_strings()), 
            callback=CustomJS(code="reloadWithParams('properties', %s)" % cb_string),
            value=prop,
        ))
    return Row(children=children)


def make_plot_type_buttons(plot_type):
    return RadioButtonGroup(
        labels=PLOT_TYPES,
        active=PLOT_TYPES.index(plot_type),
        callback=CustomJS(code="reloadWithParams('plot_type', cb_obj.labels[cb_obj.active])"),
    )
