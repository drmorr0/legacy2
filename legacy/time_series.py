
from categories import make_category_select
from categories import SHORT_CATEGORY_DICT
from plot import get_extents
from plot import make_range_slider

from bokeh.layouts import Column 
from bokeh.models import CustomJS
from bokeh.models import Range1d
from bokeh.plotting import Figure

def make_time_series_plot(church_data, prop, *, width=1000, height=600):
    churches = church_data.groupby('church_id')

    plot_bounds = get_extents('year', prop, church_data)
    prop_string = SHORT_CATEGORY_DICT[prop]

    plot = Figure(
        width=width,
        height=height,
        title=prop_string + " over time", 
        x_axis_label='Year', 
        y_axis_label=prop_string,
        x_range=Range1d(**plot_bounds['x_range']),
        y_range=Range1d(**plot_bounds['y_range']),
        tools="save",
        logo=None,
    )

    xvals = [x[1] for x in churches['year']]
    yvals = [y[1] for y in churches[prop]]

    lines = plot.multi_line(
        xvals,
        yvals,
        alpha=0.2,
        hover_alpha=1.0,
        hover_color='orange',
        line_width=1,
    )

    prop_slider = make_range_slider(
        plot_bounds['y_range'], 
        title=prop_string, 
        callback=CustomJS(args={'plot': plot}, code="plot.y_range.end = cb_obj.value;"),
        step=1/100,
    )
    year_slider = make_range_slider(
        plot_bounds['x_range'], 
        title='Years', 
        callback=CustomJS(args={'plot': plot}, code="plot.x_range.end = cb_obj.value;"),
    )

    return Column(
        plot, 
        prop_slider, 
        year_slider,
    )
