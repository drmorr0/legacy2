import logging

from legacy.controls import make_range_slider
from legacy.controls import make_category_select
from legacy.categories import SHORT_CATEGORY_DICT
from legacy.plot import get_extents
from legacy.plot import make_plot_object

from bokeh.layouts import Column 
from bokeh.models import ColumnDataSource
from bokeh.models import CustomJS
from bokeh.models import HoverTool
from bokeh.models import TapTool

from copy import copy
import numpy as np


def _make_histogram_tools(data_source, prop_string):
    return [
        HoverTool(
            tooltips="""
                <div>@top churches between @left and @right</div>
            """,
        ),
        TapTool(
            callback=CustomJS(
                args={'data_source':data_source},
                code="""populateDetailsColumns("{prop}", data_source.selected['1d']['indices'], cb_obj.data)""".format(
                    prop=prop_string,
                ),
            ),
        ),
    ]


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


def make_histogram_plot(church_data, prop):

    plot_bounds = get_extents('year', prop, church_data)
    first_year = plot_bounds['x_range'][0]
    current_year = plot_bounds['x_range'][1]

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
        left=[round(x) for x in xvals],
        right=[round(x) + round(width_array[0]) for x in xvals[:-1]] + [church_data[prop].max()],
    ))

    plot = make_plot_object(
        title=prop_string + " in " + str(current_year), 
        x_axis_label=prop_string, 
        y_axis_label='Church Count',
        plot_bounds={'x_range': (0, max(xvals)), 'y_range': (0, max(yvals))},
        tools=_make_histogram_tools(bar_data, prop_string)
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
