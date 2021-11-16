import dash
import dash.exceptions
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output, State
import tifffile as tfi
import glob
import os
import numpy as np
from skimage.exposure import rescale_intensity, histogram
import matplotlib.pyplot as plt
from PIL import Image, ImageEnhance
import base64
import pandas as pd
import re
from random import randint
from io import BytesIO


path_out = "/Users/kanferg/Desktop/NIH_Youle/Python_projacts_general/dash/Table_interactive_montage/temp/"
path = "/Users/kanferg/Desktop/Gil_LabWork/Autophagy_nanoscale_project/Antibody_testing/96_well_40xW_6KO_vps34ini/20210817_103210_942/"
os.chdir(path)
files =  glob.glob("*.tiff")

def show_image_adjust(image, low_prec, up_prec):
    """
    image= np array 2d
    low/up precentile border of the image
    """
    percentiles = np.percentile(image, (low_prec, up_prec))
    scaled_ch1 = rescale_intensity(image, in_range=tuple(percentiles))
    return scaled_ch1

def unique_rand(inicial, limit, total):
    data = []
    i = 0
    while i < total:
                number = randint(inicial, limit)
                if number not in data:
                    data.append(number)
                    i += 1
    return data


def get_file(ind,files):
    '''
    :cvar
    ind selected well
    files glob of all the files in the selected directory
    '''
    target = "Well" + ind
    lis_temp = []
    for file in files:
        if target in file:
            lis_temp.append(file)
        else:
            continue
    single_ind = unique_rand(0, len(lis_temp), 1)
    return lis_temp[single_ind[-1]]

# create the 96 well plate layout

ind = ["B", "C", "D", "E", "F", "G"]
_col = ["02", "03", "04", "05", "06", "07", "08", "09", "10"]
values = {"02": [], "03": [], "04": [], "05": [], "06": [], "07": [], "08": [], "09": [], "10": []}
for i in range(len(_col)):
    for z in range(len(ind)):
        values[_col[i]].append(ind[z] + _col[i])
print(values)
df = pd.DataFrame(values)

#app = dash.Dash()
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = html.Div([
    dash_table.DataTable(
            id='datatable-interactivity',
            columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns],
            data=df.to_dict('records'),
            style_cell={'minWidth': 95, 'maxWidth': 95, 'width': 95},
            style_header={
                    'backgroundColor': 'rgb(210, 210, 210)',
                    'color': 'black',
                    'fontWeight': 'bold'
                },
            style_data={
                    'color': 'black',
                    'backgroundColor': 'white'
                },
    ),
    dbc.Row([
        dbc.Col(
            dcc.Slider(
                id='my-slider_low_prec',
                min=1,
                max=99,
                step=1,
                value=1,
                vertical=False,
                ), width={'size': 3, "offset": 0}),
        dbc.Col(
            dcc.Slider(
                id='my-slider_up_prec',
                 min=1,
                max=99,
                step=1,
                value=99,
                vertical=False,
                ), width={'size': 3, "offset": 0})]),
    dbc.Row([
        dbc.Col(
            html.Button('Submit', id='submit-val', n_clicks=0)
            , width={'size': 3, "offset": 0}),
        dbc.Col(
            dcc.Dropdown(id='dropdown_channel',
                         options=[{'label': i, 'value': i}
                                  for i in ['ch1', 'ch2']])
            , width={'size': 3, "offset": 0}),
        ]),

    html.Img(id='image', style={'height': '50%', 'width': '50%'})
])


@app.callback(
    Output('image', 'src'),
    [Input('submit-val', 'n_clicks'),
     State('datatable-interactivity', 'active_cell'),
     State('dropdown_channel','value'),
     State('my-slider_low_prec', 'value'),
     State('my-slider_up_prec', 'value')],
    prevent_intial_call=True)
def update_image_src(n, active_cell, channel ,low, high):
    if len(active_cell) > 0:
        if channel == 'ch1':
            ch = 0
        else:
            ch = 1
        ind = df.iloc[active_cell['row'], active_cell['column']]
        os.chdir(path)
        file = get_file(ind,files)
        pixels = tfi.imread(file)
        pixels = pixels[:,:,ch]
        img = show_image_adjust(pixels, low, high)
        im_pil = Image.fromarray(np.uint16(img))
        os.chdir(path_out)
        im_pil.save("1.png", format='png')
        encoded_image = base64.b64encode(open("1.png", 'rb').read())
        return 'data:image/png;base64,{}'.format(encoded_image.decode())
    elif len(dropdown) == 0:
        raise dash.exceptions.PreventUpdate

if __name__ == '__main__':
    app.run_server()


