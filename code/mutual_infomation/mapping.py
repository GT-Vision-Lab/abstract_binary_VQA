# Author Peng Zhang
# This function is used to build connection between objects and words, 
# which has two steps, 1. Build co-occurrence matrix for each scene 2. Compute mutual information in Matlab.
# declare all the package here
import json
import numpy as np
import scipy.io as sio
import os
import copy

# List all the obj in the training set
obj_data = json.load(open('../abstract/binary_train_image_obj_list.json'))
all_obj = []
for ii in obj_data:
    all_obj += ii.values()[0]
    
all_obj = list(set(all_obj))
print len(all_obj)

# Change some object names to be readable
show_obj = copy.deepcopy(all_obj)
for i in range(len(all_obj)):
    if all_obj[i] == 'Doll01':
        show_obj[i] = 'brunette black man'
    if all_obj[i] == 'Doll02':
        show_obj[i] = 'brunette black woman'
    if all_obj[i] == 'Doll03':
        show_obj[i] = 'blond white man'
    if all_obj[i] == 'Doll04':
        show_obj[i] = 'blond white woman'
    if all_obj[i] == 'Doll05':
        show_obj[i] = 'brunette brown man'
    if all_obj[i] == 'Doll06':
        show_obj[i] = 'brunette brown woman'
    if all_obj[i] == 'Doll07':
        show_obj[i] = 'white old man'
    if all_obj[i] == 'Doll08':
        show_obj[i] = 'white old woman'
    if all_obj[i] == 'Doll09':
        show_obj[i] = 'bald brown old man'
    if all_obj[i] == 'Doll10':
        show_obj[i] = 'brown old woman'
    if all_obj[i] == 'Doll11':
        show_obj[i] = 'brunette white young man'
    if all_obj[i] == 'Doll12':
        show_obj[i] = 'redhead white young woman'
    if all_obj[i] == 'Doll13':
        show_obj[i] = 'brunette brown young man'
    if all_obj[i] == 'Doll14':
        show_obj[i] = 'brunette brown young woman'
    if all_obj[i] == 'Doll15':
        show_obj[i] = 'redhead white boy'
    if all_obj[i] == 'Doll16':
        show_obj[i] = 'blond white girl'
    if all_obj[i] == 'Doll17':
        show_obj[i] = 'brunette brown boy'
    if all_obj[i] == 'Doll18':
        show_obj[i] = 'brunette brown girl'
    if all_obj[i] == 'Doll19':
        show_obj[i] = 'white baby'
    if all_obj[i] == 'Doll20':
        show_obj[i] = 'brown baby'
        
## Build co-occurrence matrix
# We only use true pairs
obj_tuple_all = json.load(open('../abstract/binary_train_chunk.json'))
ans_data = json.load(open('../abstract/binary_extracted_train.json'))

obj_tuple = []
for i in range(len(obj_tuple_all)):
    if ans_data[i]['tuple_answer'] == 'yes':
        obj_tuple.append(obj_tuple_all[i])
        
# Load training json files
listing = os.listdir("../abstract_images/scene_json_abstract_v002_train2015/")

# Collect the image names for living and park scenes
park_list = []
living_list = []
for i in range(len(listing)):
    img = json.load(open('../abstract_images/scene_json_abstract_v002_train2015/'+listing[i]))
    img_name = listing[i][24:-5].lstrip('0')
    if not img_name:
        img_name = '0'
    if img['scene']['sceneType'][0] == 'P':
        park_list.append(img_name)
    elif img['scene']['sceneType'][0] == 'L':
        living_list.append(img_name)
        
json.dump(living_list,open('../abstract/abstract_living_list.json','w'))
json.dump(park_list,open('../abstract/abstract_park_list.json','w'))

# Which tuple belongs to park, and which long to living room
park_tuple = []
park_ans = []
living_tuple = []
living_ans = []
for i in range(len(ans_data)):
    if str(ans_data[i]['tuple_imgid']) in park_list:
        park_tuple.append(obj_tuple_all[i])
        park_ans.append(ans_data[i])
    elif str(ans_data[i]['tuple_imgid']) in living_list:
        living_tuple.append(obj_tuple_all[i])
        living_ans.append(ans_data[i])
        
# for living scenes
obj_tuple_living = []
for i in range(len(living_ans)):
    if living_ans[i]['tuple_answer'] == 'yes':
        obj_tuple_living.append(living_tuple[i])

# compute both the p set and s set into one matrix
p_list = []
r_list = []
s_list = []
for item in obj_tuple_living:
    # split into each word
    p_list.append(" ".join(item['primary']))
    s_list.append(" ".join(item['secondary']))
    
p_set = set(p_list)
s_set = set(s_list)

p_set_list = list(p_set)
s_set_list = list(s_set)

ind_all = []
val_all = []
num_all = []

# Merge the words in P and S
p_set_list += s_set_list
p_set_list = list(set(p_set_list))
p_list += s_list

# Sort the word in frequency decreasing order
for i in range(len(p_set_list)):
    tmp = p_set_list[i]
    indices = [ii for ii, x in enumerate(p_list) if x == tmp]
    num_all.append(len(indices))
    
ind_sort = sorted(range(len(num_all)), key=lambda k: num_all[k],reverse = True)
ind_all = []
val_all = []
for i in range(len(p_set_list)):
    tuple_count = 0
    if num_all[ind_sort[i]] < 2:
        break
    else:
        val_all.append(p_set_list[ind_sort[i]])
        ind_all.append(num_all[ind_sort[i]])

# Build the co-occurrence matrix
# How many unique words in the list
new_living_list = []
for i in range(len(ind_all)):
    new_living_list.append(p_set_list[ind_sort[i]])
p_co_matrix = np.zeros((len(new_living_list),len(all_obj)))
   
# Count for P
xx = []
for item in obj_tuple_living:
    item_join = " ".join(item['primary'])
    if item_join in new_living_list:
        indice = new_living_list.index(item_join)
        obj = item['obj']
        for obj_item in obj:
            ind = all_obj.index(obj_item)
            p_co_matrix[indice,ind] += 1

# Count for S       
for item in obj_tuple_living:
    item_join = " ".join(item['secondary'])
    if item_join in new_living_list:
        indice = new_living_list.index(item_join)
        obj = item['obj']
        for obj_item in obj:
            ind = all_obj.index(obj_item)
            p_co_matrix[indice,ind] += 1
        
sio.savemat("living_co_matrix",{'p_co_matrix':p_co_matrix})

# for park scenes
obj_tuple_park = []
for i in range(len(park_ans)):
    if park_ans[i]['tuple_answer'] == 'yes':
        obj_tuple_park.append(park_tuple[i])

# compute both the p set and s set into one matrix
p_list = []
r_list = []
s_list = []
for item in obj_tuple_park:
    p_list.append(" ".join(item['primary']))
    r_list.append(" ".join(item['relation']))
    s_list.append(" ".join(item['secondary']))
    
p_set = set(p_list)
r_set = set(r_list)
s_set = set(s_list)

p_set_list = list(p_set)
r_set_list = list(r_set)
s_set_list = list(s_set)

ind_all = []
val_all = []
num_all = []

p_set_list += s_set_list
p_set_list = list(set(p_set_list))
p_list += s_list

for i in range(len(p_set_list)):
    tmp = p_set_list[i]
    indices = [ii for ii, x in enumerate(p_list) if x == tmp]
    num_all.append(len(indices))
    
ind_sort = sorted(range(len(num_all)), key=lambda k: num_all[k],reverse = True)
ind_all = []
val_all = []
for i in range(len(p_set_list)):
    tuple_count = 0
    if num_all[ind_sort[i]] < 2:
        break
    else:
        val_all.append(p_set_list[ind_sort[i]])
        ind_all.append(num_all[ind_sort[i]])

new_park_list = []
for i in range(len(ind_all)):
    new_park_list.append(p_set_list[ind_sort[i]])
p_co_matrix = np.zeros((len(new_park_list),len(all_obj)))


# For P
xx = []
for item in obj_tuple_park:
    item_join = " ".join(item['primary'])
    if item_join in new_park_list:
        indice = new_park_list.index(item_join)
        obj = item['obj']
        for obj_item in obj:
            ind = all_obj.index(obj_item)
            p_co_matrix[indice,ind] += 1
            
# For S
for item in obj_tuple_park:
    item_join = " ".join(item['secondary'])
    if item_join in new_park_list:
        indice = new_park_list.index(item_join)
        obj = item['obj']
        for obj_item in obj:
            ind = all_obj.index(obj_item)
            p_co_matrix[indice,ind] += 1
        
# Save into mat file and compute mutual information there
sio.savemat("park_co_matrix",{'p_co_matrix':p_co_matrix})

json.dump(new_living_list,open('../abstract/living_word_list.json','w'))
json.dump(new_park_list,open('../abstract/park_word_list.json','w'))