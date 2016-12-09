import logging

from controls import make_range_slider
from controls import make_category_select
from categories import SHORT_CATEGORY_DICT
from plot import get_extents
from plot import make_plot_object

from bokeh.layouts import Column 
from bokeh.models import CustomJS

def make_comparison_plot(church_data, props):
    if len(props) > 2:
        logging.warning("Comparison query provided more than 2 properties, ignoring the rest")
        props = props[:2]

    churches = church_data.groupby('church_id')

    plot_bounds = get_extents(props[0], props[1], church_data)
    prop0_string = SHORT_CATEGORY_DICT[props[0]]
    prop1_string = SHORT_CATEGORY_DICT[props[1]]

    plot = make_plot_object(
        title=prop0_string + ' vs. ' + prop1_string,
        x_axis_label=prop0_string,
        y_axis_label=prop1_string,
        plot_bounds=plot_bounds,
    )

    xvals = [x[1].iloc[-1] for x in churches[props[0]]]
    yvals = [y[1].iloc[-1] for y in churches[props[1]]]

    points = plot.circle(
        x=xvals,
        y=yvals,
        size=10,
        alpha=0.2,
        hover_alpha=1.0,
        hover_color='orange',
        line_width=1,
    )

    prop0_slider = make_range_slider(
        plot_bounds['x_range'],
        title=prop0_string,
        step=1/100,
        callback=CustomJS(args={'plot': plot}, code="plot.x_range.end = cb_obj.value;"),
    )

    prop1_slider = make_range_slider(
        plot_bounds['y_range'],
        title=prop1_string,
        step=1/100,
        callback=CustomJS(args={'plot': plot}, code="plot.y_range.end = cb_obj.value;"),
    )
        
    return Column(
        plot, 
        prop0_slider, 
        prop1_slider,
    )
