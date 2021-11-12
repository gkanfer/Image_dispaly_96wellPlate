import dash
import dash.exceptions
import dash_core_components as dcc
import dash_html_components as html
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

path_out = "/Users/kanferg/Desktop/NIH_Youle/Python_projacts_general/dash/Table_interactive_montage/temp/"
image_directory = "/Users/kanferg/Desktop/NIH_Youle/Python_projacts_general/dash/Table_interactive_montage/Image_example/"
list_of_images = [os.path.basename(x) for x in glob.glob('{}*.tiff'.format(image_directory))]

def show_image_adjust(image, low_prec, up_prec):
    """
    image= np array 2d
    low/up precentile border of the image
    """
    percentiles = np.percentile(image, (low_prec, up_prec))
    scaled_ch1 = rescale_intensity(image, in_range=tuple(percentiles))
    return scaled_ch1


# create the 96 well plate layout

ind = ["B", "C", "D", "E", "F", "G"]
_col = ["02", "03", "04", "05", "06", "07", "08", "09","10"]
values = {"02":[], "03":[], "04":[], "05":[], "06":[], "07":[], "08":[], "09":[], "10":[]}
for i in range(len(_col)):
    for z in range(len(ind)):
        values[_col[i]].append(ind[z]+_col[i])
print(values)
df = pd.DataFrame(values)

app = dash.Dash()

app.layout = html.Div([
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns],
        data=df.to_dict('records'),
        style_cell={'minWidth': 95, 'maxWidth': 95, 'width': 95}),
    dcc.Slider(
        id='my-slider_low_prec',
        min=1,
        max=99,
        step=5,
        value=1,
        vertical=True,
    ),
    dcc.Slider(
        id='my-slider_up_prec',
        min=1,
        max=99,
        step=5,
        value=99,
        vertical=True,
        ),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Img(id='image',style={'height':'10%', 'width':'10%'})
])

@app.callback(
    Output('image', 'src'),
    [Input('submit-val', 'n_clicks'),
    State('datatable-interactivity', 'active_cell'),
    State('my-slider_low_prec', 'value'),
    State('my-slider_up_prec', 'value')],
    prevent_intial_call=True)
def update_image_src(n,active_cell,low,high):
    if len(active_cell) > 0:
        ind = df.iloc[active_cell['row'], active_cell['column']]

        os.chdir(image_directory)
        pixels = tfi.imread(dropdown)
        img = show_image_adjust(pixels,low,high)
        im_pil=Image.fromarray(np.uint8(img))
        os.chdir(path_out)
        im_pil.save("1.png", format='png')
         encoded_image = base64.b64encode(open("1.png", 'rb').read())
        return 'data:image/png;base64,{}'.format(encoded_image.decode())
    elif len(dropdown) == 0:
        raise dash.exceptions.PreventUpdate

if __name__ == '__main__':
    app.run_server()

