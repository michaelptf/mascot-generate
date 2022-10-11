#!/usr/bin/env python
# coding: utf-8

# Import required libraries
from PIL import Image
import pandas as pd
import numpy as np
import time
import os
import random
import progressbar

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)



# Import configuration file
from config import CONFIG

# get the current dir
parent_dir = os.path.dirname(os.path.abspath(__file__))

# Parse the configuration file and make sure it's valid
def parse_config():

    # Input traits must be placed in the assets folder. Change this value if you want to name it something else.
    assets_path = os.path.join(parent_dir, 'assets')

    # Loop through all layers defined in CONFIG
    for layer in CONFIG:

        # Go into assets/ to look for layer folders
        layer_path = os.path.join(assets_path, layer['directory'])

        # Get trait array in sorted order
        traits = sorted([trait for trait in os.listdir(layer_path) if trait[0] != '.'])

        # If layer is not required, add a None to the start of the traits array
        if not layer['required']:
            traits = [None] + traits

        # Generate final rarity weights
        if layer['rarity_weights'] is None:
            rarities = [1 for x in traits]
        elif layer['rarity_weights'] == 'random':
            rarities = [random.random() for x in traits]
        elif type(layer['rarity_weights'] == 'list'):
            assert len(traits) == len(layer['rarity_weights']), "Make sure you have the current number of rarity weights"
            rarities = layer['rarity_weights']
        else:
            raise ValueError("Rarity weights is invalid")

        rarities = get_weighted_rarities(rarities)

        # Re-assign final values to main CONFIG
        layer['rarity_weights'] = rarities
        layer['cum_rarity_weights'] = np.cumsum(rarities)
        layer['traits'] = traits
        layer['num_of_traits'] = len(traits)

        print(layer)


# Weight rarities and return a numpy array that sums up to 1
def get_weighted_rarities(arr):
    return np.array(arr)/ sum(arr)

# Generate a single image given an array of filepaths representing layers
def generate_single_image(filepaths, output_filename=None, compression_ratio = 1):

    # Treat the first layer as the background
    bg = Image.open(os.path.join(parent_dir, 'assets', filepaths[0]))


    # Loop through layers 1 to n and stack them on top of another
    for filepath in filepaths[1:]:
        if filepath.endswith('.png'):
            img = Image.open(os.path.join(parent_dir, 'assets', filepath))
            # bg.paste(img, (0,0), img)
            bg.paste(img.convert('RGB'), (0,0), img)

    if compression_ratio != 1:
        width, height = bg.size
        compression_ratio = 0.5
        newWidth = int(width * compression_ratio)
        newHeight = int(height * compression_ratio)
        bg = bg.resize((newWidth, newHeight))

    bg = bg.convert('RGB')

    # Save the final image into desired location
    if output_filename is not None:
        bg.save(output_filename)
    else:
        # If output filename is not specified, use timestamp to name the image and save it in output/single_images
        if not os.path.exists(os.path.join('output', 'single_images')):
            os.makedirs(os.path.join('output', 'single_images'))
        bg.save(os.path.join('output', 'single_images', str(int(time.time())) + '.jpg'))


# Generate a single image with all possible traits
# generate_single_image(['Background/green.png',
#                        'Body/brown.png',
#                        'Expressions/standard.png',
#                        'Head Gear/std_crown.png',
#                        'Shirt/blue_dot.png',
#                        'Misc/pokeball.png',
#                        'Hands/standard.png',
#                        'Wristband/yellow.png'])


# Get total number of distinct possible combinations
def get_total_combinations():

    total = 1
    for layer in CONFIG:
        total = total * len(layer['traits'])
    return total


# Select an index based on rarity weights
def select_index(cum_rarities, rand):

    cum_rarities = [0] + list(cum_rarities)
    for i in range(len(cum_rarities) - 1):
        if rand >= cum_rarities[i] and rand <= cum_rarities[i+1]:
            return i

    # Should not reach here if everything works okay
    return None

# Generate a random set of traits given rarities
def generate_predefined_trait_set_from_config(trait_indexes):

    trait_set = []
    trait_paths = []

    current_layer = 0
    for layer in CONFIG:
        # Extract list of traits and cumulative rarity weights
        traits, cum_rarities = layer['traits'], layer['cum_rarity_weights']

        # Find the index of the current layer
        idx = trait_indexes[current_layer]

        # # Select an element index based on random number and cumulative rarity weights
        # idx = select_index(cum_rarities, index)

        # Add selected trait to trait set
        trait_set.append(traits[idx])

        # Add trait path to trait paths if the trait has been selected
        if traits[idx] is not None:
            trait_path = os.path.join(layer['directory'], traits[idx])
            trait_paths.append(trait_path)

        current_layer = current_layer + 1

    return trait_set, trait_paths

# Generate a random set of traits given rarities
def generate_random_trait_set_from_config():

    trait_set = []
    trait_paths = []

    for layer in CONFIG:
        # Extract list of traits and cumulative rarity weights
        traits, cum_rarities = layer['traits'], layer['cum_rarity_weights']

        # Generate a random number
        rand_num = random.random()

        # Select an element index based on random number and cumulative rarity weights
        idx = select_index(cum_rarities, rand_num)

        # Add selected trait to trait set
        trait_set.append(traits[idx])

        # Add trait path to trait paths if the trait has been selected
        if traits[idx] is not None:
            trait_path = os.path.join(layer['directory'], traits[idx])
            trait_paths.append(trait_path)

    return trait_set, trait_paths


# Generate the image set. Don't change drop_dup
def generate_images(edition, count, brand_name, is_random, compression_ratio, drop_dup=True):

    # Initialize an empty rarity table
    rarity_table = {}
    for layer in CONFIG:
        rarity_table[layer['name']] = []

    # Define output path to output/edition_{edition_num}
    path = os.path.join('static', 'output', 'edition_' + str(edition), 'images')
    # parent_dir = os.path.dirname(os.path.abspath(__file__))
    # print(parent_dir)
    op_path = os.path.join(parent_dir, path)
    print(op_path)
    # Will require this to name final images as 000, 001,...
    zfill_count = len(str(count - 1))

    # Create output directory if it doesn't exist
    if not os.path.exists(op_path):
        os.makedirs(op_path)


    generated_count = 0
    bar = progressbar.ProgressBar(max_value=count)
    if is_random:
         # Create ramdom images
        for n in range(count):

            # Set image name
            image_name = str(n).zfill(zfill_count) + '.png'

            # Get a random set of valid traits based on rarity weights
            trait_sets, trait_paths = generate_random_trait_set_from_config()

            # Generate the actual image
            generate_single_image(trait_paths, os.path.join(op_path, image_name), compression_ratio)

            # Populate the rarity table with metadata of newly created image
            for idx, trait in enumerate(trait_sets):
                if trait is not None:
                    rarity_table[CONFIG[idx]['name']].append(trait[: -1 * len('.png')])
                else:
                    rarity_table[CONFIG[idx]['name']].append('none')

            
            generated_count = generated_count + 1
            bar.update(generated_count)
    
    else:
        # BIG ASSUMPTION!! Assume there are always 5 layers.
        LAYER_1_COUNT = 4
        LAYER_2_COUNT = 5
        LAYER_3_COUNT = 5
        LAYER_4_COUNT = 5
        LAYER_5_COUNT = 4

        current_index = 0
        selected_indexes = [20, 21, 23, 24, 25, 27, 28, 29, 31, 32, 33, 35, 36, 37, 39, 80, 84, 88, 92, 96, 100, 104, 108, 109, 112, 113, 116, 117, 120, 121, 123, 124, 125, 127, 128, 129, 131, 132, 133, 135, 136, 137, 139, 140, 142, 144, 146, 148, 150, 152, 154, 156, 158, 160, 161, 162, 164, 166, 168, 169, 170, 172, 174, 176, 177, 178, 281, 282, 285, 286, 289, 290, 293, 294, 297, 298, 301, 302, 305, 306, 309, 310, 313, 314, 317, 318, 382, 383, 386, 387, 390, 391, 394, 398, 600, 603, 604, 607, 608, 611, 612, 615, 616, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 642, 646, 650, 654, 658, 702, 703, 706, 707, 710, 711, 714, 715, 718, 719, 722, 726, 730, 734, 738, 741, 745, 749, 753, 757, 821, 825, 829, 833, 837, 921, 925, 929, 933, 937, 940, 944, 948, 952, 956, 1102, 1106, 1110, 1114, 1118, 1121, 1122, 1123, 1125, 1126, 1127, 1129, 1130, 1131, 1133, 1134, 1135, 1137, 1138, 1139, 1143, 1147, 1151, 1155, 1159, 1222, 1226, 1230, 1234, 1238, 1260, 1263, 1264, 1268, 1271, 1272, 1275, 1276, 1279, 1280, 1281, 1283, 1284, 1285, 1287, 1288, 1289, 1291, 1292, 1293, 1295, 1296, 1297, 1299, 1300, 1303, 1304, 1308, 1311, 1312, 1316, 1319, 1360, 1362, 1364, 1366, 1367, 1368, 1370, 1372, 1374, 1375, 1376, 1378, 1379, 1407, 1415, 1420, 1421, 1424, 1425, 1428, 1429, 1432, 1433, 1436, 1437, 1471, 1480, 1482, 1483, 1484, 1486, 1487, 1488, 1490, 1491, 1492, 1494, 1495, 1496, 1498, 1623, 1627, 1631, 1635, 1639, 1661, 1663, 1665, 1667, 1669, 1671, 1673, 1675, 1677, 1679, 1720, 1722, 1724, 1726, 1728, 1730, 1732, 1734, 1736, 1738, 1741, 1743, 1745, 1747, 1749, 1751, 1753, 1755, 1757, 1759, 1765, 1773, 1801, 1806, 1809, 1814, 1817, 1882, 1883, 1885, 1887, 1889, 1890, 1891, 1893, 1895, 1897, 1898, 1899]

        bar = progressbar.ProgressBar(max_value=count)
        for i1 in range(LAYER_1_COUNT):
            for i2 in range(LAYER_2_COUNT):
                for i3 in range(LAYER_3_COUNT):
                    for i4 in range(LAYER_4_COUNT):
                        for i5 in range(LAYER_5_COUNT):

                            if current_index in selected_indexes:

                                # Set image name
                                image_name = str(current_index).zfill(zfill_count) + '.jpg'

                                # Get a random set of valid traits based on rarity weights
                                trait_sets, trait_paths = generate_predefined_trait_set_from_config([i1, i2, i3, i4, i5])

                                # Generate the actual image
                                generate_single_image(trait_paths, os.path.join(op_path, image_name), compression_ratio)

                                # Populate the rarity table with metadata of newly created image
                                for idx, trait in enumerate(trait_sets):
                                    if trait is not None:
                                        rarity_table[CONFIG[idx]['name']].append(trait[: -1 * len('.png')])
                                    else:
                                        rarity_table[CONFIG[idx]['name']].append('none')

                            else:
                                print(f'{current_index} is not selected')
                        
                            current_index = current_index + 1
                            bar.update(current_index)


    # Create the final rarity table by removing duplicate creat
    rarity_table = pd.DataFrame(rarity_table).drop_duplicates()
    print("Generated %i images, %i are distinct" % (count, rarity_table.shape[0]))

    if drop_dup:
        # Get list of duplicate images
        img_tb_removed = sorted(list(set(range(count)) - set(rarity_table.index)))

        # Remove duplicate images
        print("Removing %i images..." % (len(img_tb_removed)))

        #op_path = os.path.join('output', 'edition_' + str(edition))
        for i in img_tb_removed:
            os.remove(os.path.join(op_path, str(i).zfill(zfill_count) + '.png'))

        # Rename images such that it is sequentialluy numbered
        for idx, img in enumerate(sorted(os.listdir(op_path))):
            os.rename(os.path.join(op_path, img), os.path.join(op_path, 'Amuro_' + brand_name + '_Avatar_' + str(idx).zfill(zfill_count) + '.png'))


    # Modify rarity table to reflect removals
    rarity_table = rarity_table.reset_index()
    rarity_table = rarity_table.drop('index', axis=1)
    return rarity_table

# Main function. Point of entry
def main(num_of_img, name_of_edition, name_of_brand, is_random, compression_ratio, de_dup):

    print("Checking assets...")
    parse_config()
    print("Assets look great! We are good to go!")
    print()

    tot_comb = get_total_combinations()
    print("You can create a total of %i distinct avatars" % (tot_comb))
    print()

    # print("How many avatars would you like to create? Enter a number greater than 0: ")
    # while True:
    #     num_avatars = int(input())
    #     if num_avatars > 0:
    #         break

    # print("What would you like to call this edition?: ")
    # edition_name = input()

    edition_name = name_of_edition
    num_avatars = int(num_of_img)
    print("Starting task...")
    rt = generate_images(edition_name, num_avatars, name_of_brand, is_random, compression_ratio, de_dup)

    print("Saving metadata...")
    rt.to_csv(os.path.join('static', 'output', 'edition_' +  str(edition_name), 'metadata.csv'))

    print("Task complete!")


# Run the main function
main(2500, "v9_1_normal_final", "cmi", False, 1, False)