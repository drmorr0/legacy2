
from categories import make_category_select
from categories import SHORT_CATEGORY_DICT
from filter_widget import make_filter_widget
from sql import run_query

from bokeh.layouts import Column 
from bokeh.layouts import Row
from bokeh.models import CustomJS
from bokeh.models import Range1d
from bokeh.models import Slider
from bokeh.plotting import Figure

def make_comparison_plot(conn, props, filter_value, selected, *, width=1000, height=600):
    if len(props) > 2:
        logging.warning("Comparison query provided more than 2 properties, ignoring the rest")
        props = props[:2]

    church_data = run_query(conn, props, filter_value, selected)
    churches = church_data.groupby('church_id')

    min_prop0 = church_data[props[0]].min()
    max_prop0 = church_data[props[0]].max()
    min_prop1 = church_data[props[1]].min()
    max_prop1 = church_data[props[1]].max()
    prop0_string = SHORT_CATEGORY_DICT[props[0]]
    prop1_string = SHORT_CATEGORY_DICT[props[1]]

    plot = Figure(
        width=width,
        height=height,
        title=prop0_string + " vs. " + prop1_string,
        x_axis_label=prop0_string,
        y_axis_label=prop1_string,
        x_range=Range1d(min_prop0, max_prop0),
        y_range=Range1d(min_prop1, max_prop1),
        tools="save",
        logo=None,
    )

    xvals = [x[1] for x in churches[props[0]]]
    yvals = [y[1] for y in churches[props[1]]]

    lines = plot.multi_line(
        xvals,
        yvals,
        alpha=0.2,
        hover_alpha=1.0,
        hover_color='orange',
        line_width=1,
    )

    prop0_range_callback = CustomJS(args={'plot': plot}, code="plot.x_range.end = cb_obj.value;")
    prop0_slider = Slider(
        start=min_prop0+1, 
        end=max_prop0, 
        value=max_prop0, 
        step=(max_prop0-min_prop0)/100,
        title=prop0_string,
        callback=prop0_range_callback,
    )

    prop1_range_callback = CustomJS(args={'plot': plot}, code="plot.y_range.end = cb_obj.value;")
    prop1_slider = Slider(
        start=min_prop1+1, 
        end=max_prop1, 
        value=max_prop1, 
        step=(max_prop1-min_prop1)/100, 
        title=prop1_string,
        callback=prop1_range_callback,
    )

    return Column(
        plot, 
        prop0_slider, 
        prop1_slider,
    )
