
from categories import make_category_select
from categories import SHORT_CATEGORY_DICT

from bokeh.layouts import column 
from bokeh.models import CustomJS
from bokeh.models import Range1d
from bokeh.models import Slider
from bokeh.plotting import Figure

def make_time_series_plot(church_data, prop, *, width=1000, height=600):
    churches = church_data.groupby('church_id')

    min_year = church_data['year'].min()
    max_year = church_data['year'].max()
    min_prop = 0
    max_prop = church_data[prop].max()

    plot = Figure(
        width=width,
        height=height,
        title=prop, 
        x_axis_label='Year', 
        y_axis_label=SHORT_CATEGORY_DICT[prop],
        x_range=Range1d(min_year, max_year),
        y_range=Range1d(min_prop, max_prop),
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

    prop_range_callback = CustomJS(args={'plot': plot}, code="plot.y_range.end = cb_obj.value;")
    prop_slider = Slider(
        start=min_prop+1, 
        end=max_prop, 
        value=max_prop, 
        step=(max_prop-min_prop)/100, 
        title=SHORT_CATEGORY_DICT[prop],
        callback=prop_range_callback,
    )

    year_range_callback = CustomJS(args={'plot': plot}, code="plot.x_range.end = cb_obj.value;")
    year_slider = Slider(
        start=min_year+1, 
        end=max_year, 
        value=max_year, 
        step=1,
        title='Years',
        callback=year_range_callback,
    )

    return column(make_category_select(prop), plot, prop_slider, year_slider)
