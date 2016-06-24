% clear;clc;
% addpath('jsonlab');
% tdata=loadjson('items.json');
load('new_obj');
% scene = tdata;
instancelist = cell(length(new_obj),1);
for i=1:1:length(new_obj)
    instancelist{i} = new_obj{i}.name;
end
instancematrix = zeros(length(instancelist),10);
count = 52;
for i=52:1:length(new_obj)
    numtype = new_obj{i}.numtype;
    for j=1:1:numtype
        instancematrix(i,j) = count;
        count = count+1;
    end
end
categorylist = {'human';'animal';'largeObject';'smallObject'};
save('Lists.mat','categorylist','instancelist','instancematrix','-v7.3');
disp('saved');