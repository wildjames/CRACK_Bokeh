import pandas as pd
import datetime
import time
import os

import bokeh.plotting as bkp
import bokeh.models as bkm
import bokeh.layouts as bkl

def monitor_file():
    '''Stream data to the file, line by line.'''
    try:
        line = temperature_file.readline().strip()
        if line == '':
            raise EOFError

        line = line.split(',')
        date, temp = line

        date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        temp = float(temp)

        new_line = {'time': [date], 'temp': [temp]}
        data.stream(new_line, rollover=100)
    
        print("At {}, the temperature is {}".format(date, temp))
    except EOFError:
        pass


# If the temperature data file does not exist, make it as an empty file. 
if not os.path.isfile('data/TemperatureData.txt'):
    with open('data/TemperatureData.txt', 'w') as f:
        f.write('')

# I need to open the file,  g r a c e f u l l y
temperature_file = open('data/TemperatureData.txt', 'r', os.O_NONBLOCK)

# Initialise the data storage
data = bkm.ColumnDataSource({'time':[], 'temp':[]})

# Fill with the data so far.
for line in temperature_file:
    line = line.strip().split(',')
    date, temp = line

    date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    temp = float(temp)

    new_line = {'time': [date], 'temp': [temp]}
    data.stream(new_line, rollover=100)



# Here, we make the figure and add the line glyph
p = bkp.figure(title='Streaming Data Demo', plot_width=1600, plot_height=450, x_axis_type='datetime')
p.line(x='time', y='temp', source=data)

# Make pretty axes
p.xaxis.formatter = bkm.DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )
p.xaxis.axis_label = 'Time'
p.yaxis.axis_label = 'Temperature'

# Add the figure, and the periodic callback.
bkp.curdoc().add_root(p)
bkp.curdoc().add_periodic_callback(monitor_file, 50)