import pandas as pd

import bokeh.plotting as bkp
import bokeh.models as bkm
import bokeh.layouts as bkl


def read_data(fname):
    '''Small wrapper so I dont have to type this over and over. '''

    data = pd.read_csv(fname, 
        delimiter=' ',
        header=1,
        names=['phase', 'flux', 'err']
    )

    data['o_flux'] = data['flux']

    data['upper_err'] = data['flux'] + data['err']
    data['lower_err'] = data['flux'] - data['err']

    # Convert to columnDataSource
    data = bkm.ColumnDataSource(data)

    return data


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