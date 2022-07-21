from flask import Flask, request, render_template, send_file
from nft_generate import main
import os
import random


app = Flask(__name__)
app.config["DEBUG"] = True
# change the name of the brand
brand_name = "Gump"
app.config['BRAND_NAME'] = brand_name
#change the name of the edition
edition_name = "Limited"
app.config['EDITION_NAME'] = edition_name
# change the path where the output image will be
img_folder = os.path.join('static', 'output', 'edition_' + edition_name, 'images')
app.config['UPLOAD_FOLDER'] = img_folder


@app.route('/', methods=["POST", "GET"])
def home():
  return render_template("index.html")

@app.route('/strike', methods=["POST"])
def strike():
  
  if request.method == "POST":
    # generate a random numebr
    global image_number
    image_number = random.randint(0, 1250)
    image_number = f"{image_number:04}"

    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], 'Amuro_'+ app.config['BRAND_NAME'] +'_Avatar_' + str(image_number) + '.png')):
      print("Already have nft pool generated! no need generate nft pool again")
    else :
      print("Start generate function")
      global number_of_image
      number_of_image = request.form["imageNumber"]
      number_of_image = 3000 #<-change this number to generate number of image 
      main(number_of_image, app.config['EDITION_NAME'], app.config['BRAND_NAME'])

    # get the nft image path
    result_image = os.path.join(app.config['UPLOAD_FOLDER'], 'Amuro_'+ app.config['BRAND_NAME'] +'_Avatar_' + str(image_number) + '.png')

    # show mutiple of image
    # image_list = os.listdir(app.config['UPLOAD_FOLDER'])
    # result_image_list = ['output/edition_img_output/images/' + image for image in image_list]
    return render_template("striked.html", result_image=result_image, image_number=image_number, brand_name=app.config['BRAND_NAME'], edition_name=app.config['EDITION_NAME'])

@app.route('/download')
def download_nft():
  img_path = os.path.join('static', 'output', 'edition_' + app.config['EDITION_NAME'], 'images', 'Amuro_' + app.config['BRAND_NAME'] + '_Avatar_'+str(image_number)+'.png')
  return send_file(img_path, as_attachment=True)
