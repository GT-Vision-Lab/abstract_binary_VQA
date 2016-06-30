__author__ = 'pengzhang'
# New Version
# chunking the tuples into three arguments
import copy
import json
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag.hunpos import HunposTagger

###############
# load data
tuple_anno = json.load(open('../abstract/binary_extracted_train.json'))
###############
ht = HunposTagger('../en_wsj.model')

p_list = ['NN','NNS','NNP','NNPS','PRP','PRP$','UH']
s_list = ['NN','JJ','JJS','JJR','DT','NNS','NNP','NNPS','PRP','PRP$']
s_jj_list = ['JJ','JJS','JJR','DT']
verb_list = ['VB','VBG','VBD','VBZ','VBN','VBP']

obj_list = json.load(open('../abstract/abstract_obj_list.json'))
location_list = ['bed','bar','pad','lilypad','shelf','house','coatrack','endtable','left','right','center','top',\
                 'front','middle','back','ground','cartoon','monkeybar','petbed','rope','footstool','bat']

all_obj_list = []
for i in range(len(obj_list)):
    all_obj_list += obj_list[i].values()[0]

all_obj_list = set(all_obj_list)
all_obj_list = list(all_obj_list)

location_list += all_obj_list


first_ind = []
relation_ind = []
second_ind = []
# for n in range(5000):
for n in range(len(tuple_anno)):
    tuple_value = tuple_anno[n]['tuple_value']
    tuple_list = tuple_anno[n]['tuple_list']
    tuple_question = tuple_anno[n]['tuple_question']

    item = copy.deepcopy(tuple_value)  # extracted tuple
    parsing = copy.deepcopy(tuple_list)  # parsing results
    question = copy.deepcopy(tuple_question)  # question

    # POS tagging the whole sentence, tags in entity list, words in words list
    question = re.sub("'s","",question)
    question = re.sub("'o","",question)
    question = re.sub("[^a-zA-z0-99]", " ", question)
    question_token = word_tokenize(question)
    question_tag = ht.tag(question_token)
    words = item
    entity = []
    new_item = []
    for w in words:
        w_tag = ht.tag(word_tokenize(w))    # POS tag for each word
        nltk_tag = nltk.pos_tag(word_tokenize(w))
        if not w in question_token:     # Remember to fix this, this happens when 's appears
            continue
        new_item.append(w)
        word_ind = question_token.index(w)
        entity_tmp = list(question_tag[word_ind])

        if w_tag[0][1] in verb_list:
            entity_tmp[1] = w_tag[0][1]
        elif nltk_tag[0][1] == 'VBG':
            entity_tmp[1] = nltk_tag[0][1]

        # if w_tag[0][1] in verb_list or nltk_tag[0][1] == 'VBG':
        #     entity_tmp[1] = 'VBG'
        
        entity.append(entity_tmp)
        
    p_tag_ind = []
    r_tag_ind = []
    
    # split parsing results
    parsing_split = word_tokenize(parsing)
    
    # chunk nouns
    if 'nsubj' in parsing_split or 'nsubjpass' in parsing_split or 'nsubj_1' in parsing_split:
        if 'nsubj' in parsing_split:
            nsubj_ind = parsing_split.index('nsubj') # the reference point
        elif 'nsubjpass' in parsing_split:
            nsubj_ind = parsing_split.index('nsubjpass')
        else:
            nsubj_ind = parsing_split.index('nsubj_1')
        
        nsubj_tmp = []
        if entity[nsubj_ind][1] not in p_list and words[nsubj_ind] not in location_list:
            # nsubj has to be a noun
            for k in range(nsubj_ind):
                if entity[k][1] in p_list or words[k] in location_list:
                    nsubj_tmp.append(k)
            if not nsubj_tmp:
                for k in range(nsubj_ind,len(entity),1):
                    if entity[k][1] in p_list or words[k] in location_list:
                        nsubj_tmp.append(k)
            
            if not nsubj_tmp: # if nothing satisfied, e.g. moose, not in location_list, tagged as JJ
                nsubj_ind = len(entity)-1
            else:
                nsubj_ind = nsubj_tmp[0]
            
        
        if 'nsubj_1' in parsing_split and 'cc' in parsing_split:
            nsubj_ind = parsing_split.index('nsubj_1')
        if nsubj_ind < len(entity) - 3 and entity[nsubj_ind + 1][1] == 'IN':
            if words[nsubj_ind + 2] in location_list:
                if words[nsubj_ind + 2] == 'front' and words[nsubj_ind + 3] == 'of':
                    # e.g. something "in front of" something
                    # exception: boy in front of the dog playing with toy
                    nsubj_ind = nsubj_ind
                else:
                    # e.g. man in couch
                    nsubj_ind = nsubj_ind + 2
            else:
                if nsubj_ind < len(entity)-4:
                    if entity[nsubj_ind + 2][1] in s_jj_list and entity[nsubj_ind + 3][1] in p_list:
                        # e.g. man in red shirt
                        nsubj_ind = nsubj_ind + 3
        
        p_tag_ind.append(nsubj_ind)
    else:
        flag = 0
        first_noun = 0
        for i in range(len(entity)):
            if entity[i][1] in p_list and not first_noun:
                first_noun = 1
                flag = 1
                nsubj_ind = i
                p_tag_ind.append(nsubj_ind)
            elif entity[i][1] in p_list and flag and first_noun:
                nsubj_ind = i
                p_tag_ind.append(nsubj_ind)
            else:
                break
    
    
    # nothing in the noun index list
    if not p_tag_ind:
        nsubj_ind = len(entity)-1
        p_tag_ind.append(nsubj_ind)


    # chunk for S list
    new_entity = entity[nsubj_ind+1:]
    new_words = words[nsubj_ind+1:]

    
    s_tag_ind = []
    for i in range(len(new_entity)):
        if new_entity[i][1] in s_list:
            if i == len(new_entity)-1:
                if new_entity[i][1] in p_list or new_words[i] in location_list:
                    # index is the last word, e.g. cat in room
                    s_tag_ind.append(i)
            else:
                if i < len(new_entity)-1:
                    if new_entity[i][1] in s_jj_list and new_entity[i+1][1] in s_list:
                        # e.g. they wearing same pants
                        s_tag_ind.append(i)
                        break
                    elif new_entity[i][1] in p_list:
                        # e.g. anything on coffee table
                        s_tag_ind.append(i)
                        if i < len(new_entity)-2:
                            # something in front of something, something having fun with something
                            if new_words[i] == 'front' or new_words[i] == 'fun':
                                if new_entity[i+1][1] == 'IN':
                                    s_tag_ind.append(i+2)
                                    break
                                else:
                                    break
                            else:
                                break
                        else:
                            break
                  
    if len(s_tag_ind):
        dobj_ind = s_tag_ind[-1] + nsubj_ind + 1
    else:
        dobj_ind = []

    # chunk for R list
    if nsubj_ind < len(entity)-1:
        if not dobj_ind:
            rel_ind = range(nsubj_ind+1,len(entity),1)
        else:
            rel_ind = range(nsubj_ind+1,dobj_ind,1)
    else:
        rel_ind = []
        dobj_ind = []
        
    second_ind.append(dobj_ind)
    first_ind.append(nsubj_ind)
    relation_ind.append(rel_ind)


chunk_tuple = []
for i in range(len(first_ind)):
    pre_chunk = {}
    p_tuple = []
    r_tuple = []
    s_tuple = []

    tuple_item = copy.deepcopy(tuple_anno[i]['tuple_value'])

    for m in range(first_ind[i]+1):
        p_tuple.append(tuple_item[m])
    if relation_ind[i]:
        for n in relation_ind[i]:
            r_tuple.append(tuple_item[n])
    if second_ind[i]:
        for k in range(second_ind[i],len(tuple_item),1):
            s_tuple.append(tuple_item[k])
    pre_chunk['question'] = tuple_anno[i]['tuple_question']
    pre_chunk['tuple'] = tuple_item
    pre_chunk['primary'] = p_tuple
    pre_chunk['relation'] = r_tuple
    pre_chunk['secondary'] = s_tuple
    pre_chunk['obj'] = tuple_anno[i]['tuple_obj']
    pre_chunk['queid'] = tuple_anno[i]['tuple_queid']

    chunk_tuple.append(pre_chunk)

############
json.dump(chunk_tuple,open('../abstract/binary_train_chunk.json','w'))