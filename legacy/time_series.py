import logging

from controls import make_category_select
from controls import make_range_slider
from categories import SHORT_CATEGORY_DICT
from plot import get_extents
from plot import make_plot_object

from bokeh.layouts import Column 
from bokeh.models import ColumnDataSource
from bokeh.models import CustomJS
from bokeh.models import HoverTool


def make_time_series_hover():
    return HoverTool(
        tooltips="""
        <div>@church_name</div>
        """
    )


def make_time_series_plot(church_data, prop):
    churches = church_data.groupby('church_id')

    plot_bounds = get_extents('year', prop, church_data)
    prop_string = SHORT_CATEGORY_DICT[prop]

    plot = make_plot_object(
        title=prop_string + " over time", 
        x_axis_label='Year', 
        y_axis_label=prop_string,
        plot_bounds=plot_bounds,
        tools=[make_time_series_hover()],
    )

    time_series_data = ColumnDataSource(data=dict(
        x=[x[1] for x in churches['year']],
        y=[y[1] for y in churches[prop]],
        church_name=[church[1]['name'].iloc[-1] for church in churches],
    ))

    lines = plot.multi_line(
        xs='x',
        ys='y',
        source=time_series_data, 
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
