import logging

from legacy.controls import make_range_slider
from legacy.controls import make_category_select
from legacy.categories import SHORT_CATEGORY_DICT
from legacy.plot import apply_theme
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

    hover_data = ColumnDataSource(data={'x0': [], 'y0': [], 'x1': [], 'y1': []})
    selected_data = ColumnDataSource(data={'x0': [], 'y0': [], 'x1': [], 'y1': []})
    history = {
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
    )

    hover_lines = plot.segment(x0='x0', y0='y0', x1='x1', y1='y1', source=hover_data)
    selected_lines = plot.segment(x0='x0', y0='y0', x1='x1', y1='y1', source=selected_data)
    apply_theme(plot, points, hover_lines, selected_lines, overrides={
        1: {'line_color': 'orange', 'line_alpha': 1.0},
        2: {'line_color': 'firebrick', 'line_alpha': 1.0},
    })

    plot.add_tools(*_make_comparison_tools(
        comparison_data,
        hover_data,
        selected_data,
        history, 
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


def _make_comparison_tools(comparison_data, hover_data, selected_data, history, points, prop0_str, prop1_str):
    return (
        HoverTool(
            tooltips="<div>@church_name</div>",
            callback=CustomJS(
                args={'comparisonData': comparison_data, 'hoverData': hover_data}, 
                code="""
                    var history = %s;
                    showHistoryLine(comparisonData, hoverData, history, cb_data.index['1d'].indices);
                """ % history,
            ),
            renderers=[points],
        ),
        TapTool(
            callback=CustomJS(
                args={'comparisonData': comparison_data, 'selectedData': selected_data},
                code="""
                    var history = {history};
                    var selectedChurches = getElementsAt(cb_obj.data, comparisonData.selected['1d'].indices,
                        ['church_id', 'church_name', 'x', 'y']);
                    html = makeChurchComparisonList('{prop0_string}', '{prop1_string}', selectedChurches);
                    populateDetailsColumns(html);
                    showHistoryLine(comparisonData, selectedData, history, comparisonData.selected['1d'].indices);
                """.format(history=history, prop0_string=prop0_str, prop1_string=prop1_str),
            ),
            renderers=[points],
        ),
    )


