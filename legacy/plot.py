
from bokeh.models import Slider


def get_extents(xprop, yprop, church_data):
    return {
        'x_range': {'start': church_data[xprop].min(), 'end': church_data[xprop].max()},
        'y_range': {'start': church_data[yprop].min(), 'end': church_data[yprop].max()},
    }


def make_range_slider(rng, title, callback, step=1):
    if step < 0:
        raise ValueError("Invalid setting for step: {step}".format(step=step))
    elif step < 1:
        step *= (rng['end'] - rng['start'])
        
    return Slider(
        start=rng['start']+1, 
        end=rng['end'], 
        value=rng['end'], 
        step=step,
        title=title,
        callback=callback,
    )

