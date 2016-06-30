__author__ = 'pengzhang'
# This function reads in parsing results and save as a file

import json
import re
from collections import OrderedDict

# Training
train_parse_txt = open('../abstract/abstract_binary_train_out.txt', 'r')
train_sent_tuple = []
sent_item = OrderedDict()
count = 0
for line in train_parse_txt:
    line = re.sub("[^a-zA-Z0-99()]", " ", line).split()
    if len(line):
        if line[0][0:5] == "(ROOT":
            train_sent_tuple.append(sent_item)
            sent_item = OrderedDict()
            count += 1
            # print line
        if not line[0][0] == '(':
            line_label = re.sub("[^a-zA-Z0-99]", " ", line[0]).split()
            if line_label[0] in sent_item.keys():
                if line_label[0] + '_1' not in sent_item.keys():
                    # if line_label[0] == 'nsubj':
                    #     sent_item[line_label[0]] = sent_item.pop(line_label[0])
                    #     sent_item[line_label[0]] = line[-2]
                    # else:
                    sent_item[line_label[0] + '_1'] = line[-2]
                else:
                    sent_item[line_label[0] + '_2'] = line[-2]
            else:
                sent_item[line_label[0]] = line[-2]
            
train_sent_tuple.pop(0)
sent_tuple = open('../abstract/binary_tuple_train.json', 'w')
json.dump(train_sent_tuple, sent_tuple, sort_keys=False)


# Testing
val_parse_txt = open('../abstract/abstract_binary_val_out.txt', 'r')
val_sent_tuple = []
sent_item = OrderedDict()
count = 0
for line in val_parse_txt:
    line = re.sub("[^a-zA-Z0-99()]", " ", line).split()
    if len(line):
        if line[0][0:5] == "(ROOT":
            val_sent_tuple.append(sent_item)
            sent_item = OrderedDict()
            count += 1
            # print line
        if not line[0][0] == '(':
            line_label = re.sub("[^a-zA-Z0-99]", " ", line[0]).split()
            if line_label[0] in sent_item.keys():
                if line_label[0] + '_1' not in sent_item.keys():
                    # if line_label[0] == 'nsubj':
                    #     sent_item[line_label[0]] = sent_item.pop(line_label[0])
                    #     sent_item[line_label[0]] = line[-2]
                    # else:
                    sent_item[line_label[0] + '_1'] = line[-2]
                else:
                    sent_item[line_label[0] + '_2'] = line[-2]
            else:
                sent_item[line_label[0]] = line[-2]

val_sent_tuple.pop(0)
sent_tuple = open('../abstract/binary_tuple_val.json', 'w')
json.dump(val_sent_tuple, sent_tuple, sort_keys=False)
