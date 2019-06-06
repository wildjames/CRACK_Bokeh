import pandas as pd

import bokeh.plotting as bkp
import bokeh.models as bkm
import bokeh.layouts as bkl

# Get some housekeeping done first
p = bkp.figure(title='Fuck', plot_width=1600, plot_height=700)
p.xaxis.axis_label = 'Phase'
p.yaxis.axis_label = 'Flux'
bkp.curdoc().add_root(p)

fname = 'data/SDSSJ0748_0_2017-01-22_KG5.calib'


# Grab the data from the file with pandas
pandas_data = pd.read_csv(fname, 
    delimiter=' ',
    header=1,
    names=['phase', 'flux', 'err']
)

print("Pandas data:")
print(pandas_data.head())

# I can plot by passing the columns, i.e. as if I were passing '''numpy arrays'''
p.line(x=pandas_data['phase'], y=pandas_data['flux']+0.2, color='black', line_width=3, legend='Numpy array')

# Or I can access by passing the dataframe, and the keys to use...
p.line(x='phase', y='flux', source=pandas_data, color='blue', line_width=3, legend='Pandas DF')


# Now, grab the data and plot it from columndatasource
data = pd.read_csv(fname, 
    delimiter=' ',
    header=1,
    names=['phase', 'flux', 'err']
)
# Offset up a little
data['flux'] += 0.4


# Convert to columnDataSource and plot
data = bkm.ColumnDataSource(data)
p.line(x='phase', y='flux', source=data, color='red', line_width=3, legend='Bokeh CDS')

p.legend.click_policy = 'hide'