import json
import os

data = json.load(open(os.path.join("..", "data", "features" ,"all_features_4.json")))

dictionary_map = {}

for entry in data:
    for term in entry["features"]["tags"]:
        if term not in dictionary_map:
            dictionary_map[term] = len(dictionary_map)

print("Dictionary is buit, size: %s, start to work" % len(dictionary_map))

for entry in data:
    tags_vectors = [0] * len(dictionary_map)
    for tag in entry["features"]["tags"]:
        tags_vectors[dictionary_map[tag]] += 1
    entry["features"]["tags_vectors"] = tags_vectors

json.dump(data, open(os.path.join("..", "data", "features" ,"all_features_5.json"), "w"))

