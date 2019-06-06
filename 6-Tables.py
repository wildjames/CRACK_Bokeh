import pandas as pd

import bokeh.models as bkm
import bokeh.layouts as bkl
import bokeh.plotting as bkp



data = pd.read_csv('data/HeartDisease.csv', index_col=0, )
data = bkm.ColumnDataSource(data)
column_names = ['ID','Age','Sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','num','Place']

cols = []
for column in column_names:
    col = bkm.widgets.TableColumn(field=column, title=column)
    cols.append(col)

table = bkm.widgets.DataTable(source=data, columns=cols, width=1600, height=900, 
    fit_columns=True, index_position=None,
    reorderable = True,
    selectable = True,
    sortable = True,

)

bkp.curdoc().add_root(table)