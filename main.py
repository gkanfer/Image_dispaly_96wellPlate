import os
import dash_table
import pandas as pd
import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import  dash_core_components as dcc
from dash_canvas import DashCanvas
import glob
from PIL import Image
from io import BytesIO
import base64

#path = "/Users/kanferg/Desktop/Gil_LabWork/Autophagy_nanoscale_project/Antibody_testing/96_well_40xW_BAf_CQ_VPS34i_073021/20210730_113819_117/"
path = "/Users/kanferg/Desktop/NIH_Youle/Python_projacts_general/dash/Table_interactive_montage/Image_example/"
os.chdir(path)
#files = glob.glob("*.tiff")
files = "test.png"

app = dash.Dash(__name__)
server = app.server

# create the 96 well plate layout

ind = ["B", "C", "D", "E", "F", "G"]
_col = ["02", "03", "04", "05", "06", "07", "08", "09","10"]
values = {"02":[], "03":[], "04":[], "05":[], "06":[], "07":[], "08":[], "09":[], "10":[]}
for i in range(len(_col)):
    for z in range(len(ind)):
        values[_col[i]].append(ind[z]+_col[i])
print(values)
df = pd.DataFrame(values)

# -------------------------------------------------------------------------------------
# App layout
#app = dash.Dash(__name__, prevent_initial_callbacks=True) # this was introduced in Dash version 1.12.0
app = dash.Dash(__name__)
app.layout = html.Div([
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns],
        data=df.to_dict('records'),
        style_cell={'minWidth': 95, 'maxWidth': 95, 'width': 95 }),
    html.Br(),
    html.Br(),
    html.Div(id='bar-container'),
    html.Br(),
    html.Img(id='image')
])

@app.callback(
    Output(component_id='bar-container', component_property='children'),
    [Input(component_id='datatable-interactivity', component_property='active_cell')])
def return_cell_info(active_cell):
    return str(active_cell)

# @app.callback(
#     Output(component_id='image', component_property='src'),
#     [Input(component_id='datatable-interactivity', component_property='active_cell')])
# def update_image(active_cell):
#     encoded_image = base64.b64encode(open(image_filename, 'rb').read())
#     return str(active_cell)

# @app.callback(
#     Output(component_id='image', component_property='src'),
#     [Input(component_id='datatable-interactivity', component_property='active_cell')])
# def return_cell_info(active_cell):
#     # row = active_cell['row']
#     # col = active_cell['column']
#     ind = df.iloc[active_cell['row'], active_cell['column']]
#     return str(active_cell)

if __name__ == '__main__':
    app.run_server(debug=False)


