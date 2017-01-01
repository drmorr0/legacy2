import logging

from legacy.controls import make_category_select
from legacy.controls import make_range_slider
from legacy.categories import SHORT_CATEGORY_DICT
from legacy.plot import apply_theme
from legacy.plot import get_extents
from legacy.plot import make_plot_object

from bokeh.layouts import Column 
from bokeh.models import ColumnDataSource
from bokeh.models import CustomJS
from bokeh.models import HoverTool
from bokeh.models import TapTool

def make_time_series_plot(church_data, prop):
    churches = church_data.groupby('church_id')

    plot_bounds = get_extents('year', prop, church_data)
    prop_string = SHORT_CATEGORY_DICT[prop]

    time_series_data = ColumnDataSource(data=dict(
        x=[x[1] for x in churches['year']],
        y=[y[1] for y in churches[prop]],
        church_name=[church[1]['name'].iloc[-1] for church in churches],
        delta=["{0:.1f}%".format(y[1].iloc[-1] / y[1].iloc[0] * 100 - 100) for y in churches[prop]],
        church_id=[church[1]['church_id'].iloc[-1] for church in churches],
    ))

    plot = make_plot_object(
        title=prop_string + " over time", 
        x_axis_label='Year', 
        y_axis_label=prop_string,
        plot_bounds=plot_bounds,
        tools=_make_time_series_tools(time_series_data, prop_string),
    )

    lines = plot.multi_line(
        xs='x',
        ys='y',
        source=time_series_data, 
    )
    apply_theme(plot, lines)

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
        make_category_select(prop),
        plot, 
        prop_slider, 
        year_slider,
    )


def _make_time_series_tools(data_source, prop_string):
    return [
        HoverTool(
            tooltips="""
                <div>@church_name</div>
                <div>Growth: @delta</div>
            """,
        ),
        TapTool(
            callback=CustomJS(
                args={'data_source': data_source},
                code="""
                    var selectedChurches = getElementsAt(cb_obj.data, data_source.selected['1d']['indices'],
                        ['church_id', 'church_name', 'x', 'y']);
                    details = makeChurchesDetailsArray('Year', '{prop}', selectedChurches);
                    populateDetailsColumns(details);
                """.format(prop=prop_string),
            ),
        ),
    ]


