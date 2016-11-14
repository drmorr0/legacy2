
from categories import SHORT_CATEGORY_DICT

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


FIRST_YEAR = 2014
CURRENT_YEAR = 2015


def _squash_outliers(data, cutoff=2):
    q1, q3 = np.percentile(data, [25, 75])
    upper_fence = q3 + cutoff * (q3 - q1)
    data[data > upper_fence] = (upper_fence + 1)
    return data


def make_histogram_plot(church_data, prop, *, width=1000, height=600):

    yearly_data = {year: _squash_outliers(copy(church_data.loc[church_data['year'] == year][prop])) 
            for year in range(FIRST_YEAR, CURRENT_YEAR + 1)}
    hist_data = {year: np.histogram(data, bins='fd') for year, data in yearly_data.items()}
    hist_bins = {year: list((bins[1:] + bins[:-1]) / 2) for year, (counts, bins) in hist_data.items()}
    hist_counts = {year: list(counts) for year, (counts, bins) in hist_data.items()}

    prop_string = SHORT_CATEGORY_DICT[prop]

    xvals = hist_bins[CURRENT_YEAR]
    yvals = hist_counts[CURRENT_YEAR]

    bar_data = ColumnDataSource(data=dict(
        x=xvals,
        width=[xvals[1]-xvals[0] for x in range(len(xvals))], 
        top=yvals,
    ))

    plot = Figure(
        width=width,
        height=height,
        title=prop_string + " in " + str(CURRENT_YEAR), 
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

    callback_code = """
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

    year_range_callback = CustomJS(args={'plot': plot, 'bar_data': bar_data}, code=callback_code)
    year_slider = Slider(
        start=FIRST_YEAR,
        end=CURRENT_YEAR,
        value=CURRENT_YEAR,
        step=1,
        title='Year',
        callback=year_range_callback,
    )

    return Column(
        plot, 
        year_slider,
    )
