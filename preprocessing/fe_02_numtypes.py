import json
import os
import math
import re

data = json.load(open(os.path.join("..", "data", "features" ,"all_features_1.json")))

# loop through document list
missings_amount = 0

for entry in data:
    features = entry["features"]
    len_tokens = 1.0 * len(features["tokens_terms"]) 
    my_numbers = features["numbers"]
    for num in my_numbers:

        numeric_value = None
        if num["isInt"]:
            numeric_value = int(re.sub(r"[^\d]", "", num["value"]))
        else:
            numeric_value = float(re.sub(r"[^\d\.]", "", num["value"]))

        num_range = 0
        if numeric_value > 0:
            num_range = math.log10(numeric_value)

        #value
        #is int
        #is float
        #position
        #log in the sense of range
        num["key"] = re.sub(r"[^\d]", "", num["value"])
        num["features_vector"] = [
            numeric_value,
            1 if num["isInt"] else 0,
            0 if num["isInt"] else 1,
            num["index_terms"] / len_tokens,
            num_range
        ]    

    #test on presents of target numbers
    features["target_num_feature_vectors"] = []
    last_hit = -1
    for indx, target_number in enumerate(entry["target_num"]):
        target_key = re.sub(r"[^\d]", "", target_number)
        hit = None
        for my_num_indx in range(last_hit + 1, len(my_numbers)):
            if target_key == my_numbers[my_num_indx]["key"]:
                last_hit = my_num_indx
                hit = my_numbers[my_num_indx]["features_vector"]
                break

        features["target_num_feature_vectors"].append(hit)

        if hit is None:
            missings_amount += 1
            print("Missing number %s in entry with id: %s" % (target_number, entry["idx"]))
        

json.dump(data, open(os.path.join("..", "data", "features" ,"all_features_2.json"), "w"))
print("Total missing %s" % missings_amount)

