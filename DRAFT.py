import os
import dash
import dash_html_components as html
import base64

app = dash.Dash()
path = "/Users/kanferg/Desktop/NIH_Youle/Python_projacts_general/dash/Table_interactive_montage/Image_example/"
os.chdir(path)
image_filename = 'test.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div([
    html.Img(src='data:image/png;base64,{}'.format(encoded_image))
])

if __name__ == '__main__':
    app.run_server()

