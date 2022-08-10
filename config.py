# This file MUST be configured in order for the code to run properly

# Make sure you put all your input images into an 'assets' folder. 
# Each layer (or category) of images must be put in a folder of its own.

# CONFIG is an array of objects where each object represents a layer
# THESE LAYERS MUST BE ORDERED.

# Each layer needs to specify the following
# 1. id: A number representing a particular layer
# 2. name: The name of the layer. Does not necessarily have to be the same as the directory name containing the layer images.
# 3. directory: The folder inside assets that contain traits for the particular layer
# 4. required: If the particular layer is required (True) or optional (False). The first layer must always be set to true.
# 5. rarity_weights: Denotes the rarity distribution of traits. It can take on three types of values.
#       - None: This makes all the traits defined in the layer equally rare (or common)
#       - "random": Assigns rarity weights at random. 
#       - array: An array of numbers where each number represents a weight. 
#                If required is True, this array must be equal to the number of images in the layer directory. The first number is  the weight of the first image (in alphabetical order) and so on...
#                If required is False, this array must be equal to one plus the number of images in the layer directory. The first number is the weight of having no image at all for this layer. The second number is the weight of the first image and so on...

# Be sure to check out the tutorial in the README for more details.                

CONFIG = [
    {
        'id': 1,
        'name': 'layer1',
        'directory': 'fimmick-cmi/rare/Layer1',
        'required': True,
        'rarity_weights': None,
    },
    {
        'id': 2,
        'name': 'layer2',
        'directory': 'fimmick-cmi/rare/Layer2',
        'required': True,
        'rarity_weights': None,
    },
    {
        'id': 3,
        'name': 'layer3',
        'directory': 'fimmick-cmi/rare/Layer3',
        'required': True,
        'rarity_weights': None,
    },
    {
        'id': 4,
        'name': 'layer4',
        'directory': 'fimmick-cmi/rare/Layer4',
        'required': True,
        'rarity_weights': None,
    },
    {
        'id': 5,
        'name': 'layer5',
        'directory': 'fimmick-cmi/rare/Layer5',
        'required': True,
        'rarity_weights': None,
    }
]

#
#
#  Config Example:
#
#
#
# CONFIG = [
#     {
#         'id': 1,
#         'name': 'background',
#         'directory': 'BG',
#         'required': True,
#         'rarity_weights': 'random',
#     },
#     {
#         'id': 2,
#         'name': 'body',
#         'directory': 'body',
#         'required': True,
#         'rarity_weights': [12, 12, 3, 6, 6, 12, 3],
#     },
#     {
#         'id': 3,
#         'name': 'hair',
#         'directory': 'hair',
#         'required': True,
#         'rarity_weights': 'random',
#     },
#     {
#         'id': 4,
#         'name': 'clothes',
#         'directory': 'clothes',
#         'required': True,
#         'rarity_weights': 'random',
#     },
#     {
#         'id': 5,
#         'name': 'accessories/jewelry',
#         'directory': 'Accessories_Jewelry',
#         'required': False,
#         'rarity_weights': 'random',
#     },
#     {
#         'id': 6,
#         'name': 'glasses',
#         'directory': 'Glasses_Shades',
#         'required': False,
#         'rarity_weights': 'random',
#     },
#     {
#         'id': 7,
#         'name': 'hat/headband',
#         'directory': 'Hat_Headband',
#         'required': False,
#         'rarity_weights': 'random',
#     },
#     {
#         'id': 8,
#         'name': 'photography accessories(front)',
#         'directory': 'Photography_Accessories',
#         'required': True,
#         'rarity_weights': 'random',
#     },
# ]

