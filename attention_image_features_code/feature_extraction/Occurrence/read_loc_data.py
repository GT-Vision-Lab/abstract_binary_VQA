import pdb # python debugger
import json
import os
import scipy.io as io
import numpy as np
from collections import defaultdict

# use this line on server
path_to_json = '../abstract_images/scene_json_abstract_v002_train2015/'

# use this line on local machine
#path_to_json = '../full_scale_01_indv'

files = os.listdir(path_to_json)

occur_coord = defaultdict(list)
cooccur_coord = defaultdict(list)

for index, f in enumerate(files):
    availObjects = json.loads(open(os.path.join(path_to_json, f)).read())['scene']['availableObject']
    data_present = [instance for Object in availObjects for instance in Object['instance'] if instance['present']]

    for i, obj in enumerate(data_present):
        assert(obj['present'])
        occur_coord['x'].append(obj['x'])
        occur_coord['y'].append(obj['y'])
        occur_coord['z'].append(obj['z'])
        occur_coord['flip'].append(obj['flip'])

        for j, other_obj in enumerate(data_present):
            if i != j:
                assert(other_obj['present'])
                cooccur_coord['x1'].append(obj['x'])
                cooccur_coord['x2'].append(other_obj['x'])
                cooccur_coord['y1'].append(obj['y'])
                cooccur_coord['y2'].append(other_obj['y'])
                cooccur_coord['z1'].append(obj['z'])
                cooccur_coord['z2'].append(other_obj['z'])
                cooccur_coord['flip'].append(obj['flip'])
    print index

write = {}
for o in occur_coord:
    write[o] = np.array(occur_coord[o])

io.savemat('xiao_feat/Occurrence/occur_coords.mat', write)

write = {}
for o in cooccur_coord:
    write[o] = np.array(cooccur_coord[o])

io.savemat('xiao_feat/Occurrence/cooccur_coords.mat', write)
