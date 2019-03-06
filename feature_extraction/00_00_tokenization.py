#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import re
import html
# read file as json
# iterate over list of objects
# pass object to a feature extraction function

# feature extraction function
# 1: token is a sequence of chars in the same domain (letters, digits, symbols etc)
char_type = {}
for c in "0123456789":
    char_type[c] = 0

for c in "abcdefghijklmnopqrstuvwxyz":
    char_type[c] = 1

for c in "|~™¡¢£¦¨á!\"#$%&'( )*+,-./[ ]^_:;<=>?@.{}\\®\x08":
    char_type[c] = 3

for c in " \t\n":
    char_type[c] = 4

system_tokens = set([
    "systicker",
    "sysurl",
    "sysfloats",
    "sysints"
])

def tokenize(input):
    input = html.unescape(input)
    input = html.unescape(input)

    tickers = re.findall(r"\$[A-Z-_\.]{1,8}", input)
    input = re.sub(r"\$[A-Z-_\.]{1,8}", "systicker", input)

    urls = re.findall(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(?:/[-_\w]+)*/?(?:\?[=&\w\d\-\_]+)*", input)
    input = re.sub(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(?:/[-_\w]+)*/?(?:\?[=&\w\d\-\_]+)*", "sysurl", input)
    
    tags = re.findall(r"#[A-Za-z]{1,15}", input)
    input = re.sub(r"#[A-Za-z]{1,15}", "", input)
    
    #many dots and number
    input = re.sub(r"(?P<dots>\.{2,10})(?P<number>\d)", r"\g<dots> \g<number>", input)
    
    floats = re.findall(r"\d*(?:\,\d+)*\.\d+", input)
    input = re.sub(r"\d*(?:\,\d+)*\.\d+", " sysfloats ", input)
    
    ints = re.findall(r"\d+(?:\,\d\d\d)*", input)
    input = re.sub(r"\d+(?:\,\d\d\d)*", " sysints ", input)

    prev_c_type = None
    current_token = []
    tokens_terms = []
    for c in input.lower():
        type_c = char_type[c]

        if type_c != prev_c_type:
            if len(current_token):
                tokens_terms.append("".join(current_token))
            
            if type_c == 4:
                current_token = []
            else:    
                current_token = [c]
        elif type_c == 3:
            if len(current_token):
                tokens_terms.append("".join(current_token))
            current_token = [c]        
        else:
            current_token.append(c)
        
        if type_c == 4:
            prev_c_type = None
        else:    
            prev_c_type = type_c

    numbers = []
    i_ints = 0
    i_floats = 0
    for i_numders, token in enumerate(tokens_terms):
        if token == "sysfloats":
            numeric_value = floats[i_floats]
            i_floats += 1
            numbers.append({
                "index_terms": i_numders,
                "value": numeric_value,
                "isInt": False,
            })
        elif token == "sysints":
            numeric_value = ints[i_ints]
            i_ints += 1
            numbers.append({
                "index_terms": i_numders,
                "value": numeric_value,
                "isInt": True,
            })

    tokens_symbols = []
    for term in tokens_terms:
        if term not in system_tokens:
            for symbol in term:
                tokens_symbols.append(symbol)
        else:
            tokens_symbols.append(term)
    
    i_numders = 0
    for indx, token in enumerate(tokens_symbols):
        if token == "sysfloats" or token == "sysints":
            numbers[i_numders]["index_symbols"] = indx
            i_numders += 1


    return {
        "numbers": numbers,
        "tokens_terms": tokens_terms,
        "tokens_symbols": tokens_symbols,
        "urls": urls,
        "tags": tags,
        "tickers": tickers
    }

results = {}
files = ["FinNum_test_all_without_GS.json", "FinNum_dev_all_with_GS.json", "FinNum_train_all_with_GS.json"]

for json_file in files:
    with open(os.path.join("..", "data", "raw", json_file), "r") as fr:
        data = json.load(fr)
        for entry in data:
            if entry["idx"] in results:
                print("Warning: we have it already")
                print(entry)
                print(results[entry["idx"]])
                continue
            entry["features"] = tokenize(entry["tweet"])
            results[entry["idx"]] = entry    

json.dump([x for x in results.values()], open(os.path.join("..", "data", "features" ,"all_features_0.json"), "w"))