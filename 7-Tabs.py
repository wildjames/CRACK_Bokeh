import pandas as pd
import numpy as np
import datetime
import time
import os

import bokeh.plotting as bkp
import bokeh.models as bkm
import bokeh.layouts as bkl

from demo import read_data

def monitor_file():
    global temp_data
    try:
        line = temperature_file.readline().strip()
        if line == '':
            raise EOFError

        line = line.split(',')
        date, temp = line

        date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        temp = float(temp)

        new_line = {'time': [date], 'temp': [temp]}
        temp_data.stream(new_line, rollover=100)
    
        print("At {}, the temperature is {}".format(date, temp))
    except EOFError:
        pass

# If the temperature data file is not there, create it as an empty file
if not os.path.isfile('data/TemperatureData.txt'):
    with open('data/TemperatureData.txt', 'w') as f:
        f.write('')

# I need to open the file,  g r a c e f u l l y
temperature_file = open('data/TemperatureData.txt', 'r', os.O_NONBLOCK)
# Initialise the data storage as empty
temp_data = bkm.ColumnDataSource({'time':[], 'temp':[]})

# Fill with the data so far.
for line in temperature_file:
    line = line.strip().split(',')
    date, temp = line

    date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    temp = float(temp)

    new_line = {'time': [date], 'temp': [temp]}
    temp_data.stream(new_line, rollover=100)

# Here, we make the figure and add the line glyph
p = bkp.figure(title='Streaming Data Demo', plot_width=1600, plot_height=800, x_axis_type='datetime')
p.line(x='time', y='temp', source=temp_data, line_width=3)

# Make pretty axes
p.xaxis.formatter = bkm.DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )
p.xaxis.axis_label = 'Time'
p.yaxis.axis_label = 'Temperature'


########################################################################################
########################################################################################
########################################################################################

heart_data = pd.read_csv('data/HeartDisease.csv', index_col=0)
heart_data = bkm.ColumnDataSource(heart_data)
column_names = ['ID','Age','Sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','num','Place']

cols = []
for column in column_names:
    col = bkm.widgets.TableColumn(field=column, title=column)
    cols.append(col)

table = bkm.widgets.DataTable(source=heart_data, columns=cols, width=1600, height=800, fit_columns=True, index_position=None,
    reorderable = True,
    selectable = True,
    sortable = True,
)


########################################################################################
########################################################################################
########################################################################################


def alter_data(attr, old, new):
    '''Take a ColumnDataSource, and modify it in place. Adds [offset] to the flux column's original value.'''
    offset = float(new)

    # Grab the stuff for tweaking
    data = tab3_data.data

    offset = np.exp(offset * data['phase'])

    data['flux']      = data['o_flux'] + offset
    data['upper_err'] = data['flux'] + data['err']
    data['lower_err'] = data['flux'] - data['err']

    tab3_data.data = data


fname = 'data/SDSSJ0748_0_2017-02-15_KG5.calib'
title = 'Slide my Slider ;)'
color = 'black'

# Grab the data from the file, into a pandas array
tab3_data = read_data(fname)

# Create a bokeh figure
tab3_plot = bkp.figure(title=title, plot_width=1600, plot_height=700)
# Format some stuff
tab3_plot.xaxis.axis_label = 'Phase'
tab3_plot.yaxis.axis_label = 'Flux'

# Add data to it
tab3_plot.scatter(x='phase', y='flux', source=tab3_data, color=color)


#### Lets add a slider 
slider = bkm.Slider(title='Flux offset', start=-1, end=1, value=0.0, width=600, step=0.01)
#TODO:
slider.on_change('value', alter_data)


# Make layouts, and add to document
tab1_layout = bkl.row(p)
tab2_layout = bkl.row(table)
tab3_layout = bkl.column([tab3_plot, slider])

tab1 = bkm.Panel(child=tab1_layout, title='Temperature Plot')
tab2 = bkm.Panel(child=tab2_layout, title='Heart Disease Data')
tab3 = bkm.Panel(child=tab3_layout, title='Slider demo')

tabs = bkm.widgets.Tabs(tabs=[tab1, tab2, tab3])

bkp.curdoc().add_root(tabs)
bkp.curdoc().add_periodic_callback(monitor_file, 10)