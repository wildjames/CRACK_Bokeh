import pandas as pd

import bokeh.plotting as bkp
import bokeh.models as bkm


# Grab the data from the file with pandas
pandas_data = pd.read_csv('data/SDSSJ0748_0_2017-01-22_KG5.calib', 
    delimiter=' ',
    header=1,
    names=['phase', 'flux', 'err']
)
pandas_data['upper_err'] = pandas_data['flux'] + pandas_data['err']
pandas_data['lower_err'] = pandas_data['flux'] - pandas_data['err']

print("Pandas data:")
print(pandas_data.head())


# Convert that to bokeh data type:
bokeh_data = bkm.ColumnDataSource(pandas_data)

# Create a bokeh figure
p = bkp.figure(title='I am a title!', plot_width=1200, plot_height=600)
# Add data to it
p.scatter(x='phase', y='flux', source=bokeh_data)

### here be dragons! ###
# Add errorbars
errorbar_glyphs = bkm.Whisker(base='phase', upper='upper_err', lower='lower_err', 
    source=bokeh_data, line_color='blue')
p.add_layout(errorbar_glyphs)

# Format some stuff
p.xaxis.axis_label = 'Phase'
p.yaxis.axis_label = 'Flux'

bkp.show(p)