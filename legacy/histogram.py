import logging

from legacy.controls import make_range_slider
from legacy.controls import make_category_select
from legacy.categories import get_category_string
from legacy.plot import apply_theme
from legacy.plot import get_extents
from legacy.plot import make_plot_object

from bokeh.layouts import Column 
from bokeh.models import ColumnDataSource
from bokeh.models import CustomJS
from bokeh.models import HoverTool
from bokeh.models import TapTool

from copy import deepcopy
import numpy as np

def _squash_outliers(data, cutoff=2):
    try:
        q1, q3 = np.percentile(data, [25, 75])
        upper_fence = q3 + cutoff * (q3 - q1)
        data[data > upper_fence] = (upper_fence + 1)
        return data
    except IndexError:
        return []


def make_histogram_plot(church_data, prop):

    plot_bounds = get_extents('year', prop, church_data)
    first_year = plot_bounds['x_range'][0]
    current_year = plot_bounds['x_range'][1]

    bin_midpoints = {}
    hist_items = {}
    max_vals = {}
    for year in range(first_year, current_year + 1):
        yearly_church_data = church_data.loc[church_data['year'] == year]
        squashed_data = _squash_outliers(deepcopy(yearly_church_data[prop]))
        max_vals[year] = yearly_church_data[prop].max()
        __, bins = np.histogram(squashed_data, bins='fd')
        bin_pairs = zip(list(bins[:-1]), list(bins[1:-1]) + [max_vals[year] + 1])
        bin_midpoints[year] = list((bins[1:] + bins[:-1]) / 2)
        hist_items[year] = [
            yearly_church_data.ix[(left <= yearly_church_data[prop]) & (yearly_church_data[prop] <
                right)].sort_values(prop).to_dict(orient='records') for left, right in bin_pairs
        ]

    prop_string = get_category_string(prop)

    xvals = bin_midpoints[current_year]
    yvals = [len(items) for items in hist_items[current_year]]

    if len(xvals) == 1:
        width_array = [1]
    else:
        width_array = [xvals[1]-xvals[0]] * len(xvals) 

    bar_data = ColumnDataSource(data=dict(
        x=xvals,
        width=width_array,
        top=yvals,
        items=hist_items[current_year],
        left=[round(x-width_array[0]/2) for x in xvals],
        right=[round(x + width_array[0]/2) for x in xvals[:-1]] + [max_vals[current_year]]
    ))

    plot = make_plot_object(
        title=prop_string + " in " + str(current_year), 
        x_axis_label=prop_string, 
        y_axis_label='Church Count',
        plot_bounds={'x_range': (0, xvals[-1]), 'y_range': (0, max(yvals))},
        tools=_make_histogram_tools(bar_data, prop, prop_string)
    )

    bars = plot.vbar(
        x='x',
        width='width',
        bottom=0,
        top='top',
        source=bar_data,
    )
    apply_theme(plot, bars)

    year_slider = make_range_slider(
        plot_bounds['x_range'],
        title='Year',
        callback=CustomJS(
            args={'plot': plot, 'bar_data': bar_data}, 
            code="""
                histogramSliderCallback(cb_obj.value, '{prop_string}', {bin_midpoints}, {hist_items}, 
                    {max_vals}, plot, bar_data);
            """.format(prop_string=prop_string, bin_midpoints=bin_midpoints, hist_items=hist_items, max_vals=max_vals),
        ),
    )

    return Column(
        make_category_select(prop),
        plot, 
        year_slider,
    )


def _make_histogram_tools(data_source, prop, prop_string):
    return [
        HoverTool(
            tooltips="""
                <div>@top churches between @left and @right</div>
            """,
        ),
        TapTool(
            callback=CustomJS(
                args={'data_source':data_source},
                code="""
                    html = makeChurchList("{prop}", "{prop_string}", 
                        cb_obj.data['items'][cb_obj.selected['1d']['indices'][0]]);
                    populateDetailsColumns([html]);
                """.format(prop=prop, prop_string=prop_string),
            ),
        ),
    ]


