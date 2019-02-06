import toxicity_scrape

import glob
import os
import pandas as pd
import json

import argparse


def fix_trainval_paths(dataroot):
    '''
    1.  There are mismatches between actual file names and file names in train.json
        Luckily images are all put in folders starting with an id. This function uses
        that fact to fix train.json and val.json (which is the same).

    2.  Some image files contain ':' in the meta data when the actual file has '_' in the same spot
    '''

    def fix_paths(meta_dict, actual_dirnames):

        print("extracting unique dirnames..")
        meta_dirnames = set([os.path.basename(os.path.dirname(image["file_name"])) for image in meta_dict["images"]])
        print("found:",len(meta_dirnames))

        faulty = meta_dirnames.difference(actual_dirnames)
        corrections = actual_dirnames.difference(meta_dirnames)

        print("%d mismatches found"%len(faulty))
        print("%d corrections found"%len(corrections))

        l1=list(faulty)
        # l1.sort()
        # l2=list(corrections)
        # l2.sort()
        # for elem in zip(l1,l2):
        #     print (elem[0],"-->",elem[1])
        # all dir names start with 5 digits,
        # make lookup tables with these digits as keys:
        faulty_lookup = {}
        corrections_lookup = {}
        for dirname in faulty:
            faulty_lookup[dirname[:5]] = dirname
        for dirname in corrections:
            corrections_lookup[dirname[:5]] = dirname

        print("fixing paths..")
        for image in meta_dict["images"]:

            # some image filenames contain ':' in the meta but '_' in the actual file names
            image["file_name"] = image["file_name"].replace(":","_")

            # fix dirnames
            dirname = os.path.basename(os.path.dirname(image["file_name"]))
            key = dirname[:5]
            if key in faulty_lookup:
                if faulty_lookup[key] in image["file_name"]:
                    image["file_name"] = image["file_name"].replace(faulty_lookup[key], corrections_lookup[key])

    imagedir = os.path.join(dataroot,"images")
    print("glob..")
    image_files = glob.glob(imagedir+"/**/*.jpg",recursive=True)
    print("extracting unique glob dirnames..")
    actual_dirnames = set([os.path.basename(os.path.dirname(path)) for path in image_files])

    print("train.json")
    with open(os.path.join(dataroot,"train.json"),"r") as file:
        trainmeta = json.load(file)
    fix_paths(trainmeta, actual_dirnames)
    with open(os.path.join(dataroot,"train_fixed.json"),"w") as file:
        json.dump(trainmeta, file)

    print("val.json")
    with open(os.path.join(dataroot,"val.json"),"r") as file:
        valmeta = json.load(file)
    fix_paths(valmeta, actual_dirnames)
    with open(os.path.join(dataroot,"val_fixed.json"),"w") as file:
        json.dump(valmeta, file)

    print("done!")


# TODO: Make csv with all known names from the image dataset.
# Need to keep track of which mushrooms we are missing 1: image data for, 2: toxicity data
# ALSO: As we are bound to end up with several sources of toxicity data, these may contradict each other.
# Names may differ etc. A manifest of names will be central. So start from the image data labels.


# TODO: from image-meta: json containing dict {cat_id:cat_name}
# TODO: from image-meta/toxicity data: json {mushroom_name:is_edible}
# TODO: from image-meta/toxicity data: json that maps different spellings to one mushroom name, if needed (at least make a study of this)
def build_decode_dict(dataroot):
    with open(os.path.join(dataroot,"train.json"),"r") as file:
        trainmeta = json.load(file)
    decoder = {}
    for elem in trainmeta["categories"]:
        decoder[elem['id']]=elem['name'].lower()

    filename = os.path.join(dataroot,"decode_dict.json")
    with open(filename,"w") as file:
        json.dump(decoder, file)

def build_edible_dict(dataroot):
    edible_csv = os.path.join(dataroot,"edible.csv")
    if not os.path.isfile(edible_csv):
        Exception("'edible.csv' missing! Run toxicity_scrape.get_wiki_category_names() first")

    edible_df = pd.read_csv(edible_csv)
    edible_dict = {}
    for elem in edible_df.values:
        edible_dict[elem[1].lower()]=elem[2]

    edible_dict_file = os.path.join(dataroot, "edible.json")
    with open(edible_dict_file,"w") as file:
        json.dump(edible_dict, file)


def check_name_overlap(dataroot):
    edible_dict_file = os.path.join(dataroot, "edible.json")
    with open(edible_dict_file, "r") as file:
        edible_dict = json.load(file)

    with open(os.path.join(dataroot,"train.json"),"r") as file:
        trainmeta = json.load(file)
    image_cat_names = set([elem["name"].lower() for elem in trainmeta["categories"]])

    edible_names = set(edible_dict.keys())

    # category names without edible information:
    russian_roulette_shrooms = image_cat_names.difference(edible_names)

    # edible/poisonous mushrooms without image data (or name mismatches)
    no_image_data_shrooms = edible_names.difference(image_cat_names)

    working_list = image_cat_names.intersection(edible_names)

    return working_list, russian_roulette_shrooms, no_image_data_shrooms




if __name__ == "__main__":
    dataroot = r"data"

    # fix_trainval_paths(dataroot)
    #
    # df = toxicity_scrape.get_wiki_category_names()
    # df.to_csv(os.path.join(dataroot,"edible.csv"))
    build_decode_dict(dataroot)
    build_edible_dict(dataroot)
    working_list, russian_roulette_shrooms, no_image_data_shrooms = check_name_overlap(dataroot)
