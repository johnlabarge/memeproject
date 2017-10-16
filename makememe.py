from flask import Flask
from flask import send_file
import io
import os
#import ..mememaker
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from google.cloud import storage

app = Flask(__name__)
font_path = os.path.join(os.path.dirname(__file__),
                                      'RobotoMonoBold.ttf')

@app.route('/') 
def health_check():
   return "Healthy"

@app.route('/base_image')
def base_image():
     return send_file(image(),  mimetype='image/jpeg')#return 'Hello, World'

@app.route('/<string:top_text>/<string:bottom_text>')
def make_meme(top_text,bottom_text):

    top_text = top_text.replace('_',' ')
    bottom_text = bottom_text.replace('_',' ')

    memeImage = Image.open(image())
    draw = ImageDraw.Draw(memeImage)

    top_font = get_font(top_text,memeImage,draw)
    bottom_font = get_font(bottom_text,memeImage,draw)

    top_x_pos = get_x_position(top_text,top_font,memeImage,draw)
    bottom_x_pos = get_x_position(bottom_text,bottom_font,memeImage,draw)

    draw.multiline_text([top_x_pos,0],top_text,font=top_font,fill='white',align='center')
    draw.multiline_text([bottom_x_pos,memeImage.height-bottom_font.size-2],bottom_text,font=bottom_font,fill='white',align="center")

    outImage = io.BytesIO(b'')
    memeImage.save(outImage,"JPEG")
    outImage.seek(0)

    return send_file(outImage, mimetype='image/jpeg')

def get_x_position(text,font,image,drawer):
    center_of_image = image.size[0]/2
    text_center = drawer.textsize(text,font=font)[0]/2
    return center_of_image-text_center


def get_font(text,image,drawer):
    image_size = image.size
    image_width = image_size[0]
    image_height = image_size[1]
    font_size = image_height/4

    def update_font():
        return ImageFont.truetype(font_path,font_size)

    while True:
        font = update_font()
        text_width = drawer.textsize(text, font=font)[0]
        if image_width < text_width:
            font_size = font_size - 1
        else:
            return font

def base_image_bucket():
    return storage.Client().get_bucket("cloudjlb-container-devops-memeimages")


def image():
    blob = base_image_bucket().blob("meme-image.jpg");
    f = io.BytesIO(b'')
    blob.download_to_file(f)
    f.seek(0)
    return f
    #return Image.open(f)

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
