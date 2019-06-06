import pandas as pd

import bokeh.plotting as bkp
import bokeh.models as bkm
import bokeh.layouts as bkl

from demo import read_data

#TODO:
def construct_figure(fname, color, title):
    '''Writing the same code twice is for idiots'''

    # Grab the data from the file, into a columndatasource
    bokeh_data = read_data(fname)

    # Create a bokeh figure
    p = bkp.figure(title=title, plot_width=1200, plot_height=350)
    # Add data to it
    p.scatter(x='phase', y='flux', source=bokeh_data, color=color)

    # Format some stuff
    p.xaxis.axis_label = 'Phase'
    p.yaxis.axis_label = 'Flux'

    return p


# Plot the first figure
fig1 = construct_figure('data/SDSSJ0748_0_2017-01-22_KG5.calib', 'black', title="I'm the first figure!")
# Plot the second figure
fig2 = construct_figure('data/SDSSJ0748_0_2017-12-12_KG5.calib', 'red', title="I'm the second figure :(")



# Slave the x axes to each other
fig2.x_range = fig1.x_range


# Make a layout
figs = [fig1, fig2]
layout = bkl.column(figs)

bkp.show(layout)