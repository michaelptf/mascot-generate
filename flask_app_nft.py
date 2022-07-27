
from asyncore import read
from flask import Flask, request, render_template, send_file
from nft_generate import main
import os
import random
import csv


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
# change the path where the output csv file will be
csvfile_path = os.path.join('static', 'output', 'edition_' + edition_name, 'metadata.csv')
app.config['CSV_PATH'] = csvfile_path

def checkRarity(image_number):
  # get the nft number
  nft_id = image_number
  # open metadata.csv
  with open(app.config['CSV_PATH'], 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)
    # get the specific nft row
    result_row = rows[nft_id+1]

    if(result_row[2] == '91' or result_row[2] == '197'):
      return "SUPER RARE"
    elif(result_row[2] == '108' or result_row[2] =='118'):
      return "RARE"
    elif(result_row[2] == '60' or result_row[2] =='71' or result_row[2] =='141'):
      return "COMMON"
    


@app.route('/', methods=["POST", "GET"])
def home():
  preview_image_list = []
  # generate 6 random number for display
  random_number_list = random.sample(range(1000), 6)
  # append that 6 random images path to the list
  for number in random_number_list:
    print(number)
    result_number = f"{number:04}"
    preview_image_list.append(os.path.join(app.config['UPLOAD_FOLDER'], 'Amuro_'+ app.config['BRAND_NAME'] +'_Avatar_' + str(result_number) + '.png'))

  return render_template("index.html", preview_image_list=preview_image_list, brand_name=app.config['BRAND_NAME'])

@app.route('/strike', methods=["POST"])
def strike():
  
  if request.method == "POST":
    # generate a random numebr
    random_image_number = random.randint(0, 1000)
    global image_number
    image_number = f"{random_image_number:04}" # change the number of digit want to diplay

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

    # check the rarity of the nft
    rarity_text = checkRarity(random_image_number)
    if(rarity_text == "SUPER RARE"):
      rarity='super-rare'
    elif(rarity_text == "RARE"):
      rarity='rare'
    else:
      rarity=''
    
    # show mutiple of image
    # image_list = os.listdir(app.config['UPLOAD_FOLDER'])
    # result_image_list = ['output/edition_img_output/images/' + image for image in image_list]
    return render_template("striked.html", result_image=result_image, image_number=image_number, brand_name=app.config['BRAND_NAME'], edition_name=app.config['EDITION_NAME'], rarity_box=rarity,rarity_text=rarity_text)

@app.route('/download')
def download_nft():
  img_path = os.path.join('static', 'output', 'edition_' + app.config['EDITION_NAME'], 'images', 'Amuro_' + app.config['BRAND_NAME'] + '_Avatar_'+str(image_number)+'.png')
  return send_file(img_path, as_attachment=True)

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
