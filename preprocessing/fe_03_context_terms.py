import json
import os

data = json.load(open(os.path.join("..", "data", "features" ,"all_features_2.json"))

dictionary_map = {}

for entry in data:
    for term in entry["features"]["tokens_terms"]:
        if term not in dictionary_map:
            dictionary_map[term] = len(dictionary_map)

N = 3

print("Dictionary is buit, size: %s, start to work n = %s" % (len(dictionary_map), N))

for entry in data:
    tokens = entry["features"]["tokens_terms"]
    num_tokens = len(tokens)
    context_vectors = []
    for num in entry["features"]["numbers"]:
        context = [0] * len(dictionary_map)
        token_indx = num["index_terms"]
        left_indx = max(0, token_indx - N)
        right_indx = min(num_tokens - 1, token_indx + N + 1)
        indises = list(range(left_indx, token_indx)) + list(range(token_indx + 1, right_indx))
        for i in indises:
            context[dictionary_map[tokens[i]]] += 1
        context_vectors.append(context)
    entry["features"]["target_num_terms_context_vectors"] = context_vectors

json.dump(data, open(os.path.join("..", "data", "features" ,"all_features_3.json"), "w"))

