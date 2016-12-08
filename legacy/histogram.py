
from categories import make_category_select
from categories import SHORT_CATEGORY_DICT
from plot import get_extents
from plot import make_range_slider

from bokeh.layouts import Column 
from bokeh.layouts import Row
from bokeh.models import ColumnDataSource
from bokeh.models import CustomJS
from bokeh.models import Range1d
from bokeh.models import Slider
from bokeh.plotting import Figure

from copy import copy
import logging
import numpy as np
import json


def _squash_outliers(data, cutoff=2):
    try:
        q1, q3 = np.percentile(data, [25, 75])
        upper_fence = q3 + cutoff * (q3 - q1)
        data[data > upper_fence] = (upper_fence + 1)
        return data
    except IndexError:
        return []


def _remove_nans(data):
    return data[~np.isnan(data)]


def _sanitize(data):
    return _squash_outliers(_remove_nans(data))


def make_histogram_plot(church_data, prop, *, width=1000, height=600):

    plot_bounds = get_extents('year', prop, church_data)
    first_year = plot_bounds['x_range']['start']
    current_year = plot_bounds['x_range']['end']

    yearly_data = {year: _sanitize(copy(church_data.loc[church_data['year'] == year][prop])) 
            for year in range(first_year, current_year + 1)}
    hist_data = {year: np.histogram(data, bins='fd') for year, data in yearly_data.items()}
    hist_bins = {year: list((bins[1:] + bins[:-1]) / 2) for year, (counts, bins) in hist_data.items()}
    hist_counts = {year: list(counts) for year, (counts, bins) in hist_data.items()}

    prop_string = SHORT_CATEGORY_DICT[prop]

    xvals = hist_bins[current_year]
    yvals = hist_counts[current_year]

    if len(xvals) == 1:
        width_array = [1]
    else:
        width_array = [xvals[1]-xvals[0] for x in range(len(xvals))] 

    bar_data = ColumnDataSource(data=dict(
        x=xvals,
        width=width_array,
        top=yvals,
    ))

    plot = Figure(
        width=width,
        height=height,
        title=prop_string + " in " + str(current_year), 
        x_axis_label=prop_string, 
        y_axis_label='Church Count',
        x_range=Range1d(0, max(xvals)),
        y_range=Range1d(0, max(yvals)),
        tools="save",
        logo=None,
    )

    bars = plot.vbar(
        x='x',
        width='width',
        bottom=0,
        top='top',
        source=bar_data,
        alpha=0.2,
        hover_alpha=1.0,
        hover_color='orange',
    )

    year_slider = make_range_slider(
        plot_bounds['x_range'],
        title='Year',
        callback=CustomJS(
            args={'plot': plot, 'bar_data': bar_data}, 
            code=SLIDER_CALLBACK_CODE(hist_bins, hist_counts, prop_string)
        ),
    )

    return Column(
        make_category_select(prop),
        plot, 
        year_slider,
    )


def SLIDER_CALLBACK_CODE(hist_bins, hist_counts, prop_string): 
    return """
        var hist_bins= {hist_bins};
        var hist_counts= {hist_counts};
        var year = cb_obj.value;
        plot.title["text"] = "{prop_string} in " + year;
        plot.x_range.end = Math.max(...hist_bins[year]);
        plot.y_range.end = Math.max(...hist_counts[year]);
        bar_data.data['top'] = hist_counts[year];
        bar_data.data['x'] = hist_bins[year];
        bar_data.data['width'] = Array(hist_bins[year].length).fill(hist_bins[year][1] - hist_bins[year][0]);
        bar_data.trigger('change')
    """.format(
        hist_bins=hist_bins,
        hist_counts=hist_counts,
        prop_string=prop_string,
    )
