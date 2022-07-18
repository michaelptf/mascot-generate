

from flask import Flask, request, render_template, send_file
from nft_generate import main
import os

app = Flask(__name__)
app.config["DEBUG"] = True
# change the path where the output image will be
img_folder = os.path.join('static', 'output', 'edition_img_output', 'images')
app.config['UPLOAD_FOLDER'] = img_folder

@app.route('/', methods=["POST", "GET"])
def home():
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
      os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
    if request.method == "POST":
        global number_of_image
        # number_of_image = request.form["imageNumber"]
        number_of_image = 1
        main(number_of_image)
        # change the file name of the result image to your own
        # result_img = os.path.join(app.config['UPLOAD_FOLDER'], '0.png')
        # return render_template("index.html", result_img=result_img)

        # show mutiple of image
        image_list = os.listdir(app.config['UPLOAD_FOLDER'])
        result_image_list = ['output/edition_img_output/images/' + image for image in image_list]
        return render_template("index.html", result_image_list=result_image_list)
    return render_template("index.html")

@app.route('/download')
def download_nft():
    img_path = os.path.join('static', 'output', 'edition_img_output', 'images', 'Amuro_Brand name_Avatar_0.png')
    return send_file(img_path, as_attachment=True)
