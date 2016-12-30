
from bokeh.models import Range1d
from bokeh.models import Slider
from bokeh.models import SaveTool
from bokeh.plotting import Figure
from bokeh.plotting.helpers import _make_glyph


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


def apply_theme(plot, *renderers, **kwargs):

    alpha = 0.2
    hover_color = 'orange'
    hover_alpha = 1.0
    selection_color = 'firebrick'
    selection_alpha = 1.0

    for renderer in renderers:
        hover_props = {}
        selection_props = {}
        for prop_name in ("fill_color", "line_color"):
            if prop_name not in renderer.glyph.__class__.properties():
                continue
            hover_props[prop_name] = hover_color
            selection_props[prop_name] = selection_color

        for prop_name in ("fill_alpha", "line_alpha"):
            if prop_name not in renderer.glyph.__class__.properties():
                continue
            hover_props[prop_name] = hover_alpha
            selection_props[prop_name] = selection_alpha
            setattr(renderer.glyph, prop_name, alpha)

        renderer.hover_glyph = _make_glyph(renderer.glyph.__class__, hover_props, {})
        renderer.selection_glyph = _make_glyph(renderer.glyph.__class__, selection_props, {'line_width': 2})
        renderer.nonselection_glyph = None
        renderer.glyph.line_width=1

    if 'overrides' in kwargs:
        overrides = kwargs['overrides']
        for index, props in kwargs['overrides'].items():
            renderer = renderers[index]
            for prop, value in props.items():
                if prop[:6] == 'hover_':
                    glyph = renderer.hover_glyph
                elif prop[:6] == 'selection_':
                    glyph = renderer.selection_glyph
                else:
                    glyph = renderer.glyph

                setattr(glyph, prop, value)
