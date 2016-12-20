
from bokeh.models import Range1d
from bokeh.models import Slider
from bokeh.models import SaveTool
from bokeh.plotting import Figure


PLOT_TYPES = ["Time Series", "Histogram", "Comparison"]


def get_extents(xprop, yprop, church_data):
    return {
        'x_range': (church_data[xprop].min(), church_data[xprop].max()),
        'y_range': (church_data[yprop].min(), church_data[yprop].max()),
    }


def make_plot_object(title, x_axis_label, y_axis_label, plot_bounds, tools=None, width=1000, height=600):
    if not tools: tools = []
    tools.extend(['save'])
    plot = Figure(
        width=width,
        height=height,
        title=title,
        x_axis_label=x_axis_label,
        y_axis_label=y_axis_label,
        x_range=Range1d(plot_bounds['x_range'][0], plot_bounds['x_range'][1]),
        y_range=Range1d(plot_bounds['y_range'][0], plot_bounds['y_range'][1]),
        tools=tools,
        logo=None,
    )

    return plot

