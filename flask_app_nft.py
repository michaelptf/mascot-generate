
from asyncore import read
from flask import Flask, request, render_template, send_file, url_for
from nft_generate import main
import os
import random
import csv
from PIL import Image, ImageDraw, ImageFont

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
nft_card_caption = "Gump NFT Series"
app.config['CAPTION'] = nft_card_caption

def checkRarity(image_number):
  # get the nft number
  nft_id = image_number
  # open metadata.csv
  with open(app.config['CSV_PATH'], 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)
    # get the specific nft row
    result_row = rows[nft_id+1]

    # change accroding to config.py
    if(result_row[2] == '91' or result_row[2] == '197'):
      return "SUPREME"
    elif(result_row[2] == '108' or result_row[2] =='118'):
      return "SUPER RARE"
    elif(result_row[2] == '60' or result_row[2] =='71' or result_row[2] =='141'):
      return "RARE"
    
def paste_nft_to_frame():
  # get the image open
  nft_frame = Image.open('static/images/Gump nft frame clean.png')
  nft_image = Image.open(result_image)
  # open the edition tag that will be pasted on the frame
  edition_image = Image.open('static/images/Edition.png')
  # check the rarity then open the corresponding tag image
  rarity = checkRarity(random_image_number)
  rarity_image = Image.open(os.path.join('static', 'images', rarity + '.png'))
  
  # calculate the ratio of wanted tag size to image size
  ratio = int(168/edition_image.height)
  # make a copy and resize image
  nft_frame_copy = nft_frame.copy()
  nft_image_copy = nft_image.copy().resize((1810, 1810))
  edition_image_copy =  edition_image.copy().resize((edition_image.width*ratio, edition_image.height*ratio))
  rarity_image_copy = rarity_image.copy().resize((rarity_image.width*ratio, rarity_image.height*ratio))

  # make the nft rounder
  mask_image = Image.new("L", nft_image_copy.size, 0)
  draw = ImageDraw.Draw(mask_image)
  draw.rounded_rectangle((0, 0, 1810, 1810), radius=96, fill=255)
  mask_image.save("static/images/mask_image.png", quality=95)

  # paste different component to the frame
  nft_frame_copy.paste(nft_image_copy, (200, 234), mask_image)
  nft_frame_copy.paste(edition_image_copy, (180, 2750))
  nft_frame_copy.paste(rarity_image_copy, (950, 2750))

  #define thw font to be used and paste them to the frame  
  font_title = ImageFont.truetype('static/styles/Montserrat-Regular.ttf', 150)
  font_caption = ImageFont.truetype('static/styles/Montserrat-Regular.ttf', 75)
  title = "#" + str(image_number) + " " + app.config['BRAND_NAME']
  caption = app.config['CAPTION']
  image_editable = ImageDraw.Draw(nft_frame_copy)
  image_editable.text((186,2400), title, (255, 255, 255), font=font_title)
  image_editable.text((186,2600), caption, (255, 255, 255), font=font_caption)
  
  # save the image
  nft_frame_copy.save(os.path.join(app.config['UPLOAD_FOLDER'],  'Framed_Amuro_'+ app.config['BRAND_NAME'] +'_Avatar_' + str(image_number) + '.png'))

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

@app.route('/strike', methods=["POST", "GET"])
def strike():
  
    # generate a random numebr
    global random_image_number
    random_image_number = random.randint(0, 1000)
    global image_number
    image_number = f"{random_image_number:04}" # change the number of digit want to diplay

    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], 'Amuro_'+ app.config['BRAND_NAME'] +'_Avatar_' + str(image_number) + '.png')):
      print("Already have nft pool generated! no need generate nft pool again")
    else :
      print("Start generate function")
      global number_of_image
      number_of_image = request.form["imageNumber"]
      number_of_image = 100 #<-change this number to generate number of image 
      main(number_of_image, app.config['EDITION_NAME'], app.config['BRAND_NAME'])

    # get the nft image path
    global result_image
    result_image = os.path.join(app.config['UPLOAD_FOLDER'], 'Amuro_'+ app.config['BRAND_NAME'] +'_Avatar_' + str(image_number) + '.png')
    paste_nft_to_frame()
    # check the rarity of the nft
    rarity_text = checkRarity(random_image_number)
    if(rarity_text == "SUPREME"):
      rarity='supreme'
    elif(rarity_text == "SUPER RARE"):
      rarity='super-rare'
    else:
      rarity=''
    
    framed_image = os.path.join(app.config['UPLOAD_FOLDER'],  'Framed_Amuro_'+ app.config['BRAND_NAME'] +'_Avatar_' + str(image_number) + '.png')
    return render_template("striked.html", framed_image=framed_image, result_image=result_image , image_number=image_number, brand_name=app.config['BRAND_NAME'], edition_name=app.config['EDITION_NAME'], rarity_box=rarity,rarity_text=rarity_text)

@app.route('/download')
def download_nft():
  img_path = os.path.join(app.config['UPLOAD_FOLDER'], 'Amuro_' + app.config['BRAND_NAME'] + '_Avatar_'+str(image_number)+'.png')
  return send_file(img_path, as_attachment=True)

@app.route('/download_framed')
def download_nft_framed():
  img_path = os.path.join(app.config['UPLOAD_FOLDER'], 'Framed_Amuro_' + app.config['BRAND_NAME'] + '_Avatar_'+str(image_number)+'.png')
  return send_file(img_path, as_attachment=True)

@app.route('/strike_api', methods=["GET"])
def get_info():
    # for hompage 
    preview_image_list = []
    # generate 6 random number for display
    random_number_list = random.sample(range(1000), 6)
    # append that 6 random images path to the list
    for number in random_number_list:
      print(number)
      result_number = f"{number:04}"
      preview_image_list.append(request.host_url + os.path.join(app.config['UPLOAD_FOLDER'], 'Amuro_'+ app.config['BRAND_NAME'] +'_Avatar_' + str(result_number) + '.png'))

    # generate a random numebr
    global random_image_number
    random_image_number = random.randint(0, 1000)
    global image_number
    image_number = f"{random_image_number:04}" # change the number of digit want to diplay

    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], 'Amuro_'+ app.config['BRAND_NAME'] +'_Avatar_' + str(image_number) + '.png')):
      print("Already have nft pool generated! no need generate nft pool again")
    else :
      print("Start generate function")
      global number_of_image
      number_of_image = request.form["imageNumber"]
      number_of_image = 100 #<-change this number to generate number of image 
      main(number_of_image, app.config['EDITION_NAME'], app.config['BRAND_NAME'])

    # get the nft image path
    global result_image
    result_image = os.path.join(app.config['UPLOAD_FOLDER'], 'Amuro_'+ app.config['BRAND_NAME'] +'_Avatar_' + str(image_number) + '.png')
    paste_nft_to_frame()
    # check the rarity of the nft
    rarity_text = checkRarity(random_image_number)
    if(rarity_text == "SUPREME"):
      rarity='supreme'
    elif(rarity_text == "SUPER RARE"):
      rarity='super-rare'
    else:
      rarity='rare'
    
    framed_image = os.path.join(app.config['UPLOAD_FOLDER'],  'Framed_Amuro_'+ app.config['BRAND_NAME'] +'_Avatar_' + str(image_number) + '.png')

    # Returning an api for showing in  reactjs
    return {
      'framed_image': request.host_url + framed_image, 
      'result_image': request.host_url + result_image , 
      'image_number': image_number, 
      'brand_name': app.config['BRAND_NAME'], 
      'edition_name': app.config['EDITION_NAME'], 
      'rarity_box': rarity,
      'rarity_text': rarity_text,
      'preview_image_list': preview_image_list
    }


if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
