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


def make_comparison_plot(church_data, props):
    if len(props) > 2:
        logging.warning("Comparison query provided more than 2 properties, ignoring the rest")
        props = props[:2]

    churches = church_data.groupby('church_id')

    plot_bounds = get_extents(props[0], props[1], church_data)
    prop0_string = SHORT_CATEGORY_DICT[props[0]]
    prop1_string = SHORT_CATEGORY_DICT[props[1]]

    comparison_data = ColumnDataSource(data=dict(
        x=[x[1].iloc[-1] for x in churches[props[0]]],
        y=[y[1].iloc[-1] for y in churches[props[1]]],
        church_name=[church[1]['name'].iloc[-1] for church in churches],
        church_id=[church[1]['church_id'].iloc[-1] for church in churches],
    ))

    comparison_history = ColumnDataSource(data={'x0': [], 'y0': [], 'x1': [], 'y1': []})
    comparison_history_points = {
        'x':[list(x[1]) for x in churches[props[0]]],
        'y':[list(y[1]) for y in churches[props[1]]],
    }

    plot = make_plot_object(
        title=prop0_string + ' vs. ' + prop1_string,
        x_axis_label=prop0_string,
        y_axis_label=prop1_string,
        plot_bounds=plot_bounds,
    )

    xvals = [x[1].iloc[-1] for x in churches[props[0]]]
    yvals = [y[1].iloc[-1] for y in churches[props[1]]]

    points = plot.circle(
        x='x',
        y='y',
        source=comparison_data,
        size=10,
        alpha=0.2,
        hover_alpha=1.0,
        hover_color='orange',
        line_width=1,
    )

    lines = plot.segment(
        x0='x0',
        y0='y0',
        x1='x1',
        y1='y1',
        source=comparison_history, 
        line_color='orange',
        line_width=1,
    )

    plot.add_tools(*_make_comparison_tools(
        comparison_data,
        comparison_history, 
        comparison_history_points, 
        points, 
        prop0_string, 
        prop1_string
    ))

    prop0_slider = make_range_slider(
        plot_bounds['x_range'],
        title=prop0_string,
        step=1/100,
        callback=CustomJS(args={'plot': plot}, code="plot.x_range.end = cb_obj.value;"),
    )

    prop1_slider = make_range_slider(
        plot_bounds['y_range'],
        title=prop1_string,
        step=1/100,
        callback=CustomJS(args={'plot': plot}, code="plot.y_range.end = cb_obj.value;"),
    )
        
    return Column(
        plot, 
        prop0_slider, 
        prop1_slider,
    )


def _make_comparison_tools(point_source, history_source, history_points, points, prop0_str, prop1_str):
    return (
        HoverTool(
            tooltips="<div>@church_name</div>",
            callback=CustomJS(
                args={'history_source': history_source},
                code="""
                    var history_points = %s;
                    showHistoryLine(history_source, history_points, cb_data.index['1d'].indices);
                """ % history_points,
            ),
            renderers=[points],
        ),
        TapTool(
            callback=CustomJS(
                args={'data_source': point_source},
                code="""
                    var selectedChurches = getElementsAt(cb_obj.data, data_source.selected['1d']['indices'],
                        ['church_id', 'church_name', 'x', 'y']);
                    html = makeChurchComparisonList('{prop0_string}', '{prop1_string}', selectedChurches);
                    populateDetailsColumns(html);
                """.format(prop0_string=prop0_str, prop1_string=prop1_str),
            ),
            renderers=[points],
        ),
    )


