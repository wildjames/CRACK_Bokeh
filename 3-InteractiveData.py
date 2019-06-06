import pandas as pd

import bokeh.plotting as bkp
import bokeh.models as bkm
import bokeh.layouts as bkl

from demo import read_data

#TODO:
def offset_data(attr, old, new):
    '''Take a ColumnDataSource, and modify it in place. Adds [offset] to the flux column's original value.'''
    offset = float(new)
    global bokeh_data

    flux = bokeh_data.data['o_flux'] + offset
    err_hi = bokeh_data.data['flux'] + bokeh_data.data['err']
    err_lo = bokeh_data.data['flux'] - bokeh_data.data['err']
    
    data = bokeh_data.data

    data['flux'] = flux
    data['upper_err'] = err_hi
    data['lower_err'] = err_lo

    bokeh_data.data = data


fname = 'data/SDSSJ0748_0_2017-02-15_KG5.calib'
title = 'Slide my Slider ;)'
color = 'black'

# Grab the data from the file, into a pandas array
bokeh_data = read_data(fname)

# Create a bokeh figure
p = bkp.figure(title=title, plot_width=1600, plot_height=700)
# Add data to it
p.scatter(x='phase', y='flux', source=bokeh_data, color=color)

# Format some stuff
p.xaxis.axis_label = 'Phase'
p.yaxis.axis_label = 'Flux'

# Plot the figure
fig = p

#TODO:
#### Lets add a slider 
slider = bkm.Slider(title='Flux offset', start=-1, end=1, value=0.0, width=600, step=0.01)
slider.on_change('value', offset_data)


# Make a layout, and add to document
layout = bkl.column([fig, slider])

bkp.curdoc().add_root(layout)
bkp.curdoc().title = __name__