from flask import Flask, request, render_template
from nft_generate import main
import os

app = Flask(__name__)
app.config["DEBUG"] = True
# change the path where the output image will be
img_folder = os.path.join('static', 'output', 'edition_img_output', 'images')
app.config['UPLOAD_FOLDER'] = img_folder

@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        main()
        # change the file name of the result image to your own
        result_img = os.path.join(app.config['UPLOAD_FOLDER'], '0.png')
        return render_template("index.html", result_img=result_img)
    return render_template("index.html")

