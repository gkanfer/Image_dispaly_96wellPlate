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


app = dash.Dash()

app.layout = html.Div([
    dcc.Dropdown(
        id='image-dropdown',
        options=[{'label': i, 'value': i} for i in list_of_images],
        value=list_of_images[0]
    ),
    dcc.Slider(
        id='my-slider_low_prec',
        min=1,
        max=99,
        step=5,
        value=1,
    ),
    dcc.Slider(
            id='my-slider_up_prec',
            min=1,
            max=99,
            step=5,
            value=99,
        ),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Img(id='image',style={'height':'10%', 'width':'10%'})
])

@app.callback(
    Output('image', 'src'),
    [Input('submit-val', 'n_clicks'),
    State('image-dropdown', 'value'),
    State('my-slider_low_prec', 'value'),
    State('my-slider_up_prec', 'value')],
    prevent_intial_call=True)
def update_image_src(n,dropdown,low,high):
    if len(dropdown) > 0:
        os.chdir(image_directory)
        pixels = tfi.imread(dropdown)
        img = show_image_adjust(pixels,low,high)
        im_pil=Image.fromarray(np.uint8(img))
        os.chdir(path_out)
        im_pil.save("1.png", format='png')
        img_name = "1.png"
        return path_out + '/' + img_name
    elif len(dropdown) == 0:
        raise dash.exceptions.PreventUpdate

if __name__ == '__main__':
    app.run_server()

