import json
import os

data = json.load(open(os.path.join("..", "data", "features" ,"all_features_5.json")))

dictionary_map = {}

for entry in data:
    for term in entry["features"]["tickers"]:
        if term not in dictionary_map:
            dictionary_map[term] = len(dictionary_map)

print("Dictionary is buit, size: %s, start to work" % len(dictionary_map))

for entry in data:
    tickers_vectors = [0] * len(dictionary_map)
    for ticker in entry["features"]["tickers"]:
        tickers_vectors[dictionary_map[ticker]] += 1
    entry["features"]["tickers_vectors"] = tickers_vectors

json.dump(data, open(os.path.join("..", "data", "features" ,"all_features_6.json"), "w"))

