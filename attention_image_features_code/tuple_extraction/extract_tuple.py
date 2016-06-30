__author__ = 'pengzhang'
import json
from collections import OrderedDict
import nltk
from gensim.models import Word2Vec
from nltk.tag.hunpos import HunposTagger
from nltk.tokenize import word_tokenize

####################
# Load dataset

tuple_parsing = json.load(open('../abstract/binary_tuple_val.json'), object_pairs_hook=OrderedDict)
tuple_question = json.load(open('../abstract/binary_question_val.json', 'r'))
#####################
obj_list = json.load(open('../abstract/abstract_image_obj_list.json'))
location_list = ['bed','bar','pad','lilypad','shelf','house','coatrack','endtable','left','right','center','top',\
                 'front','middle','back','ground','cartoon','monkeybar','petbed','rope','footstool','bat']

all_obj_list = []
for i in range(len(obj_list)):
    all_obj_list += obj_list[i][str(i)]

all_obj_list = set(all_obj_list)
all_obj_list = list(all_obj_list)

location_list += all_obj_list


tuple_word = ['nsubj', 'nsubj_1', 'root', 'nsubjpass', 'case', 'nmod', 'xcomp', 'compound', 'dobj', 'acl', 'advmod', 'ccomp', \
              'nmod_1', 'case_1', 'advcl', 'compound', 'nummod', 'dep', 'amod', 'amod_1', 'dep_1', 'nmod_2', 'case_2', 'cc']
question_word = ['Is', 'Are', 'Do', 'Does', 'Will', 'Could', 'Can', 'Did', 'Would']
noun_list = ['NN', 'NNS', 'NNP', 'NNPS']
other_list = ['DT', 'PRP']
except_list = ['it', 'this', 'that', 'the']


nsubj_key = []
nsubj_question = []
nsubj_imgid = []
nsubj_tuple = []
nsubj_answer = []
nsubj_obj = []
nsubj_tag = []
nsubj_queid = []
nsubjpass_key = []
nsubjpass_question = []
nsubjpass_tuple = []
nsubjpass_imgid = []
nsubjpass_answer = []
nsubjpass_obj = []
nsubjpass_tag = []
nsubjpass_queid = []
root_key = []
root_question = []
root_tuple = []
root_imgid = []
root_answer = []
root_obj = []
root_tag = []
root_queid = []
nmod_key = []
nmod_question = []
nmod_tuple = []
nmod_imgid = []
nmod_answer = []
nmod_obj = []
nmod_tag = []
nmod_queid = []

ht = HunposTagger('../en_wsj.model')
for i in range(len(tuple_parsing)):
    question = tuple_question[i]['question']
    word_token = nltk.word_tokenize(question)
    word_tag = ht.tag(word_token)

    item = tuple_parsing[i]
    if "nsubj" in item.keys():
        ind = item.keys().index("nsubj")
        item_keys = item.keys()
        if list(word_tag[ind])[-1] not in noun_list and list(word_tag[ind])[-1] not in other_list and list(word_tag[ind])[0] not in location_list:
            if ind+1 < len(word_tag):
                if list(word_tag[ind-1])[-1] in noun_list or list(word_tag[ind])[0] in location_list:
                    sent_tuple_key_tmp = item_keys[ind-1:len(item_keys)]
                elif list(word_tag[ind+1])[-1] in noun_list or list(word_tag[ind])[0] in location_list:
                    sent_tuple_key_tmp = item_keys[ind:len(item_keys)]
                else:
                    sent_tuple_key_tmp = item_keys[ind+1:len(item_keys)]
            else:
                if list(word_tag[ind-1])[-1] in noun_list or list(word_tag[ind])[0] in location_list:
                    sent_tuple_key_tmp = item_keys[ind-1:len(item_keys)]
                else:
                    sent_tuple_key_tmp = item_keys[ind:len(item_keys)]
        elif list(word_tag[ind])[-1] not in noun_list and list(word_tag[ind])[-1] in other_list:
            if list(word_tag[ind])[0] not in except_list:
                sent_tuple_key_tmp = item_keys[ind:len(item_keys)]
            else:
                sent_tuple_key_tmp = item_keys[ind+1:len(item_keys)]
        else:
            item_keys = item.keys()
            sent_tuple_key_tmp = item_keys[ind:len(item_keys)]

        for sent_key in item.keys():
            if sent_key not in sent_tuple_key_tmp or sent_key not in tuple_word:
                item.pop(sent_key)

        if 'root' in item.keys():
            question = tuple_question[i]['question']
            word_token = nltk.word_tokenize(question)
            word_tag = ht.tag(word_token)
            for word in word_tag:
                if word[-1] == 'VBG' and word[0] == item['root']:
                    item = OrderedDict([('root_doing', v) if k == 'root' else (k, v) for k, v in item.items()])
                    break

        if len(item.keys())>2:
            if item[item.keys()[0]] == item[item.keys()[1]]:
                item.pop(item.keys()[0])

        if 'dep' in item.keys():
            if item['dep'] == 'the':
                item.pop('dep')

        sent_value = []
        for tuple_key in item.keys():
            sent_value.append(item[tuple_key])



        nsubj_key.append(item.keys())
        nsubj_tuple.append(sent_value)
        nsubj_question.append(tuple_question[i]['question'])
        nsubj_imgid.append(tuple_question[i]['img_id'])
        nsubj_answer.append(tuple_question[i]['answer'])
        nsubj_obj.append(tuple_question[i]['obj'])
        nsubj_tag.append(word_tag)
        nsubj_queid.append(tuple_question[i]['question_id'])
    elif "nsubjpass" in item.keys():
        ind = item.keys().index("nsubjpass")
        item_keys = item.keys()

        if list(word_tag[ind])[-1] not in noun_list and list(word_tag[ind])[-1] not in other_list and list(word_tag[ind])[0] not in location_list:
            if ind+1 < len(word_tag):
                if list(word_tag[ind-1])[-1] in noun_list or list(word_tag[ind])[0] in location_list:
                    sent_tuple_key_tmp = item_keys[ind-1:len(item_keys)]
                elif list(word_tag[ind+1])[-1] in noun_list or list(word_tag[ind])[0] in location_list:
                    sent_tuple_key_tmp = item_keys[ind:len(item_keys)]
                else:
                    sent_tuple_key_tmp = item_keys[ind+1:len(item_keys)]
            else:
                if list(word_tag[ind-1])[-1] in noun_list or list(word_tag[ind])[0] in location_list:
                    sent_tuple_key_tmp = item_keys[ind-1:len(item_keys)]
                else:
                    sent_tuple_key_tmp = item_keys[ind:len(item_keys)]
        elif list(word_tag[ind])[-1] not in noun_list and list(word_tag[ind])[-1] in other_list:
            if list(word_tag[ind])[0] not in except_list:
                sent_tuple_key_tmp = item_keys[ind:len(item_keys)]
            else:
                sent_tuple_key_tmp = item_keys[ind+1:len(item_keys)]
        else:
            item_keys = item.keys()
            sent_tuple_key_tmp = item_keys[ind:len(item_keys)]

        for sent_key in item.keys():
            if sent_key not in sent_tuple_key_tmp or sent_key not in tuple_word:
                item.pop(sent_key)

        if len(item.keys())>2:
            if item[item.keys()[0]] == item[item.keys()[1]]:
                item.pop(item.keys()[0])

        if 'dep' in item.keys():
            if item['dep'] == 'the':
                item.pop('dep')

        sent_value = []
        for tuple_key in item.keys():
            sent_value.append(item[tuple_key])

        nsubjpass_key.append(item.keys())
        nsubjpass_tuple.append(sent_value)
        nsubjpass_question.append(tuple_question[i]['question'])
        nsubjpass_imgid.append(tuple_question[i]['img_id'])
        nsubjpass_answer.append(tuple_question[i]['answer'])
        nsubjpass_obj.append(tuple_question[i]['obj'])
        nsubjpass_tag.append(word_tag)
        nsubjpass_queid.append(tuple_question[i]['question_id'])
    else:
        if item['root'] not in question_word:
            ind = item.keys().index("root")
            item_keys = item.keys()
            sent_tuple_key_tmp = item_keys[ind:len(item_keys)]
            for sent_key in sent_tuple_key_tmp:
                if sent_key not in tuple_word:
                    item.pop(sent_key)
            item_keys = item.keys()
            sent_tuple_key = item_keys[ind:len(item_keys)]
            root_key.append(sent_tuple_key)
            sent_value = []
            for tuple_key in sent_tuple_key:
                sent_value.append(item[tuple_key])
            root_tuple.append(sent_value)
            root_question.append(tuple_question[i]['question'])
            root_imgid.append(tuple_question[i]['img_id'])
            root_answer.append(tuple_question[i]['answer'])
            root_obj.append(tuple_question[i]['obj'])
            root_tag.append(word_tag)
#             print tuple_question
            root_queid.append(tuple_question[i]['question_id'])
        else:
            if 'nmod' in item.keys():
                ind = item.keys().index('nmod')
            elif 'nummod' in item.keys():
                # print item
                ind = item.keys().index('nummod')
            else:
                print item
                ind = item.keys().index('dep')

            item_keys = item.keys()
            sent_tuple_key_tmp = item_keys[ind:len(item_keys)]
            for sent_key in sent_tuple_key_tmp:
                if sent_key not in tuple_word:
                    item.pop(sent_key)

            if 'dep' in item.keys():
                if item['dep'] == 'the':
                    item.pop('dep')

            item_keys = item.keys()
            sent_tuple_key = item_keys[ind:len(item_keys)]
            nmod_key.append(sent_tuple_key)
            sent_value = []
            for tuple_key in sent_tuple_key:
                sent_value.append(item[tuple_key])
            nmod_tuple.append(sent_value)
            nmod_question.append(tuple_question[i]['question'])
            nmod_imgid.append(tuple_question[i]['img_id'])
            nmod_answer.append(tuple_question[i]['answer'])
            nmod_obj.append(tuple_question[i]['obj'])
            nmod_tag.append(word_tag)
            nmod_queid.append(tuple_question[i]['question_id'])

    word_tag = dict(word_tag)
    k = word_tag.keys()
    t = word_tag.values()


###

tuple_anno = []
for i in range(len(nsubj_key)):
    tuple_tmp = {}
    train_tuple_item = nsubj_key[i]
    tuple_tmp['tuple_list'] = " ".join(train_tuple_item)
    tuple_tmp['tuple_value'] = nsubj_tuple[i]
    tuple_tmp['tuple_question'] = nsubj_question[i]
    tuple_tmp['tuple_obj'] = nsubj_obj[i]
    tuple_tmp['tuple_imgid'] = nsubj_imgid[i]
    tuple_tmp['tuple_answer'] = nsubj_answer[i]
    tuple_tmp['tuple_tag'] = nsubj_tag[i]
    tuple_tmp['tuple_queid'] = nsubj_queid[i]

    tuple_anno.append(tuple_tmp)


for i in range(len(nsubjpass_key)):
    tuple_tmp = {}
    train_tuple_item = nsubjpass_key[i]
    tuple_tmp['tuple_list'] = " ".join(train_tuple_item)
    tuple_tmp['tuple_value'] = nsubjpass_tuple[i]
    tuple_tmp['tuple_question'] = nsubjpass_question[i]
    tuple_tmp['tuple_obj'] = nsubjpass_obj[i]
    tuple_tmp['tuple_imgid'] = nsubjpass_imgid[i]
    tuple_tmp['tuple_answer'] = nsubjpass_answer[i]
    tuple_tmp['tuple_tag'] = nsubjpass_tag[i]
    tuple_tmp['tuple_queid'] = nsubjpass_queid[i]

    tuple_anno.append(tuple_tmp)

    
for i in range(len(nmod_key)):
    tuple_tmp = {}
    train_tuple_item = nmod_key[i]
    tuple_tmp['tuple_list'] = " ".join(train_tuple_item)
    tuple_tmp['tuple_value'] = nmod_tuple[i]
    tuple_tmp['tuple_question'] = nmod_question[i]
    tuple_tmp['tuple_obj'] = nmod_obj[i]
    tuple_tmp['tuple_imgid'] = nmod_imgid[i]
    tuple_tmp['tuple_answer'] = nmod_answer[i]
    tuple_tmp['tuple_tag'] = nmod_tag[i]
    tuple_tmp['tuple_queid'] = nmod_queid[i]

    tuple_anno.append(tuple_tmp)


for i in range(len(root_key)):
    tuple_tmp = {}
    train_tuple_item = root_key[i]
    tuple_tmp['tuple_list'] = " ".join(train_tuple_item)
    tuple_tmp['tuple_value'] = root_tuple[i]
    tuple_tmp['tuple_question'] = root_question[i]
    tuple_tmp['tuple_obj'] = root_obj[i]
    tuple_tmp['tuple_imgid'] = root_imgid[i]
    tuple_tmp['tuple_answer'] = root_answer[i]
    tuple_tmp['tuple_tag'] = root_tag[i]
    tuple_tmp['tuple_queid'] = root_queid[i]

    tuple_anno.append(tuple_tmp)

############
json.dump(tuple_anno, open('../abstract/binary_extracted_val.json','w'))
############
# #save for later
# for i in range(len(train_tuple_tag_all)):
#     sent_part = word_tokenize(train_tuple_question[i])
#     tuple_part = train_tuple_value[i]
#     tuple_tag = []
#     for item in tuple_part:
#         tuple_tag.append(train_tuple_tag_all[i][sent_part.index(item)])
#
#     train_tuple_tag.append(tuple_tag)