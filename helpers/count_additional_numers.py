#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import re
import html

counter_better = 0
counter_total = 0
with open(os.path.join("..", "data", "features" ,"00_00_training_features.json"), "r") as fr:
    data = json.load(fr)
    for entry in data:
        counter_total += 1
        if len(entry["target_num"]) < len(entry["features"]["numbers"]):
            counter_better += 1
            print(entry["idx"])
print("total %s" % counter_total)
print("better %s" % counter_better)
print("persentage  1 %s" % (counter_better / (counter_total / 100)))
print("persentage  2 %s" % (counter_better * 100 / counter_total))